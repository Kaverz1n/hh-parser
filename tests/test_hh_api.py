import pytest

from src.hh_api import HHAPI
from src.employer import Employer


@pytest.fixture
def hh_api_fixture() -> HHAPI:
    hh_api = HHAPI(['5173609'])

    return hh_api


def test_init(hh_api_fixture) -> None:
    api = hh_api_fixture
    assert api.employers_id_list == ['5173609']


def test_repr(hh_api_fixture) -> None:
    api = hh_api_fixture
    assert repr(api) == "HHAPI(['5173609'])"


def test_str(hh_api_fixture) -> None:
    api = hh_api_fixture
    assert str(api) == 'API сайта https://hh.ru/'


def test_get_employers(hh_api_fixture) -> None:
    api = hh_api_fixture
    for el in api.get_employers():
        assert isinstance(el, Employer)

    api = HHAPI(['NOT_WORKING_ID'])
    with pytest.raises(KeyError):
        api.get_employers()
