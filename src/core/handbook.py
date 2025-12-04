from pathlib import Path
import json
import logging

class HandbookLoader:
    """
    Loads strategy-specific handbooks for AI agents.
    Supports BaseOPS, HyperOPS, ExtendOPS, and PumpOPS.
    
    NEW: Uses consolidated protocols from /protocols/ directory.
    Falls back to legacy handbook locations if protocols not found.
    """
    
    def __init__(self, mode="BaseOPS"):
        self.mode = mode
        self.base_path = Path(__file__).parent.parent.parent  # Go up to ZKputer root
        self.logger = logging.getLogger(f"HandbookLoader-{mode}")
        
        # NEW: Protocol paths (preferred)
        self.protocols_dir = self.base_path / "protocols"
        self.core_protocol_path = self.protocols_dir / "core" / "MASTER_PROTOCOL.md"
        self.risk_limits_path = self.protocols_dir / "core" / "RISK_LIMITS.json"
        self.compliance_schema_path = self.protocols_dir / "core" / "COMPLIANCE_SCHEMA.json"
        
        # OPS-specific protocol
        mode_map = {"BaseOPS": "base", "ExtendOPS": "extend", "HyperOPS": "hyper", "PumpOPS": "pump"}
        if mode not in mode_map:
            raise ValueError(f"Unknown mode: {mode}. Supported: BaseOPS, HyperOPS, ExtendOPS, PumpOPS")
        self.ops_protocol_path = self.protocols_dir / "ops" / f"{mode_map[mode]}.md"
        
        # LEGACY: Strategy-specific handbook paths (fallback)
        if mode == "BaseOPS":
            self.handbook_dir = self.base_path / "BaseOPS" / "📚 Agent Handbook"
        elif mode == "HyperOPS":
            self.handbook_dir = self.base_path / "HyperOPS" / "📚 Agent Handbook"
        elif mode == "ExtendOPS":
            self.handbook_dir = self.base_path / "ExtendOPS" / "docs" / "handbook"
        elif mode == "PumpOPS":
            self.handbook_dir = self.base_path / "PumpOPS" / "📚 Agent Handbook"
        
        # Check for new protocol structure first
        self.use_new_protocols = self.protocols_dir.exists() and self.core_protocol_path.exists()
        
        if not self.use_new_protocols:
            # Fall back to legacy
            if not self.handbook_dir.exists():
                self.logger.error(f"Handbook directory not found: {self.handbook_dir}")
                raise FileNotFoundError(f"Handbook directory not found for {mode}: {self.handbook_dir}")
    
    def load_file(self, filename):
        """Load a specific handbook file"""
        try:
            file_path = self.handbook_dir / filename
            if not file_path.exists():
                self.logger.error(f"Handbook file not found: {file_path}")
                return f"ERROR: Handbook file not found: {filename}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.logger.info(f"Loaded handbook file: {filename} ({len(content)} chars)")
                return content
        except Exception as e:
            self.logger.error(f"Error loading handbook file {filename}: {e}")
            return f"ERROR: Could not load {filename}: {str(e)}"
    
    def read_handbook(self):
        """Load the main protocol/handbook"""
        if self.use_new_protocols:
            return self._load_protocols()
        return self.load_file("daily_OPS.md")
    
    def _load_protocols(self):
        """Load from new protocol structure"""
        result = {}
        
        # Core protocol
        if self.core_protocol_path.exists():
            with open(self.core_protocol_path, 'r') as f:
                result["MASTER_PROTOCOL.md"] = f.read()
        
        # OPS-specific protocol
        if self.ops_protocol_path.exists():
            with open(self.ops_protocol_path, 'r') as f:
                result[f"{self.mode}_protocol.md"] = f.read()
        
        return result
    
    def read_agent_instructions(self):
        """Load agent instructions (bootstrap for new structure)"""
        if self.use_new_protocols:
            bootstrap_path = self.base_path / ".zkputer" / "AGENT_BOOTSTRAP.md"
            if bootstrap_path.exists():
                with open(bootstrap_path, 'r') as f:
                    return f.read()
        return self.load_file("AGENT_INSTRUCTIONS.md")
    
    def read_protocol_compliance(self):
        """Load protocol compliance rules"""
        if self.use_new_protocols:
            return self._load_protocols()
        return self.load_file("PROTOCOL_COMPLIANCE.md")
    
    def read_source_priority(self):
        """Load source priority protocol"""
        return self.load_file("SOURCE_PRIORITY_PROTOCOL.md")
    
    def get_risk_limits(self):
        """Load machine-readable risk limits from JSON"""
        if self.risk_limits_path.exists():
            with open(self.risk_limits_path, 'r') as f:
                return json.load(f)
        # Fallback to hardcoded
        return {
            "universal": {
                "max_risk_per_trade_percent": 20,
                "max_leverage": 12,
                "max_concurrent_positions": 2
            }
        }
    
    def get_compliance_schema(self):
        """Load the compliance schema for trade validation"""
        if self.compliance_schema_path.exists():
            with open(self.compliance_schema_path, 'r') as f:
                return json.load(f)
        return None
    
    def get_active_config(self):
        """Load ACTIVE_OPS.json configuration"""
        config_path = self.base_path / ".zkputer" / "ACTIVE_OPS.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {"active_mode": self.mode}
    
    def get_strategy_config(self):
        """Get strategy-specific configuration"""
        config = {
            "strategy": self.mode,
            "handbook_path": str(self.handbook_dir),
            "available_files": []
        }
        
        try:
            # List available handbook files
            for file_path in self.handbook_dir.glob("*.md"):
                config["available_files"].append(file_path.name)
        except Exception as e:
            self.logger.error(f"Error listing handbook files: {e}")
        
        return config
    
    def validate_handbook(self):
        """Validate that required handbook files exist"""
        required_files = ["daily_OPS.md", "AGENT_INSTRUCTIONS.md"]
        missing_files = []
        
        for filename in required_files:
            file_path = self.handbook_dir / filename
            if not file_path.exists():
                missing_files.append(filename)
        
        if missing_files:
            self.logger.error(f"Missing required handbook files: {missing_files}")
            return False, missing_files
        
        return True, []
    
    def switch_mode(self, new_mode):
        """Switch to a different strategy mode"""
        self.__init__(new_mode)
        return f"Switched to {new_mode} mode"
