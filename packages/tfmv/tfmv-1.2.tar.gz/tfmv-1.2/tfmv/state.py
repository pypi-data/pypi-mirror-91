"""
state.py

related to terraform state operations
"""

from pathlib import Path
from typing import Union, Optional, List, Tuple

from tfmv.client import TfClient
from tfmv.error import DuplicateError


class TfState:
    """
    represents a terraform state
    """

    def __init__(self, path: Union[str, Path], verbose=False):
        self.home_path = Path(path)
        self._local_state_path: Optional[Path] = None
        self._tf_client = TfClient(self.home_path)
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        """set the state verbosity"""
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value
        self._tf_client.verbose = value

    @property
    def local_state_path(self) -> Path:
        """Path of the local state file"""
        if self._local_state_path is None:
            return self.home_path.joinpath("terraform.tfstate")
        return self._local_state_path

    def pull(self, state_file: Path = None) -> None:
        """Pulls the remote state to a local file (created in home directory if none is given)"""
        if state_file is not None:
            self._local_state_path = state_file
        self._tf_client.state_pull(self.local_state_path)

    def push(self) -> None:
        """Pushes the local state file to the remote state"""
        if not self.local_state_path.exists():
            raise FileNotFoundError(f"state '{self.home_path}' has no local file, call `pull` first")
        self._tf_client.state_push(self.local_state_path)

    def clean(self, dry_run=False) -> None:
        """Clean the local state file and its backups"""
        if not self.local_state_path.exists():
            return
        state_dir = self.local_state_path.parent
        for file in state_dir.glob(f"{self.local_state_path.name}*"):
            if dry_run:
                print(f"would delete file: {file}")
            else:
                file.unlink()

    def list(self) -> List[str]:
        """list the items in the state"""
        return self._tf_client.state_list(self.local_state_path)

    def move_to(self, from_object: str, to_object: str, dest: 'TfState', dry_run=False):
        """move an item"""
        if not self.local_state_path.exists():
            raise FileNotFoundError(f"source state '{self.home_path}' has no local state file, call `pull` first")
        if not dest.local_state_path.exists():
            raise FileNotFoundError(f"dest state '{self.home_path}' has no local state file, call `pull` first")
        opts = " -dry-run" if dry_run else ""
        self._tf_client.state_mv(self.local_state_path, dest.local_state_path, from_object, to_object, opts)


def filter_and_rename(items: List[str], prefix: str, new_prefix: str) -> Tuple[List[str], List[str]]:
    """filter items by prefix, and return replaces the prefix by a new prefix
    :param items: initial list of items
    :param prefix: only items starting with prefix + '.', or equal to prefix, are selected
    :param new_prefix: new prefix for renaming
    :return: tuple (filtered_items, renamed_items)
    """
    # """"""
    from_items, to_items, duplicates = [], [], []
    for item in items:
        if item == prefix or item.startswith(f'{prefix}.'):
            new_item = f'{new_prefix}{item[len(prefix):]}'
            if new_item.startswith('.'):
                new_item = new_item[1:]
            from_items.append(item)
            if new_item in items and new_prefix != prefix:
                duplicates.append(new_item)
            else:
                to_items.append(new_item)
    if any(duplicates):
        raise DuplicateError(*duplicates)
    return from_items, to_items
