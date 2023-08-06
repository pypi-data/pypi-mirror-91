import subprocess
from pathlib import Path
from typing import List


class TfClient:
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir

    def state_pull(self, state_file: Path):
        """Execute state pull and redirect to the given state file"""
        self._run_command("state pull", f'> "{state_file}"')

    def state_push(self, state_file: Path):
        """Execute state push for the given state file"""
        self._run_command("state push", f'"{state_file}"')

    def state_list(self, state_file: Path) -> List[str]:
        """List the content of the state (from the state file if given and exists)"""
        opt = f"-state={state_file}" if state_file.exists() else ""
        return self._run_command("state list", opt).split()

    def state_mv(self, from_file: Path, to_file: Path, from_object: str, to_object: str, opts: str = ""):
        """Execute state mv"""
        self._run_command("state mv", f'-state={from_file} -state-out="{to_file}" {from_object} {to_object} {opts}')

    def _run_command(self, command: str, extra="") -> str:
        """Execute a terraform command in the work directory"""
        cmd = f"""
        cd "{self.work_dir}" ;
        terraform state {command} {extra};
        """
        result = subprocess.run(["/usr/bin/bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"'terraform {cmd}' command failed: {result.stderr.decode('unicode_escape')}")
        return result.stdout.decode('unicode_escape')