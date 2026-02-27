"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


def test_filter_returns_empty_when_no_interactions_match() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_does_not_mutate_input_list() -> None:
    interactions = [_make_log(1, 1, 1)]
    original = interactions.copy()
    _ = _filter_by_item_id(interactions, 1)
    assert interactions == original


def test_filter_handles_zero_and_negative_item_ids() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, -1), _make_log(3, 3, 1)]
    assert _filter_by_item_id(interactions, 0) == [interactions[0]]
    assert _filter_by_item_id(interactions, -1) == [interactions[1]]


def test_filter_with_non_integer_item_id_returns_empty() -> None:
    interactions = [_make_log(1, 1, 1)]
    assert _filter_by_item_id(interactions, "1") == []
    assert _filter_by_item_id(interactions, 1.0) == []


def test_filter_with_large_item_id_values() -> None:
    big = 10 ** 18
    interactions = [_make_log(1, 1, big)]
    assert _filter_by_item_id(interactions, big) == interactions
    assert _filter_by_item_id(interactions, big + 1) == []
