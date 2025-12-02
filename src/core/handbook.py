"""
Handbook Loader - Programmatic Protocol Enforcement
Ensures any agent (human or AI) follows the exact instructions from handbook files.
"""
import os
from pathlib import Path

class HandbookLoader:
    def __init__(self, mode="BaseOPS"):
        self.mode = mode
        self.base_path = Path(__file__).parent.parent.parent  # Go up to ZKputer root
        
        if mode == "BaseOPS":
            self.handbook_dir = self.base_path / "BaseOPS" / "📚 Agent Handbook"
        else:
            self.handbook_dir = self.base_path / "HyperOPS" / "📚 Agent Handbook"
    
    def read_handbook(self):
        """
        Command: 'Read Handbook'
        Returns the exact files to read per AGENT_INSTRUCTIONS.md
        """
        files_to_read = []
        
        if self.mode == "BaseOPS":
            files_to_read = [
                "AGENT_INSTRUCTIONS.md",
                "daily_OPS.md",
                "PROTOCOL_COMPLIANCE.md",
                "SOURCE_PRIORITY_PROTOCOL.md"
            ]
        else:  # HyperOPS
            files_to_read = [
                "AGENT_INSTRUCTIONS.md",
                "daily_OPS.md",
                "HyperGrok_Prompt.md",
                "PROTOCOL_COMPLIANCE.md"
            ]
        
        handbook_content = {}
        for filename in files_to_read:
            filepath = self.handbook_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    handbook_content[filename] = f.read()
            else:
                handbook_content[filename] = f"[FILE NOT FOUND: {filepath}]"
        
        return handbook_content
    
    def get_daily_routine_steps(self):
        """
        Command: 'Run the Daily'
        Extracts the exact checklist from daily_OPS.md Part B
        """
        daily_ops_path = self.handbook_dir / "daily_OPS.md"
        
        if not daily_ops_path.exists():
            return ["ERROR: daily_OPS.md not found"]
        
        with open(daily_ops_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract Part B: Daily Routine section
        if self.mode == "BaseOPS":
            # Find "# PART B: DAILY ROUTINE" section
            if "# PART B: DAILY ROUTINE" in content:
                part_b = content.split("# PART B: DAILY ROUTINE")[1]
                return self._extract_phases(part_b)
        else:
            # HyperOPS
            if "# PART B: DAILY ROUTINE" in content:
                part_b = content.split("# PART B: DAILY ROUTINE")[1]
                return self._extract_phases(part_b)
        
        return ["ERROR: Could not parse daily routine"]
    
    def _extract_phases(self, text):
        """Extract phase headers from daily routine"""
        phases = []
        lines = text.split('\n')
        for line in lines:
            if line.startswith('### Phase'):
                phases.append(line.strip('# ').strip())
        return phases
    
    def get_compliance_rules(self):
        """
        Returns the exact compliance rules from the handbook
        """
        if self.mode == "BaseOPS":
            return {
                "max_fdv": 4000000,  # From daily_OPS.md line 324
                "min_liquidity": 50000,  # From daily_OPS.md line 328
                "min_age_hours": 0,
                "price_action_reject": "ALREADY PUMPED"  # From daily_OPS.md line 327
            }
        else:  # HyperOPS
            return {
                "max_risk_percent": 0.20,  # From daily_OPS.md line 429
                "max_leverage": 12,  # From daily_OPS.md line 431
                "account_equity": 100  # From daily_OPS.md line 429
            }
    
    def get_command_mapping(self):
        """
        Returns the exact command → action mapping from AGENT_INSTRUCTIONS.md
        """
        instructions_path = self.handbook_dir / "AGENT_INSTRUCTIONS.md"
        
        if not instructions_path.exists():
            return {}
        
        with open(instructions_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse command protocol section
        commands = {}
        if "## 🚀 Command Protocol" in content:
            protocol_section = content.split("## 🚀 Command Protocol")[1]
            # Extract command names (lines starting with **Command:**)
            for line in protocol_section.split('\n'):
                if line.startswith('**Command:**'):
                    cmd = line.split('**Command:**')[1].strip().strip('"')
                    commands[cmd] = True
        
        return commands
