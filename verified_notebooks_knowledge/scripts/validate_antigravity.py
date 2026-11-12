#!/usr/bin/env python3
"""
Antigravity Customization Validator for HALO RAG Studio.

Performs rigorous structural and schema validation on:
  - Custom Agents (.agents/agents/*.md)
  - Skills (.agents/skills/*/SKILL.md)
  - Rules (.agents/rules/*.md)
  - Lifecycle Hooks (.agents/hooks.json)
  - MCP Config (.agents/mcp_config.json)
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
import yaml


class AntigravityValidator:
    SUPPORTED_TRIGGERS = {"always_on", "model_decision", "glob", "manual"}
    ALLOWED_AGENT_FIELDS = {"name", "description", "model", "tools"}

    def __init__(self, root_dir: str = ".agents", quiet: bool = False):
        self.root_dir = root_dir
        self.quiet = quiet
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed_checks = 0

    def log(self, msg: str) -> None:
        if not self.quiet:
            print(msg)

    def extract_frontmatter(self, fpath: str) -> Tuple[Optional[Dict[str, Any]], str]:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
        if not match:
            return None, content

        try:
            fm = yaml.safe_load(match.group(1))
            return fm, match.group(2)
        except Exception as e:
            self.errors.append(f"{fpath}: Invalid YAML frontmatter: {e}")
            return None, content

    def validate_agents(self) -> None:
        agents_dir = os.path.join(self.root_dir, "agents")
        if not os.path.exists(agents_dir):
            self.errors.append(f"Missing agents directory: {agents_dir}")
            return

        expected_agents = [
            "orchestrator", "planner", "researcher", "architect",
            "rag-engineer", "agent-engineer", "integration-engineer",
            "implementer", "qa-tester", "code-reviewer", "security-auditor",
            "documentation-agent"
        ]

        for name in expected_agents:
            fpath = os.path.join(agents_dir, f"{name}.md")
            if not os.path.exists(fpath):
                self.errors.append(f"Missing custom agent manifest: {fpath}")
                continue

            fm, body = self.extract_frontmatter(fpath)
            if not fm or not isinstance(fm, dict):
                self.errors.append(f"{fpath}: Missing or invalid frontmatter")
                continue

            # Check supported fields
            unsupported = set(fm.keys()) - self.ALLOWED_AGENT_FIELDS
            if unsupported:
                self.errors.append(f"{fpath}: Contains unsupported agent frontmatter fields: {unsupported}")

            if "name" not in fm or fm["name"] != name:
                self.errors.append(f"{fpath}: Frontmatter 'name' must match filename: expected '{name}', got '{fm.get('name')}'")

            if "description" not in fm or len(fm["description"].strip()) < 10:
                self.errors.append(f"{fpath}: Missing or too short 'description'")

            if len(body.strip()) < 50:
                self.errors.append(f"{fpath}: Agent instructions body is empty or too short")

            self.passed_checks += 1
            self.log(f"  [AGENT OK] {name}")

    def validate_skills(self) -> None:
        skills_dir = os.path.join(self.root_dir, "skills")
        if not os.path.exists(skills_dir):
            self.errors.append(f"Missing skills directory: {skills_dir}")
            return

        expected_skills = [
            "project-bootstrap", "system-diagnostics", "corpus-ingestion",
            "rag-development", "rag-evaluation", "dual-speed-orchestration",
            "litellm-integration", "testing-validation", "security-audit",
            "documentation-maintenance"
        ]

        for sname in expected_skills:
            sdir = os.path.join(skills_dir, sname)
            fpath = os.path.join(sdir, "SKILL.md")
            if not os.path.exists(fpath):
                self.errors.append(f"Missing skill definition: {fpath}")
                continue

            fm, body = self.extract_frontmatter(fpath)
            if not fm or not isinstance(fm, dict):
                self.errors.append(f"{fpath}: Missing or invalid frontmatter")
                continue

            if "name" not in fm or fm["name"] != sname:
                self.errors.append(f"{fpath}: Skill name mismatch: expected '{sname}', got '{fm.get('name')}'")

            if "description" not in fm or len(fm["description"].strip()) < 10:
                self.errors.append(f"{fpath}: Missing or insufficient skill description")

            if "When to Activate" not in body or "Execution Steps" not in body:
                self.errors.append(f"{fpath}: Skill body missing required sections ('When to Activate', 'Execution Steps')")

            self.passed_checks += 1
            self.log(f"  [SKILL OK] {sname}")

    def validate_rules(self) -> None:
        rules_dir = os.path.join(self.root_dir, "rules")
        if not os.path.exists(rules_dir):
            self.errors.append(f"Missing rules directory: {rules_dir}")
            return

        expected_rules = [
            "evidence-and-truth.md", "architecture.md", "python-quality.md",
            "rag-data-governance.md", "agent-orchestration.md",
            "security-and-secrets.md", "testing-and-evaluation.md"
        ]

        for rname in expected_rules:
            fpath = os.path.join(rules_dir, rname)
            if not os.path.exists(fpath):
                self.errors.append(f"Missing rule manifest: {fpath}")
                continue

            fm, body = self.extract_frontmatter(fpath)
            if not fm or not isinstance(fm, dict):
                self.errors.append(f"{fpath}: Rule missing frontmatter")
                continue

            trigger = fm.get("trigger")
            if trigger not in self.SUPPORTED_TRIGGERS:
                self.errors.append(f"{fpath}: Invalid rule trigger '{trigger}'. Must be one of {self.SUPPORTED_TRIGGERS}")

            if trigger == "glob":
                if "globs" not in fm or not fm["globs"]:
                    self.errors.append(f"{fpath}: Rule with trigger='glob' must specify non-empty 'globs' list")

            if trigger == "model_decision":
                if "description" not in fm or len(fm["description"].strip()) < 10:
                    self.errors.append(f"{fpath}: Rule with trigger='model_decision' must provide descriptive 'description'")

            self.passed_checks += 1
            self.log(f"  [RULE OK] {rname} (trigger: {trigger})")

    def validate_hooks(self) -> None:
        fpath = os.path.join(self.root_dir, "hooks.json")
        if not os.path.exists(fpath):
            self.errors.append(f"Missing hooks configuration: {fpath}")
            return

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                self.errors.append(f"{fpath}: Root must be a JSON object mapping hook names to events")
                return

            valid_events = {"SessionStart", "PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation", "Stop"}
            for hook_name, events in data.items():
                if not isinstance(events, dict):
                    self.errors.append(f"{fpath}: Hook '{hook_name}' must be an object of events")
                    continue
                for event_name in events.keys():
                    if event_name not in valid_events:
                        self.errors.append(f"{fpath}: Hook '{hook_name}' has unsupported event '{event_name}'")

            self.passed_checks += 1
            self.log("  [HOOKS OK] hooks.json conforms to official Antigravity schema")
        except Exception as e:
            self.errors.append(f"{fpath}: JSON parse error: {e}")

    def validate_mcp(self) -> None:
        fpath = os.path.join(self.root_dir, "mcp_config.json")
        if not os.path.exists(fpath):
            self.errors.append(f"Missing MCP configuration: {fpath}")
            return

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
                self.errors.append(f"{fpath}: Missing 'mcpServers' object")
                return

            self.passed_checks += 1
            self.log("  [MCP OK] mcp_config.json verified")
        except Exception as e:
            self.errors.append(f"{fpath}: JSON parse error: {e}")

    def run(self) -> bool:
        self.log("=== Validating Antigravity Customizations (.agents/) ===")
        self.validate_agents()
        self.validate_skills()
        self.validate_rules()
        self.validate_hooks()
        self.validate_mcp()

        if self.errors:
            print("\n❌ VALIDATION ERRORS FOUND:")
            for err in self.errors:
                print(f"  - {err}")
            return False

        self.log(f"\n✅ SUCCESS: All {self.passed_checks} Antigravity customization checks passed!")
        return True


def main():
    parser = argparse.ArgumentParser(description="Validate Antigravity customization directory schema.")
    parser.add_argument("--root", default=".agents", help="Customization root directory")
    parser.add_argument("--quiet", action="store_true", help="Quiet output")
    args = parser.parse_args()

    validator = AntigravityValidator(root_dir=args.root, quiet=args.quiet)
    success = validator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
