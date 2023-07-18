import pytest

from src.vacancy import Vacancy


@pytest.fixture
def vacancy_fixture() -> Vacancy:
    vacancy = Vacancy(
        'test_name', 'test_desc', 'test_area', 12000,
        15000, 'RUR', 'От 3 до 6 лет', 'Полная занятость',
        'address', 'url'
    )
    return vacancy


def test_init(vacancy_fixture) -> None:
    vacancy = vacancy_fixture

    assert vacancy.name == 'test_name'
    assert vacancy.description == 'test_desc'
    assert vacancy.area == 'test_area'
    assert vacancy.salary_from == 12000
    assert vacancy.salary_to == 15000
    assert vacancy.currency == 'RUR'
    assert vacancy.experience == 'От 3 до 6 лет'
    assert vacancy.employment == 'Полная занятость'
    assert vacancy.address == 'address'
    assert vacancy.url == 'url'


def test_repr(vacancy_fixture) -> None:
    vacancy = vacancy_fixture

    assert repr(vacancy) == "Vacancy('test_name', 'test_desc', 'test_area', 12000, " \
                            "15000, 'RUR', 'От 3 до 6 лет', 'Полная занятость', 'address', 'url')"


def test_str(vacancy_fixture) -> None:
    vacancy = vacancy_fixture

    assert str(vacancy) == 'Вакансия test_name'


def test_salary(vacancy_fixture) -> None:
    vacancy = vacancy_fixture
    assert vacancy.salary == 13500

    setattr(vacancy, "_Vacancy__salary_from", 0)
    setattr(vacancy, "_Vacancy__salary_to", 0)
    assert vacancy.salary is None

    setattr(vacancy, "_Vacancy__salary_from", 0)
    setattr(vacancy, "_Vacancy__salary_to", 15000)
    assert vacancy.salary == 15000

    setattr(vacancy, "_Vacancy__salary_from", 16000)
    setattr(vacancy, "_Vacancy__salary_to", 0)
    assert vacancy.salary == 16000


def test_salary_prop(vacancy_fixture) -> None:
    vacancy = vacancy_fixture

    assert vacancy.salary_from == 12000
    assert vacancy.salary_to == 15000


def test_get_vacancies_inf(vacancy_fixture) -> None:
    vacancy_one = vacancy_fixture
    vacancy_params = []

    for attribute_name, attribute_value in vars(vacancy_one).items():
        vacancy_params.append(attribute_value)
    vacancy_two = Vacancy(*vacancy_params)

    vacancy_one.name = 'vacancy_one'
    vacancy_two.name = 'vacancy_two'
    vacancy_list = [vacancy_one, vacancy_two]

    assert Vacancy.get_vacancies_inf(vacancy_list) == [
        ['vacancy_one', 'test_desc', 'test_area', 12000, 15000, 13500, 'RUR',
         'От 3 до 6 лет', 'Полная занятость', 'address', 'url'],
        ['vacancy_two', 'test_desc', 'test_area', 12000, 15000, 13500, 'RUR',
         'От 3 до 6 лет', 'Полная занятость', 'address', 'url'],
    ]

    vacancy_one.name = ''
    assert Vacancy.get_vacancies_inf([vacancy_one]) == [
        [None, 'test_desc', 'test_area', 12000, 15000, 13500, 'RUR',
         'От 3 до 6 лет', 'Полная занятость', 'address', 'url']
    ]
