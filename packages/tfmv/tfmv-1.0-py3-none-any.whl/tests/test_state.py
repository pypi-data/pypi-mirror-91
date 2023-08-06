from unittest.mock import patch

import pytest
from assertpy import assert_that

from tfmv.client import TfClient
from tfmv.error import DuplicateError
from tfmv.state import TfState, filter_and_rename

test_items = ["a", "a.x", "a.x.j", "ab", "ab.xc.a.x", "b.x"]


@pytest.mark.parametrize(["items", "prefix", "new", "expected_from", "expected_to"], [
    pytest.param(test_items, "a", "A", ["a", "a.x", "a.x.j"], ["A", "A.x", "A.x.j"], id="a -> A"),
    pytest.param(test_items, "a.x", "a.X", ["a.x", "a.x.j"], ["a.X", "a.X.j"], id="a.x -> a.X"),
    pytest.param(test_items, "ab.x", "a.X", [], [], id="ab.x -> a.X"),
    pytest.param(test_items, "b", "", ["b.x"], ["x"], id="b -> ''"),
])
def test_filter_and_rename(items, prefix, new, expected_from, expected_to):
    from_, to_ = filter_and_rename(items, prefix, new)
    assert_that(from_).is_equal_to(expected_from)
    assert_that(to_).is_equal_to(expected_to)


@pytest.mark.parametrize(["items", "prefix", "new", "expected_error"], [
    pytest.param(test_items, "a.x", "b.x", ["b.x"], id="a.x -> b.x"),
])
def test_filter_and_rename_duplicate(items, prefix, new, expected_error):
    with pytest.raises(DuplicateError) as err:
        filter_and_rename(items, prefix, new)
    assert_that(err.value.duplicates).is_equal_to(expected_error)


@pytest.fixture(scope='function')
def work_dir(tmp_path):
    work_dir = tmp_path.joinpath("work")
    work_dir.mkdir()
    return work_dir


@pytest.fixture(scope='function')
def mock_client(tmp_path, work_dir):
    with patch("tfmv.state.TfClient", autospec=TfClient) as MockTfClient:
        MockTfClient.return_value.work_dir = work_dir
        yield MockTfClient


class TestTfState:

    def test_instance_without_path_has_default(self, mock_client, work_dir):
        assert_that(TfState(work_dir).local_state_path).is_equal_to(work_dir.joinpath("terraform.tfstate"))

    def test_pull_no_file_sets_path(self, mock_client, work_dir):
        state = TfState(work_dir)
        state.pull()
        assert_that(state.local_state_path).is_equal_to(work_dir.joinpath("terraform.tfstate"))

    def test_pull_with_file_set_path(self, mock_client, work_dir, tmp_path):
        state = TfState(work_dir)
        state_file = tmp_path.joinpath("state_file")
        state.pull(state_file)
        assert_that(state.local_state_path).is_equal_to(state_file)

    def test_pull_existing_file_raises(self, mock_client, work_dir):
        state = TfState(work_dir)
        state.local_state_path.touch()
        with pytest.raises(FileExistsError):
            state.pull()

    def test_push_calls_client(self, mock_client, work_dir):
        state = TfState(work_dir)
        state.local_state_path.touch()
        state.push()
        mock_client.return_value.state_push.assert_called_with(state.local_state_path)

    def test_push_without_file_raises(self, mock_client, work_dir):
        state = TfState(work_dir)
        with pytest.raises(FileNotFoundError):
            state.push()

    def test_list_calls_client_without_file(self, mock_client, work_dir):
        state = TfState(work_dir)
        state.list()
        mock_client.return_value.state_list.assert_called_with(state.local_state_path)

    def test_list_calls_client_with_file(self, mock_client, work_dir):
        state = TfState(work_dir)
        state.local_state_path.touch()
        state.list()
        mock_client.return_value.state_list.assert_called_with(state.local_state_path)

    def test_clean_without_file_does_nothing(self, mock_client, work_dir):
        state = TfState(work_dir)
        state.clean()

    def test_clean_removes_files(self, mock_client, work_dir):
        state = TfState(work_dir)
        state_file = state.local_state_path
        state_file.touch()
        state_other = state_file.parent.joinpath(f'{state_file.name}-1234')
        state_other.touch()
        state.clean()
        assert_that(state_file.exists()).is_false()
        assert_that(state_other.exists()).is_false()

    def test_clean_keeps_other_files(self, mock_client, work_dir):
        state = TfState(work_dir)
        state_file = state.local_state_path
        state_file.touch()
        other = state_file.parent.joinpath(f'another')
        other.touch()
        state.clean()
        assert_that(state_file.exists()).is_false()
        assert_that(other.exists()).is_true()

    def test_clean_dry_run_keeps_files(self, mock_client, work_dir):
        state = TfState(work_dir)
        state_file = state.local_state_path
        state_file.touch()
        state.clean(dry_run=True)
        assert_that(state_file.exists()).is_true()

    def test_move_to_calls_client(self, mock_client, work_dir):
        state = TfState(work_dir)
        state_file = state.local_state_path
        state_file.touch()
        state.move_to("a", "b", state)
        mock_client.return_value.state_mv.assert_called_with(state_file, state_file, "a", "b", "")

    def test_move_to_with_dry_run_calls_client(self, mock_client, work_dir):
        state = TfState(work_dir)
        state_file = state.local_state_path
        state_file.touch()
        state.move_to("a", "b", state, dry_run=True)
        mock_client.return_value.state_mv.assert_called_with(state_file, state_file, "a", "b", "-dry-run")

    def test_move_to_no_src_file_raises(self, mock_client, work_dir):
        state = TfState(work_dir)
        with pytest.raises(FileNotFoundError):
            state.move_to("a", "b", state)

    def test_move_to_no_dest_file_raises(self, mock_client, work_dir):
        other_dir = work_dir.parent.joinpath("other")
        other_dir.mkdir()
        state, other = TfState(work_dir), TfState(other_dir)
        state.local_state_path.touch()
        with pytest.raises(FileNotFoundError):
            state.move_to("a", "b", other)