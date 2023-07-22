import pytest

from src.database import DataBase
from src.db_manager import DBManager
from tests.test_database import database_fixture
from tests.test_employer import employer_fixture


@pytest.fixture
def db_manager_fixture(database_fixture) -> (DataBase, DBManager):
    database = database_fixture
    db_manager = DBManager(database)

    return database, db_manager


def test_init(db_manager_fixture) -> None:
    database, db_manager = db_manager_fixture
    assert isinstance(db_manager.database, DataBase)

    database.close_connection()


def test_repr(db_manager_fixture) -> None:
    database, db_manager = db_manager_fixture
    assert repr(db_manager) == "DBManager(<class 'src.database.DataBase'>)"

    database.close_connection()


def test_str(db_manager_fixture) -> None:
    database, db_manager = db_manager_fixture
    assert str(db_manager) == "Менеджер для работы с данными БД"

    database.close_connection()


def test_get_companies_and_vacancies_count(database_fixture, employer_fixture) -> None:
    database = database_fixture
    employer = employer_fixture
    database.fill_data([employer])

    db_manager = DBManager(database)
    assert db_manager.get_companies_and_vacancies_count() == [('name', 2)]

    database.close_connection()


def test_get_all_vacancies(database_fixture, employer_fixture) -> None:
    database = database_fixture
    employer = employer_fixture
    database.fill_data([employer])

    db_manager = DBManager(database)
    assert db_manager.get_all_vacancies() == [
        ('name', 'Повар универсал', 85000, 'RUR', 'https://hh.ru/vacancy/83176475'),
        ('name', 'Экономист на производство', 70000, 'RUR', 'https://hh.ru/vacancy/83176347')
    ]

    database.close_connection()


def test_get_avg_salary(database_fixture, employer_fixture) -> None:
    database = database_fixture
    employer = employer_fixture
    database.fill_data([employer])

    db_manager = DBManager(database)
    assert db_manager.get_avg_salary() == 77500

    database.close_connection()


def test_get_vacancies_with_higher_salary(database_fixture, employer_fixture) -> None:
    database = database_fixture
    employer = employer_fixture
    database.fill_data([employer])

    db_manager = DBManager(database)
    assert db_manager.get_vacancies_with_higher_salary() == [
        ('Повар универсал', 'Чистоплотность. Активность. Быстрота. Лепка пельменей, манты, треугольники.',
         'Казань', 70000, 100000, 85000, 'RUR', 'Нет опыта', 'Полная занятость', 'Адресс не указан',
         'https://hh.ru/vacancy/83176475')]

    database.close_connection()


def test_get_vacancies_with_keyword(database_fixture, employer_fixture) -> None:
    database = database_fixture
    employer = employer_fixture
    database.fill_data([employer])

    db_manager = DBManager(database)
    assert db_manager.get_vacancies_with_keyword('на производство') == [
        ('Экономист на производство', 'Высокие '
                                      'аналитические способности, ответственность, целеустремленность, '
                                      'инициативность в рамках своих компетенций, внимательность и высокая '
                                      'обучаемость. Умение работать с большими объемами информации... Сбор '
                                      'исходной информации и планирование. Расчет себестоимости готовой продукции '
                                      '(ежедневный отчет). План/факт анализ. Анализ исполнения производственного '
                                      'плана и ежемесячных...', 'Казань', 60000, 80000, 70000, 'RUR', 'От 3 до 6 лет',
         'Полная занятость', 'Казань, Каучуковая улица, 5', 'https://hh.ru/vacancy/83176347')]

    database.close_connection()
