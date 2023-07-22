import pytest

from src.employer import Employer
from src.vacancy import Vacancy


@pytest.fixture
def employer_fixture() -> Employer:
    employer = Employer('name', 'type', 'area', 'desc', 'emp_url',
                        'site_url', 'https://api.hh.ru/vacancies?employer_id=5173609', 2)

    return employer


def test_init(employer_fixture) -> None:
    employer = employer_fixture

    assert employer.name == 'name'
    assert employer.type == 'type'
    assert employer.area == 'area'
    assert employer.description == 'desc'
    assert employer.employer_url == 'emp_url'
    assert employer.site_url == 'site_url'
    assert employer.vacancies_url == 'https://api.hh.ru/vacancies?employer_id=5173609'
    assert employer.open_vacancies == 2


def test_repr(employer_fixture) -> None:
    employer = employer_fixture

    assert repr(employer) == "Employer('name', 'type', 'area', 'desc', 'emp_url', " \
                             "'site_url', 'https://api.hh.ru/vacancies?employer_id=5173609', 2)"


def test_str(employer_fixture) -> None:
    employer = employer_fixture
    assert str(employer) == 'Работадатель name'


def test_get_vacancies(employer_fixture) -> None:
    employer = employer_fixture

    for vacancy in employer.vacancies_list:
        assert isinstance(vacancy, Vacancy)

    assert len(employer.vacancies_list) == employer.open_vacancies


def test_get_employer_inf(employer_fixture) -> None:
    employer = employer_fixture

    assert employer.get_employer_inf() == ('name', 'type', 'area', 'desc', 'emp_url', 'site_url', 2)

    employer.name = ''
    assert employer.get_employer_inf() == (None, 'type', 'area', 'desc', 'emp_url', 'site_url', 2)


def test_prop(employer_fixture) -> None:
    employer = employer_fixture

    assert employer.employer_url == 'emp_url'
    assert employer.site_url == 'site_url'
    assert employer.vacancies_url == 'https://api.hh.ru/vacancies?employer_id=5173609'
