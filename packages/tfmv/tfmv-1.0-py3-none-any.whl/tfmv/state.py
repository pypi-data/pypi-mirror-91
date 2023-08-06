from pathlib import Path
from typing import Union, Optional, List

from tfmv.client import TfClient
from tfmv.error import DuplicateError


class TfState:
    def __init__(self, path: Union[str, Path]):
        self.home_path = Path(path)
        self._local_state_path: Optional[Path] = None
        self._tf_client = TfClient(self.home_path)

    @property
    def local_state_path(self) -> Path:
        if self._local_state_path is None:
            return self.home_path.joinpath("terraform.tfstate")
        return self._local_state_path

    def pull(self, state_file: Path = None) -> None:
        """Pulls the remote state to a local file (created in home directory if none is given)"""
        if state_file is not None:
            self._local_state_path = state_file
        if self.local_state_path.exists():
            raise FileExistsError(f"state '{self.home_path}' already has a local file, call `clean` first")
        self._tf_client.state_pull(state_file)

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
        for f in state_dir.glob(f"{self.local_state_path.name}*"):
            if dry_run:
                print(f"would delete file: {f}")
            else:
                f.unlink()

    def list(self) -> List[str]:
        return self._tf_client.state_list(self.local_state_path)

    def move_to(self, from_object: str, to_object: str, dest: 'TfState', dry_run=False):
        if not self.local_state_path.exists():
            raise FileNotFoundError(f"source state '{self.home_path}' has no local state file, call `pull` first")
        if not dest.local_state_path.exists():
            raise FileNotFoundError(f"dest state '{self.home_path}' has no local state file, call `pull` first")
        opts = "-dry-run" if dry_run else ""
        self._tf_client.state_mv(self.local_state_path, dest.local_state_path, from_object, to_object, opts)


def filter_and_rename(items, prefix: str, new_prefix: str):
    # prefix = f"{prefix}."
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
