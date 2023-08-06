from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime
from typing import TypeVar, Optional, Tuple, Any, Generic, List

logger = logging.getLogger("range_dict.interval_tree")

T = TypeVar('T', int, float, date, datetime, Any)


@dataclass
class Node(Generic[T]):
    range_key: Tuple[T, T]

    max_key: T

    value: Any

    left: Optional[Node] = None
    right: Optional[Node] = None


class IntervalTree:
    def __init__(self):
        self.root = None

    def insert(self, range_key: Tuple[T, T], value: Any) -> None:
        range_key = _format_key(range_key)

        if not self.root:
            self.root = Node(range_key, range_key[1], value)
            return

        _insert(self.root, range_key, value)

    def find(self, range_key: Tuple[T, T]) -> List[Any]:
        range_key = _format_key(range_key)

        return _find(self.root, range_key, accumulator=[]) if self.root else []

    def keys(self) -> List[Any]:
        return _keys(self.root, accumulator=[]) if self.root else []


def _insert(node: Node, range_key: Tuple[T, T], value: Any):
    """
    Utility function, here actual recursive inserting happens.
    """
    lower_key, higher_key = range_key
    node_lower_key, node_higher_key = node.range_key

    if lower_key < node_lower_key:
        if not node.left:
            node.left = Node(range_key, range_key[1], value)
        else:
            _insert(node.left, range_key, value)
    else:
        if not node.right:
            node.right = Node(range_key, range_key[1], value)
        else:
            _insert(node.right, range_key, value)

    if node.max_key < higher_key:
        node.max_key = higher_key


def _find(node: Node, range_key: Tuple[T, T], accumulator: List[Any]) -> List[Any]:
    """
    Utility function, here actual recursive searching happens.
    """
    lower_key, higher_key = range_key

    if _overlap(node.range_key, range_key):
        accumulator.append(node.value)

    if node.left and node.left.max_key >= lower_key:
        _find(node.left, range_key, accumulator)
    elif node.right:
        _find(node.right, range_key, accumulator)

    return accumulator


def _overlap(range_key_1: Tuple[T, T], range_key_2: Tuple[T, T]) -> bool:
    """
    Checks if given ranges overlap.
    """
    lower_key_1, higher_key_1 = range_key_1
    lower_key_2, higher_key_2 = range_key_2

    return lower_key_1 <= higher_key_2 and lower_key_2 <= higher_key_1


def _format_key(range_key: Tuple[T, T]) -> Tuple[T, T]:
    lower_key, higher_key = range_key

    if type(lower_key) != type(higher_key):
        raise KeyError(f"Range Key must have elements of the same type ('{type(lower_key)}' != '{type(higher_key)}')")

    try:
        _ = lower_key > higher_key
    except TypeError:
        raise KeyError(f"Illegal key, can not compare '{lower_key}' with '{higher_key}'")

    if lower_key > higher_key:
        logger.warning(f"Inverting order of keys passed to Range Dict's Interval Tree: "
                       f"{range_key} -> {higher_key, lower_key}")
        range_key = higher_key, lower_key

    return range_key


def _keys(node: Node, accumulator: List[Any]) -> List[Any]:
    accumulator.append(node.range_key)

    if node.left:
        _keys(node.left, accumulator)

    if node.right:
        _keys(node.right, accumulator)

    return accumulator
