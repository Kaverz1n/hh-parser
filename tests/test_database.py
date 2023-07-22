import psycopg2
import pytest

from src.database import DataBase
from src.config import config
from tests.test_employer import employer_fixture


@pytest.fixture
def database_fixture() -> DataBase:
    connection = psycopg2.connect(dbname='postgres', **config())
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS name')
    connection.close()

    database = DataBase('name')

    return database


def test_init(database_fixture) -> None:
    database = database_fixture
    assert database.db_name == 'name'

    database.close_connection()


def test_repr(database_fixture) -> None:
    database = database_fixture
    assert repr(database) == "DataBase('name')"

    database.close_connection()


def test_str(database_fixture) -> None:
    database = database_fixture
    assert str(database) == "База данных name"

    database.close_connection()


def test_create_table(database_fixture) -> None:
    database = database_fixture

    with psycopg2.connect(dbname='name', **config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM vacancies')
            assert cursor.fetchall() == []
            cursor.execute('SELECT * FROM employers')
            assert cursor.fetchall() == []

    connection.close()
    database.close_connection()


def test_fill_data(database_fixture, employer_fixture) -> None:
    employer = employer_fixture
    database = database_fixture
    database.fill_data([employer])

    with psycopg2.connect(dbname='name', **config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM employers')
            assert cursor.fetchall() == [
                (1, 'name', 'type', 'area', 'desc', 'emp_url', 'site_url', 2)
            ]
            cursor.execute('SELECT * FROM vacancies')
            assert cursor.fetchall() == [
                (1, 'Повар универсал', 1, 'Чистоплотность. Активность. Быстрота. '
                                          'Лепка пельменей, манты, треугольники.',
                 'Казань', 70000, 100000, 85000, 'RUR', 'Нет опыта', 'Полная занятость',
                 'Адресс не указан', 'https://hh.ru/vacancy/83176475'),
                (2, 'Экономист на производство', 1, 'Высокие аналитические способности, '
                                                    'ответственность, целеустремленность, '
                                                    'инициативность в рамках своих компетенций, '
                                                    'внимательность и высокая обучаемость. Умение '
                                                    'работать с большими объемами информации... '
                                                    'Сбор исходной информации и планирование. '
                                                    'Расчет себестоимости готовой продукции '
                                                    '(ежедневный отчет). План/факт анализ. Анализ '
                                                    'исполнения производственного плана и '
                                                    'ежемесячных...',
                 'Казань', 60000, 80000, 70000, 'RUR', 'От 3 до 6 лет', 'Полная занятость',
                 'Казань, Каучуковая улица, 5', 'https://hh.ru/vacancy/83176347')
            ]

    database.close_connection()


def test_create_db(database_fixture) -> None:
    database = database_fixture
    connection = psycopg2.connect(dbname='postgres', **config())
    connection.autocommit = True

    with connection.cursor() as cursor:
        with pytest.raises(psycopg2.errors.DuplicateDatabase):
            cursor.execute('CREATE DATABASE name')

    database.close_connection()


def test_connection_prop(database_fixture) -> None:
    database = database_fixture
    assert isinstance(database.connection, psycopg2.extensions.connection)

    database.close_connection()
