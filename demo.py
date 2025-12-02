#!/usr/bin/env python3
"""
ZKputer Auto-Demo Script
Runs automatically in the Docker environment to showcase the agent.
"""
import time
import subprocess
import os

def run_demo():
    """Execute a demo sequence showing ZKputer capabilities."""
    # Wait for desktop to be ready
    time.sleep(5)
    
    # Open a terminal and run the ZKputer agent
    terminal_cmd = [
        "xfce4-terminal",
        "--maximize",
        "--title=ZKputer - Sovereign Shadow Trader",
        "--execute", "python3", "/home/zkputer/zkputer/main.py"
    ]
    
    try:
        subprocess.Popen(terminal_cmd, env=os.environ.copy())
    except Exception as e:
        print(f"Demo failed to start: {e}")

if __name__ == "__main__":
    run_demo()
