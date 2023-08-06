"""
client.py

makes calls to terraform CLI
"""

import subprocess
from pathlib import Path
from typing import List

import click


class TfClient:
    """
    CLI client for terraform
    """

    def __init__(self, work_dir: Path, verbose=False):
        self.work_dir = work_dir
        self.verbose = verbose

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

    # pylint: disable=too-many-arguments
    def state_mv(self, from_file: Path, to_file: Path, from_object: str, to_object: str, opts: str = ""):
        """Execute state mv"""
        if opts != "" and opts[0] != " ":
            opts = f' {opts}'
        self._run_command("state mv", f'-state={from_file} -state-out={to_file}{opts} '
                                      f'{_escape_quote(from_object)} {_escape_quote(to_object)}')

    def _run_command(self, command: str, extra="") -> str:
        """Execute a terraform command in the work directory"""
        if extra != "" and extra[0] != " ":
            extra = f' {extra}'
        cmd = f"cd \"{self.work_dir}\" ; terraform {command}{extra} ;"
        if self.verbose:
            _print("cmd: ", cmd, fg="blue")
        result = subprocess.run(["/usr/bin/bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=False)
        if result.returncode != 0:
            stdout = result.stdout.decode('unicode_escape')
            stderr = result.stderr.decode('unicode_escape')
            if self.verbose:
                _print("out: ", stdout, fg="blue")
                _print("err: ", stderr, fg="blue")
            raise RuntimeError(f"'terraform {cmd}' command failed: {stderr}")
        return result.stdout.decode('unicode_escape')


def _print(head, text, **kwargs):
    """print formatted log message"""
    if 'bold' in kwargs:
        kwargs = kwargs.pop('bold')
    click.echo(click.style(head, bold=True, **kwargs), nl=False)
    click.echo(click.style(text, bold=False, **kwargs))


def _escape_quote(item: str) -> str:
    return item.replace('["', '[\\"').replace('"]', '\\"]')
