"""
TFMV

simple terraform utility
"""
import tempfile
from pathlib import Path
from typing import List, Tuple

import click

from tfmv.state import TfState, filter_and_rename

VALID_PATH = click.Path(exists=True, file_okay=False, writable=True)


@click.command()
@click.argument("from_", metavar="FROM")
@click.argument("to_", metavar="TO", default="", required=False)
@click.option("--src", help="source terraform configuration directory", default=".", type=VALID_PATH)
@click.option("--dest", help="destination terraform configuration directory (same as src if omitted)", default=None,
              type=VALID_PATH)
@click.option("--dry-run", "-n", help="do no write operation", is_flag=True, default=False)
@click.option("--verbose", "-v", is_flag=True, help="show detailed output")
@click.option("--use-tmp-dir", is_flag=True,
              help="use a temporary directory for local state files, instead of the configuration directory")
def mv(*args, **kwargs):
    """Terraform tool for copying/moving objects in/between states.

    Objects in the source state starting with the prefix `FROM` wil be used.
    If a value for `TO` is specified, the prefix will be changed to this value
    """
    # pylint: disable=invalid-name
    _mv(*args, **kwargs)


def _mv(from_, to_="", src=".", dest=None, dry_run=False, verbose=False, use_tmp_dir=False):
    """internal implementation of the mv command using the Mover class"""
    # pylint: disable=too-many-arguments
    Mover(src, dest).set_options(dry_run, verbose, use_tmp_dir).run(from_, to_)


class Mover:
    """implements the mv command"""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, src=".", dest=None):
        self.src = src
        self.dest = dest
        self.dry_run = False
        self.verbose = False
        self.use_tmp_dir = False
        self.src_state = TfState(self.src)
        self.dest_state = TfState(self.dest) if self.has_dest else self.src_state

        self.tmp = None
        self.src_state_file = None
        self.dest_state_file = None

    def set_options(self, dry_run=False, verbose=False, use_tmp_dir=False) -> 'Mover':
        """set the Mover command options"""
        self.dry_run = dry_run
        self.verbose = verbose
        self.use_tmp_dir = use_tmp_dir
        self.src_state.verbose = verbose
        self.dest_state.verbose = verbose
        return self

    def run(self, from_prefix: str, to_prefix: str = ""):
        """run the mv command"""
        if to_prefix == "":
            to_prefix = from_prefix
        self._check(from_prefix, to_prefix)
        try:
            self._set_state_files()
            from_objects, to_objects = self._pull_and_get_objects(from_prefix, to_prefix)
            self._move_objects(from_objects, to_objects)
            self._push_states()
        finally:
            self._clean()

    @property
    def has_dest(self) -> bool:
        """has a dest been specified?"""
        return self.dest is not None

    def _check(self, from_: str, to_: str):
        if self.verbose:
            _print_op("mv: ", "from: ", from_, color='white')
            _print_op("    ", "to:   ", to_, color='white')
            _print_op("    ", "src:  ", self.src, color='white')
            _print_op("    ", "dest: ", self.dest, color='white')
        if not self.has_dest and (to_ in ("", from_)):
            raise click.BadParameter("cannot move in place! (set TO or --dest or both)")

    def _set_state_files(self):
        """create a temporary local dir if requested, and set the state files accordingly"""
        if self.use_tmp_dir:
            if self.verbose:
                click.echo(click.style("creating temp directory", fg="green", bold=True))
            self.tmp = tempfile.TemporaryDirectory()
            tmp_dir = Path(self.tmp.name)
            self.src_state_file = tmp_dir.joinpath("src-terraform.tfstate")
            self.dest_state_file = tmp_dir.joinpath("dest-terraform.tfstate")

    def _pull_and_get_objects(self, from_: str, to_: str) -> Tuple[List[str], List[str]]:
        # pull states and read objects
        if self.verbose:
            click.echo(click.style("pulling state", fg="green", bold=True))
        self.src_state.pull(self.src_state_file)
        if self.has_dest:
            self.dest_state.pull(self.dest_state_file)

        # filter objects and get new names
        if self.verbose:
            click.echo(click.style("listing objects", fg="green", bold=True))
        src_objects = self.src_state.list()
        from_objects, to_objects = filter_and_rename(src_objects, from_, to_)

        return from_objects, to_objects

    def _move_objects(self, from_objects: List[str], to_objects: List[str]):
        # log move info
        if self.verbose:
            click.echo(click.style("moving objects", fg="green", bold=True))
            _print_op("", "src workspace:  ", str(self.src_state.home_path), color='white')
            _print_op("", "dest workspace: ", str(self.dest_state.home_path), color='white')
            _print_op("", "src state:  ", str(self.src_state.local_state_path), color='white')
            _print_op("", "dest state: ", str(self.dest_state.local_state_path), color='white')
        header = "would move: " if self.dry_run else "moving: "
        no_header = " " * len(header)

        # move selected objects
        for from_object, to_object in zip(from_objects, to_objects):
            if self.verbose:
                _print_op(header, "from: ", from_object)
                _print_op(no_header, "to:   ", to_object)
            self.src_state.move_to(
                from_object=from_object,
                to_object=to_object,
                dest=self.dest_state,
                dry_run=self.dry_run
            )

    def _push_states(self):
        """push state to remote"""
        if self.verbose:
            click.echo(click.style("pushing state", fg="green", bold=True))
        if not self.dry_run:
            self.src_state.push()
        if self.has_dest:
            click.echo("would push dest state to remote" if self.dry_run else "pushing dest state to remote")
            if not self.dry_run:
                self.dest_state.push()

    def _clean(self):
        """clean local state files and temp directory"""
        if self.verbose:
            click.echo(click.style("cleaning local files", fg="green", bold=True))
        self.src_state.clean(self.dry_run)
        if self.has_dest:
            self.dest_state.clean(self.dry_run)

        # clean temporary files
        if self.tmp is not None:
            if self.verbose:
                click.echo(click.style("cleaning temporary files", fg="green", bold=True))
            self.tmp.cleanup()


def _print_op(row_header: str, relation: str, element: str, color="cyan"):
    click.echo(click.style(row_header, fg='yellow'), nl=False)
    click.echo(click.style(relation, fg=f'bright_{color}'), nl=False)
    click.echo(click.style(f"{element}", fg=f'{color}'))


if __name__ == "__main__":
    mv()
