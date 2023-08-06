from pathlib import Path
from unittest.mock import patch, call, ANY

import click
import pytest
from assertpy import assert_that

import tfmv.client
import tfmv.error
from tfmv.state import TfState
from tfmv.main import _mv


@pytest.fixture(scope='function')
def mock_state():
    with patch("tfmv.main.TfState", autospec=tfmv.state.TfState) as MockTfState:
        MockTfState.return_value.list.return_value = ["foo.a", "foo.b", "other", "foobar", "foo"]
        MockTfState.return_value.home_path = Path('.')
        yield MockTfState


def test_mv_no_dest_creates_1_state(mock_state):
    _mv(from_="foo.a", to_="foo.aa", src="a")
    mock_state.assert_called_once_with("a")


def test_mv_with_dest_creates_2_states(mock_state):
    _mv(from_="foo.a", to_="foo.aa", src="a", dest="b")
    mock_state.assert_has_calls([call("a"), call("b")])


def test_mv_no_dest_renames(mock_state):
    _mv(from_="foo.a", to_="foo.aa", src="a")
    assert mock_state.return_value.move_to.call_count == 1
    mock_state.return_value.move_to.assert_called_once_with(from_object="foo.a", to_object="foo.aa", dest=ANY,
                                                            dry_run=False)


def test_mv_verbose(mock_state):
    _mv(from_="foo.a", to_="foo.aa", src="a", verbose=True)


def test_mv_tmp_file(mock_state):
    _mv(from_="foo.a", to_="foo.aa", src="a", use_tmp_dir=True)


def test_mv_dry_run_passed_to_move_to(mock_state):
    _mv(from_="foo", to_="bar", src="a", dry_run=True)
    mock_state.return_value.move_to.assert_has_calls([
        call(from_object="foo.a", to_object="bar.a", dest=ANY, dry_run=True)
    ])


def test_mv_dry_run_does_not_call_push(mock_state):
    _mv(from_="foo.a", to_="foo.aa", src="a", dry_run=True)
    mock_state.return_value.push.assert_not_called()


def test_mv_no_dest_no_to_raises(mock_state):
    with pytest.raises(click.BadParameter):
        _mv(from_="foo.a", src="a")


def test_mv_without_to_moves_objects(mock_state):
    _mv(from_="foo", src="a", dest="b")

    assert mock_state.return_value.move_to.call_count == 3
    mock_state.return_value.move_to.assert_has_calls([
        call(from_object="foo.a", to_object="foo.a", dest=ANY, dry_run=False),
        call(from_object="foo.b", to_object="foo.b", dest=ANY, dry_run=False),
        call(from_object="foo", to_object="foo", dest=ANY, dry_run=False),
    ])


def test_mv_without_dest_renames_objects(mock_state):
    _mv(from_="foo", to_="bar", src="a")

    assert mock_state.return_value.move_to.call_count == 3
    mock_state.return_value.move_to.assert_has_calls([
        call(from_object="foo.a", to_object="bar.a", dest=ANY, dry_run=False),
        call(from_object="foo.b", to_object="bar.b", dest=ANY, dry_run=False),
        call(from_object="foo", to_object="bar", dest=ANY, dry_run=False),
    ])


def test_mv_no_dest_calls_clean_once(mock_state):
    _mv(from_="foo", to_="bar", src="a")
    mock_state.return_value.clean.assert_called_once()


def test_mv_with_dest_calls_clean_for_both(mock_state):
    _mv(from_="foo", to_="bar", src="a", dest="b")
    assert_that(mock_state.return_value.clean.call_count).is_equal_to(2)


def test_mv_with_dry_run_calls_clean_with_dry_run(mock_state):
    _mv(from_="foo", to_="bar", src="a", dry_run=True)
    mock_state.return_value.clean.assert_called_once_with(True)


