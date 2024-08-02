import pytest

from fuel_efficiency.entities.down_hill import DownHill
from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.plateau import Plateau
from fuel_efficiency.entities.up_hill import UpHill
from fuel_efficiency.entities.valley import Valley


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_eq_error_raised(node: Node):
    node_instance = node()
    other = int()

    with pytest.raises(NotImplementedError) as excinfo:
        node_instance == other
    assert 'Missing `position` or `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_lt_error_raised(node: Node):
    valley = node()
    other = int()

    with pytest.raises(NotImplementedError) as excinfo:
        valley < other
    assert 'Missing `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_gt_error_raised(node: Node):
    valley = node()
    other = int()

    with pytest.raises(NotImplementedError) as excinfo:
        valley > other
    assert 'Missing `weight` attribute' in str(excinfo.value)


@pytest.mark.parametrize('node', [Valley, UpHill, DownHill, Plateau])
def test_ne_error_raised(node: Node):
    valley = node()
    other = int()

    with pytest.raises(NotImplementedError) as excinfo:
        valley != other
    assert 'Missing `weight` attribute' in str(excinfo.value)
