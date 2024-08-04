import pytest
from pathfinding_challenge import InvalidComparisonError, MissingAttrError
from pathfinding_challenge.algorithms.context import Context
from pathfinding_challenge.entities.down_hill import DownHill
from pathfinding_challenge.entities.node import Node
from pathfinding_challenge.entities.plateau import Plateau
from pathfinding_challenge.entities.position import Position
from pathfinding_challenge.entities.up_hill import UpHill
from pathfinding_challenge.entities.valley import Valley


class TestNode(Node):
    def __hash__(self) -> int:
        return hash((self.position.x, self.position.y))


@pytest.fixture
def node1():
    return TestNode(weight=10.0, position=Position(0, 0))


@pytest.fixture
def node2():
    return TestNode(weight=10.0, position=Position(0, 0))


@pytest.fixture
def node3():
    return TestNode(weight=20.0, position=Position(1, 1))


def test_node_eq_same_weight(node1, node2):
    assert node1 == node2


def test_node_eq_different_weight(node1, node3):
    assert node1 != node3


def test_node_eq_not_node(node1):
    ANY_INT = 5
    with pytest.raises(InvalidComparisonError) as excinfo:
        node1 != ANY_INT
    assert f'Cannot compare Node with {type(ANY_INT)}' in str(excinfo.value)


def test_node_eq(node1):
    ANY_INT = 5.0
    with pytest.raises(InvalidComparisonError) as excinfo:
        node1 == ANY_INT
    assert f'Cannot compare Node with {type(ANY_INT)}' in str(excinfo.value)


def test_node_hash(node1):
    expected_hash = hash((node1.position.x, node1.position.y))
    assert hash(node1) == expected_hash


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_eq_error_raised(node: Node):
    node_instance = node()
    other = int()

    with pytest.raises(MissingAttrError) as excinfo:
        node_instance == other
    assert 'Missing `position` or `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_lt_error_raised(node: Node):
    valley = node()
    other = int()

    with pytest.raises(MissingAttrError) as excinfo:
        valley < other
    assert 'Missing `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_gt_error_raised(node: Node):
    valley = node()
    other = int()

    with pytest.raises(MissingAttrError) as excinfo:
        valley > other
    assert 'Missing `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_ne_error_raised(node: Node):
    valley = node()
    other = int()

    with pytest.raises(MissingAttrError) as excinfo:
        valley != other
    assert 'Missing `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize(
    ('node1', 'node2', 'expected_exception', 'exception_message'),
    [
        (
            UpHill(),
            Valley(),
            ValueError,
            'UpHill cannot be adjacent to Valley',
        ),
        (
            DownHill(),
            Plateau(),
            ValueError,
            'DownHill cannot be adjacent to Plateau',
        ),
        (Valley(), UpHill(), None, ''),  # No exception
        (Plateau(), DownHill(), None, ''),  # No exception
    ],
)
def test_validate_adjacent_nodes(
    node1: Node, node2: Node, expected_exception, exception_message
):
    """
    Test the _validate_adjacent_nodes method for forbidden
    adjacent node configurations.
    """
    if expected_exception:
        with pytest.raises(expected_exception) as excinfo:
            Context._validate_adjacent_nodes(node1, node2)
        assert exception_message in str(excinfo.value)
    else:
        Context._validate_adjacent_nodes(node1, node2)


def test_context_validate_grid():
    """
    Test the Context._validate_grid method for grids with
    forbidden adjacent nodes.
    """
    invalid_grid = [[Valley(), UpHill()], [DownHill(), Plateau()]]
    context = Context()
    with pytest.raises(
        ValueError, match='DownHill cannot be adjacent to Plateau'
    ):
        context._validate_grid(invalid_grid)

    valid_grid = [[Valley(), Plateau()], [UpHill(), DownHill()]]

    context._validate_grid(grid=valid_grid)
