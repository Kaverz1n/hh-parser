import psycopg2
import pytest

from tests.test_employer import employer_fixture
from src.database import DataBase
from src.config import config
from src.utils import *


@pytest.fixture
def database_fixture() -> DataBase:
    connection = psycopg2.connect(dbname='postgres', **config())
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS test')
    connection.close()

    database = DataBase('test')

    return database


def test_delete_db(database_fixture) -> None:
    database = database_fixture
    database.close_connection()

    delete_db('test')

    with psycopg2.connect(dbname='postgres', **config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'test'")
            assert cursor.fetchone() is None

    connection.close()


def test_create_db() -> None:
    database = create_db('test', ['5173609'])
    assert isinstance(database, DataBase)

    with psycopg2.connect(dbname='postgres', **config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'test'")
            assert cursor.fetchone()[0] == 1

    database.close_connection()
    connection.close()


@pytest.mark.parametrize('database_name, employers_id_list, result, u_input', [
    ('test', ['5173609'], (1,), 'y'),
    ('test', ['5173609'], (0,), 'n'),
])
def test_load_db(
        database_name, employers_id_list, result,
        u_input, monkeypatch, database_fixture
) -> None:
    database = database_fixture
    monkeypatch.setattr('builtins.input', lambda _: u_input)

    loaded_db = load_db(database_name, employers_id_list)
    with psycopg2.connect(dbname=database_name, **config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM employers")
            assert cursor.fetchone() == result

    connection.close()

    assert isinstance(loaded_db, DataBase)

    loaded_db.close_connection()
    database.close_connection()


@pytest.mark.parametrize('answers_list, database_name, result', [
    (['y', 'noname'], 'noname', 1),
    (['n', 'test', 'n'], 'test', 0)
])
def test_chose_bd(
        answers_list, database_name, result,
        monkeypatch, database_fixture
) -> None:
    database = database_fixture

    monkeypatch.setattr('builtins.input', lambda _: answers_list.pop(0))
    chosen_bd = choose_bd(['5173609'])

    with psycopg2.connect(dbname=database_name, **config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM employers")
            assert cursor.fetchone()[0] == result

    connection.close()

    chosen_bd.close_connection()
    database.close_connection()


@pytest.mark.parametrize('answer, result', [
    (
            ['1', '0'],
            'Работадатель: Альянс\nВакансия: Повар универсал\nЗарплата: 85000 RUR\n' \
            'URL: https://hh.ru/vacancy/83176475\n\nРаботадатель: Альянс\n' \
            'Вакансия: Экономист на производство\nЗарплата: 70000 RUR\n' \
            'URL: https://hh.ru/vacancy/83176347\n\n'
    ),
    (
            ['2', '0'],
            'Альянс — 2 открытых вакансий\n \n'
    ),
    (
            ['3', '0'],
            'Вакансия: Повар универсал\nОписание: Чистоплотность. Активность. Быстрота. Лепка пельменей, '
            'манты, треугольники.\nГород: Казань\nЗарплата: 70000-100000 (85000) RUR\nОпыт: Нет опыта\n'
            'Занятость: Полная занятость\nАдрес: Адресс не указан\nURL: https://hh.ru/vacancy/83176475\n\n'
    ),
    (
            ['4', 'экономист', '0'],
            'Вакансия: Экономист на производство\nОписание: Высокие аналитические способности, ответственность, '
            'целеустремленность, инициативность в рамках своих компетенций, внимательность и высокая обучаемость. '
            'Умение работать с большими объемами информации... Сбор исходной информации и планирование. '
            'Расчет себестоимости готовой продукции (ежедневный отчет). План/факт анализ. Анализ исполнения '
            'производственного плана и ежемесячных...\nГород: Казань\nЗарплата: 60000-80000 (70000) RUR\n'
            'Опыт: От 3 до 6 лет\nЗанятость: Полная занятость\nАдрес: Казань, Каучуковая улица, 5\n'
            'URL: https://hh.ru/vacancy/83176347\n\n'
    ),
    (
            ['0'],
            ''
    ),
])
def test_menu(
        answer, result, database_fixture,
        monkeypatch, capsys, employer_fixture
) -> None:
    database = database_fixture
    employer = HHAPI(['5173609']).get_employers()
    database.fill_data(employer)

    monkeypatch.setattr('builtins.input', lambda _: answer.pop(0))
    menu(database)

    captured = capsys.readouterr()
    output = captured.out
    assert output == result

    database.close_connection()


def test_menu_error_input(database_fixture, monkeypatch, capsys) -> None:
    database = database_fixture
    input_data = ['NotNumber', 0]

    monkeypatch.setattr('builtins.input', lambda _: input_data.pop(0))
    menu(database)

    captured = capsys.readouterr()
    output = captured.out
    assert output == 'Вы ввели что-то не то...\n'


@pytest.mark.parametrize('function, params, answers', [
    (load_db, ('test', ['1234']), ['breakethatfunc', 'n']),
    (choose_bd, (['1234']), ['breakethatfunc', 'n', 'test', 'n']),
    (menu, (DataBase('test'),), ['5', '0'])
])
def test_something_go_wrong(
        function, params, answers,
        monkeypatch, capsys
) -> None:
    database = monkeypatch.setattr('builtins.input', lambda _: answers.pop(0))
    function(*params)

    if isinstance(database, DataBase):
        database.close_connection()
    else:
        captured = capsys.readouterr()
        output = captured.out.split('\n')[0]
        assert output == 'Вы ввели что-то не то...'
