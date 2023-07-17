from src.hh_api import HHAPI
from src.database import DataBase
from src.db_manager import DBManager


def create_db(database_name: str, employers_id_list: list) -> DataBase:
    '''
    Создаёт базу данных на основе классе DataBase,
    заполняя её данными
    :param database_name: имя базы данных
    :param employers_id_list: список id работадателей
    :return: база данных (object DataBase)
    '''
    api = HHAPI(employers_id_list)
    data_base = DataBase(database_name)
    data_base.fill_data(api.get_employers())

    return data_base


def load_db(database_name: str, employers_id_list: list) -> DataBase:
    '''
    Возвращает уже ране созданную базу данных с возможностью
    сохранить переданные данные (можно отказаться, чтобы
    избежать повторяющихся данных)
    :param database_name: имя базы данных
    :param employers_id_list: список id работадателей
    :return: база данных (object DataBase)
    '''
    api = HHAPI(employers_id_list)
    data_base = DataBase(database_name)

    while True:
        user_answer = input('Сохранить переданные данные в базу данных?(y/n) ')
        if user_answer.lower() == 'y':
            print('Сохраняются данные...')
            data_base.fill_data(api.get_employers())
            break
        elif user_answer.lower() == 'n':
            break
        else:
            print('Вы ввели что-то не то...')

    return data_base


def choose_bd(employers_id_list: list) -> DataBase:
    '''
    Возвращает базу данных выбранного типа (создать новую или
    выбрать ту, которая уже создана)
    :param employers_id_list: список id работадателей
    :return: база данных (object DataBase)
    '''
    while True:
        user_answer = input('Желаете создать новую бд (нет, если уже бд имеется)? (y/n) ')
        if user_answer.lower() == 'y':
            database_name = input('Введите желаемое имя для базы данных: ')
            print('Создаётся база данных и сохраняются данные...')
            database = create_db(database_name, employers_id_list)
            break
        elif user_answer.lower() == 'n':
            database_name = input('Введите имя базы данных: ')
            database = load_db(database_name, employers_id_list)
            break
        else:
            print('Вы ввели что-то не то...')

    return database

def menu(database: DataBase) -> None:
    '''
    Запускает меню выбора действий, который совершаются
    над данными сохранёными в бд, с их дальнейшим
    отображением пользователю
    '''
    while True:
        db_manager = DBManager(database)
        try:
            user_answer = int(input(
                'Добрый день! Что желаете сделать с получеными данными?\n'
                '0 - Выход\n'
                '1 - Вывести все вакансии с указанием работадателя\n'
                '2 - Вывести количество вакансий у каждого работадателя\n'
                '3 - Вывести вакансии, зарплата которых выше средней по вакансиям\n'
                '4 - Вывести вакансии по ключевым словам\n'
            ))
        except ValueError:
            print('Вы ввели что-то не то...')
            continue

        if user_answer == 1:
            for data in db_manager.get_all_vacancies():
                print(f"Работадатель: {data[0]}\nВакансия: {data[1]}\n"
                      f"Зарплата: {data[2]} {data[3]}\nURL: {data[4]}\n")
        elif user_answer == 2:
            for data in db_manager.get_companies_and_vacancies_count():
                print(f"{' — '.join(str(x) for x in data)} открытых вакансий")
            print(' ')
        elif user_answer == 3:
            for data in db_manager.get_vacancies_with_higher_salary():
                print(f'Вакансия: {data[0]}\nОписание: {data[1]}\nГород: {data[2]}\n'
                      f'Зарплата: {data[3]}-{data[4]} ({data[5]}) {data[6]}\nОпыт: {data[7]}\n'
                      f'Занятость: {data[8]}\nАдрес: {data[9]}\nURL: {data[10]}\n')
        elif user_answer == 4:
            keywords = input('Введите слово(а) для поиска: ')
            for data in db_manager.get_vacancies_with_keyword(keywords):
                print(f'Вакансия: {data[0]}\nОписание: {data[1]}\nГород: {data[2]}\n'
                      f'Зарплата: {data[3]}-{data[4]} ({data[5]}) {data[6]}\nОпыт: {data[7]}\n'
                      f'Занятость: {data[8]}\nАдрес: {data[9]}\nURL: {data[10]}\n')
        elif user_answer == 0:
            break
        else:
            print('Вы ввели что-то не то...')
