"""
TFMV

simple terraform utility
"""
import tempfile
from pathlib import Path

import click

from tfmv.state import TfState, filter_and_rename


@click.group()
def cli():
    pass


@cli.command()
@click.argument("from_", metavar="FROM")
@click.argument("to_", metavar="TO", default="", required=False)
@click.option("--src", help="source terraform configuration directory", default=".", type=click.Path("r"))
@click.option("--dest", help="destination terraform configuration directory (same as src if omitted)", default=None,
              type=click.Path("r"))
@click.option("--dry-run", "-n", help="do no write operation", is_flag=True, default=False)
@click.option("--verbose", "-v", is_flag=True, help="show detailed output")
@click.option("--use-tmp-dir", is_flag=True,
              help="use a temporary directory for local state files, instead of the configuration directory")
def mv(*args, **kwargs):
    """Terraform tool for copying/moving objects in/between states.

    Objects in the source state starting with the prefix `FROM` wil be used.
    If a value for `TO` is specified, the prefix will be changed to this value
    """
    _mv(*args, **kwargs)


def _mv(from_, to_="", src=".", dest=None, dry_run=False, verbose=False, use_tmp_dir=False):
    """implementation of the mv command"""
    if verbose:
        click.echo(f"from    = {from_}")
        click.echo(f"to      = {to_}")
        click.echo(f"src     = {src}")
        click.echo(f"dest    = {dest}")

    # check and adapt parameters
    if dest is None and (to_ == "" or to_ == from_):
        raise click.BadParameter("cannot move in place! (set TO or --dest or both)")
    src_state = TfState(src)
    dest_state = TfState(dest) if dest is not None else src_state
    if to_ == "":
        to_ = from_

    tmp = None
    src_state_file = None
    dest_state_file = None

    try:
        # get temporary local files if required
        if use_tmp_dir:
            tmp = tempfile.TemporaryDirectory()
            tmp_dir = Path(tmp.name)
            src_state_file = tmp_dir.joinpath("src-terraform.tfstate")
            dest_state_file = tmp_dir.joinpath("dest-terraform.tfstate")

        # pull states and read objects
        src_state.pull(src_state_file)
        if dest is not None:
            dest_state.pull(dest_state_file)
        src_objects = src_state.list()

        # filter objects and get new names
        from_objects, to_objects = filter_and_rename(src_objects, from_, to_)

        # log move info
        header = "would move: " if dry_run else "moving: "
        no_header = " " * len(header)
        if verbose:
            _print_op("", "src workspace:  ", src_state.home_path, color='white')
            _print_op("", "dest workspace: ", dest_state.home_path, color='white')
            _print_op("", "src state:  ", src_state.local_state_path, color='white')
            _print_op("", "dest state: ", dest_state.local_state_path, color='white')

        # move selected objects
        for from_object, to_object in zip(from_objects, to_objects):
            _print_op(header, "from: ", from_object)
            _print_op(no_header, "to:   ", to_object)
            src_state.move_to(from_object=from_object, to_object=to_object, dest=dest_state, dry_run=dry_run)

        # push state to remote
        if dry_run:
            click.echo(click.style("would push states to remote"))
        else:
            click.echo(click.style("pushing modified states to remote"))
            src_state.push()
            if dest:
                dest_state.push()

        # clean local state files
        src_state.clean(dry_run)
        if dest is not None:
            dest_state.clean(dry_run)

    finally:
        # clean temporary files
        if tmp is not None:
            tmp.cleanup()


def _print_op(row_header, relation, element, color="cyan"):
    click.echo(click.style(row_header, fg='yellow'), nl=False)
    click.echo(click.style(relation, fg=f'bright_{color}'), nl=False)
    click.echo(click.style(f"{element}", fg=f'{color}'))


