#!/usr/bin/env python3
"""
Firejail Linux Sandbox Runner
=============================
Wraps code execution in an OS-level Linux namespace sandbox with seccomp filters,
dropped capabilities, isolated /tmp, immutable root, and zero network access.
"""

import os
import sys
import shutil
import subprocess
import time
from typing import List, Dict, Any, Optional


class FirejailRunner:
    def __init__(
        self,
        workspace_dir: Optional[str] = None,
        allow_network: bool = False,
        ram_limit_mb: int = 16384,
        cpu_time_limit_sec: int = 1800,
        python_bin: str = sys.executable,
    ):
        self.workspace_dir = os.path.abspath(workspace_dir or os.getcwd())
        self.allow_network = allow_network
        self.ram_limit_mb = ram_limit_mb
        self.cpu_time_limit_sec = cpu_time_limit_sec
        self.python_bin = python_bin
        self.firejail_bin = shutil.which("firejail")

    def is_available(self) -> bool:
        return self.firejail_bin is not None

    def build_firejail_args(self, target_cmd: List[str]) -> List[str]:
        if not self.firejail_bin:
            raise RuntimeError("Firejail binary not found on system PATH.")

        args = [
            self.firejail_bin,
            "--quiet",
            "--noprofile",
            "--noroot",
            "--caps.drop=all",
            "--seccomp",
            "--read-only=/",
            f"--read-write={self.workspace_dir}",
            f"--rlimit-as={self.ram_limit_mb}m",
            f"--rlimit-cpu={self.cpu_time_limit_sec}",
        ]

        # Isolate /tmp unless the workspace directory itself is in /tmp
        if not self.workspace_dir.startswith("/tmp") and not self.workspace_dir.startswith("/var/tmp"):
            args.append("--private-tmp")

        if not self.allow_network:
            args.append("--net=none")

        args.extend(target_cmd)
        return args

    def run_command(
        self,
        cmd: List[str],
        timeout_sec: Optional[int] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Runs a command inside the firejail sandbox (or direct if firejail unavailable)."""
        start_time = time.time()
        timeout = timeout_sec or self.cpu_time_limit_sec

        run_env = os.environ.copy()
        if env:
            run_env.update(env)

        if self.is_available():
            full_cmd = self.build_firejail_args(cmd)
            is_sandboxed = True
        else:
            full_cmd = cmd
            is_sandboxed = False

        try:
            proc = subprocess.run(
                full_cmd,
                cwd=self.workspace_dir,
                env=run_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )
            duration = time.time() - start_time
            return {
                "success": proc.returncode == 0,
                "exit_code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "duration_sec": round(duration, 3),
                "sandboxed": is_sandboxed,
                "command": full_cmd,
                "timed_out": False,
            }
        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "exit_code": -1,
                "stdout": e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                "stderr": (e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")) + "\nCommand timed out.",
                "duration_sec": round(duration, 3),
                "sandboxed": is_sandboxed,
                "command": full_cmd,
                "timed_out": True,
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "duration_sec": round(duration, 3),
                "sandboxed": is_sandboxed,
                "command": full_cmd,
                "timed_out": False,
            }

    def run_python_script(
        self,
        script_path: str,
        script_args: Optional[List[str]] = None,
        timeout_sec: Optional[int] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Convenience method to execute a Python script inside Firejail."""
        target_path = os.path.abspath(script_path)
        cmd = [self.python_bin, "-u", target_path]
        if script_args:
            cmd.extend(script_args)
        return self.run_command(cmd, timeout_sec=timeout_sec, env=env)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 firejail_runner.py <script.py> [args...]")
        sys.exit(1)

    script = sys.argv[1]
    args = sys.argv[2:]

    runner = FirejailRunner()
    if not runner.is_available():
        print("⚠️ Warning: Firejail is not installed on this system.")
    else:
        print("🛡️ Firejail sandbox initialized (Air-Gapped, Seccomp, Caps-Drop).")

    result = runner.run_python_script(script, script_args=args)
    if result["stdout"]:
        print(result["stdout"], end="")
    if result["stderr"]:
        print(result["stderr"], file=sys.stderr, end="")

    print(f"\n[Sandbox Execution completed in {result['duration_sec']}s with exit code {result['exit_code']}]")
    sys.exit(result["exit_code"])


if __name__ == "__main__":
    main()
