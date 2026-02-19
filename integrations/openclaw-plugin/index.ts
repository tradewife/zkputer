import { spawn } from "node:child_process";
import path from "node:path";

function getPluginConfig(api) {
  if (typeof api?.getConfig === "function") return api.getConfig() || {};
  if (api?.config && typeof api.config === "object") return api.config;
  return {};
}

function defaultMcpConfig(rawConfig) {
  const config = rawConfig || {};
  const command = config.mcpServerCommand || process.env.ZKPUTER_MCP_COMMAND || "cargo";
  const manifestPath =
    config.cargoManifestPath ||
    process.env.ZKPUTER_CARGO_MANIFEST_PATH ||
    path.resolve(process.cwd(), "Cargo.toml");
  const args =
    Array.isArray(config.mcpServerArgs) && config.mcpServerArgs.length > 0
      ? config.mcpServerArgs
      : ["run", "--manifest-path", manifestPath, "--bin", "mcp_server"];
  const env = typeof config.mcpServerEnv === "object" && config.mcpServerEnv ? config.mcpServerEnv : {};
  const requestTimeoutMs =
    Number.isFinite(config.requestTimeoutMs) && config.requestTimeoutMs > 0 ? config.requestTimeoutMs : 15000;
  return { command, args, env, requestTimeoutMs };
}

class StdioMcpClient {
  constructor(config) {
    this.command = config.command;
    this.args = config.args;
    this.env = config.env;
    this.requestTimeoutMs = config.requestTimeoutMs;
    this.proc = null;
    this.buffer = Buffer.alloc(0);
    this.nextId = 1;
    this.pending = new Map();
    this.initialized = false;
    this.starting = null;
  }

  async initialize() {
    if (this.initialized) return;
    if (this.starting) return this.starting;
    this.starting = this.#doInitialize();
    try {
      await this.starting;
      this.initialized = true;
    } finally {
      this.starting = null;
    }
  }

  async callTool(name, args) {
    await this.initialize();
    const result = await this.#sendRequest("tools/call", { name, arguments: args || {} });
    return result;
  }

  close() {
    if (this.proc && !this.proc.killed) {
      this.proc.kill("SIGTERM");
    }
    this.proc = null;
    this.initialized = false;
    for (const [, pending] of this.pending) {
      clearTimeout(pending.timer);
      pending.reject(new Error("MCP process closed"));
    }
    this.pending.clear();
  }

  async #doInitialize() {
    this.#ensureStarted();
    await this.#sendRequest("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      clientInfo: { name: "zkputer-openclaw-plugin", version: "0.1.0" }
    });
    this.#sendNotification("notifications/initialized", {});
  }

  #ensureStarted() {
    if (this.proc && !this.proc.killed) return;
    this.proc = spawn(this.command, this.args, {
      stdio: ["pipe", "pipe", "pipe"],
      env: { ...process.env, ...this.env }
    });

    this.proc.stdout.on("data", (chunk) => this.#onStdout(chunk));
    this.proc.stderr.on("data", () => {
      // intentionally ignored for MVP noise control
    });
    this.proc.on("exit", () => {
      const err = new Error("zkputer MCP process exited");
      for (const [, pending] of this.pending) {
        clearTimeout(pending.timer);
        pending.reject(err);
      }
      this.pending.clear();
      this.initialized = false;
      this.proc = null;
    });
  }

  #onStdout(chunk) {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    for (;;) {
      const headerEnd = this.buffer.indexOf("\r\n\r\n");
      if (headerEnd === -1) return;
      const header = this.buffer.slice(0, headerEnd).toString("utf8");
      let contentLength = null;
      for (const line of header.split("\r\n")) {
        const lower = line.toLowerCase();
        if (lower.startsWith("content-length:")) {
          contentLength = Number(line.slice("content-length:".length).trim());
        }
      }
      if (!Number.isFinite(contentLength) || contentLength < 0) {
        this.buffer = Buffer.alloc(0);
        return;
      }
      const frameEnd = headerEnd + 4 + contentLength;
      if (this.buffer.length < frameEnd) return;
      const body = this.buffer.slice(headerEnd + 4, frameEnd);
      this.buffer = this.buffer.slice(frameEnd);

      let message;
      try {
        message = JSON.parse(body.toString("utf8"));
      } catch {
        continue;
      }
      if (message && Object.prototype.hasOwnProperty.call(message, "id")) {
        const pending = this.pending.get(message.id);
        if (!pending) continue;
        this.pending.delete(message.id);
        clearTimeout(pending.timer);
        if (message.error) {
          pending.reject(new Error(message.error.message || "MCP error"));
        } else {
          pending.resolve(message.result);
        }
      }
    }
  }

  #sendNotification(method, params) {
    if (!this.proc || !this.proc.stdin.writable) return;
    const payload = JSON.stringify({ jsonrpc: "2.0", method, params });
    const frame = `Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`;
    this.proc.stdin.write(frame);
  }

  #sendRequest(method, params) {
    if (!this.proc || !this.proc.stdin.writable) {
      return Promise.reject(new Error("zkputer MCP process is not running"));
    }
    const id = this.nextId++;
    const payload = JSON.stringify({ jsonrpc: "2.0", id, method, params });
    const frame = `Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`MCP request timed out for method ${method}`));
      }, this.requestTimeoutMs);
      this.pending.set(id, { resolve, reject, timer });
      this.proc.stdin.write(frame, (err) => {
        if (err) {
          clearTimeout(timer);
          this.pending.delete(id);
          reject(err);
        }
      });
    });
  }
}

function toToolResult(result) {
  if (result && typeof result === "object" && Array.isArray(result.content)) {
    return result;
  }
  const fallback = result === undefined ? null : result;
  return {
    content: [{ type: "text", text: JSON.stringify(fallback, null, 2) }],
    structuredContent: fallback
  };
}

function toToolError(error) {
  return {
    isError: true,
    content: [
      {
        type: "text",
        text: `zkputer MCP error: ${error?.message || String(error)}`
      }
    ]
  };
}

export default function (api) {
  const config = defaultMcpConfig(getPluginConfig(api));
  const mcp = new StdioMcpClient(config);

  if (typeof api?.onShutdown === "function") {
    api.onShutdown(() => mcp.close());
  }

  api.registerTool(
    {
      name: "zkputer_verify_claim",
      description:
        "Submit a zkputer verification request through the zkputer MCP server and return the resulting receipt payload.",
      parameters: {
        type: "object",
        additionalProperties: false,
        properties: {
          venue: { type: "string", enum: ["hyperliquid", "base", "solana", "polymarket"] },
          claim_type: { type: "string", enum: ["ORDER_PLACED", "TRADE_EXECUTED"] },
          account_ref: { type: "string" },
          order_ref: { type: "string" },
          execution_ref: { type: "string" },
          wait_for_result: { type: "boolean" },
          wait_timeout_ms: { type: "integer" }
        },
        required: ["venue", "claim_type", "account_ref", "order_ref"]
      },
      async execute(_id, params) {
        try {
          const result = await mcp.callTool("zkputer_verify_claim", params || {});
          return toToolResult(result);
        } catch (err) {
          return toToolError(err);
        }
      }
    },
    { optional: true }
  );

  api.registerTool(
    {
      name: "zkputer_get_receipt",
      description: "Fetch a zkputer receipt by id via the zkputer MCP server.",
      parameters: {
        type: "object",
        additionalProperties: false,
        properties: {
          receipt_id: { type: "string" }
        },
        required: ["receipt_id"]
      },
      async execute(_id, params) {
        try {
          const result = await mcp.callTool("zkputer_get_receipt", params || {});
          return toToolResult(result);
        } catch (err) {
          return toToolError(err);
        }
      }
    },
    { optional: true }
  );
}
