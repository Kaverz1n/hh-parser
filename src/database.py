import psycopg2

from src.config import config
from src.vacancy import Vacancy


class DataBase:
    '''
    Класс базы данных
    '''
    instance = None

    def __new__(cls, *args, **kwargs) -> None:
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, db_name: str) -> None:
        self.__db_name = db_name
        self.__db_data = config()
        self.__create_db()

        self.__connection = psycopg2.connect(dbname=self.__db_name, **self.__db_data)
        self.__create_tables()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__db_name})'

    def __str__(self) -> str:
        return f'База данных {self.__db_name}'

    def __create_db(self) -> None:
        '''
        Создаёт базу данных с переданным пользователем названием
        '''
        try:
            # подключение к бд postgres
            connection = psycopg2.connect(dbname='postgres', **self.__db_data)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE {self.__db_name}')

            connection.close()
        except psycopg2.errors.DuplicateDatabase:
            pass
        finally:
            connection.close()

    def __create_tables(self) -> None:
        '''
        Заполняет созданнную бд таблицами, которые создаются в последствии
        выполнения кода из файла queries.sql
        '''
        # подключение к созданной бд
        connection = self.__connection
        with connection.cursor() as cursor:
            # создание таблиц в базе данных
            with open('queries.sql', 'r', encoding='UTF-8') as sql_file:
                commands = sql_file.read()
                cursor.execute(commands)

    def fill_data(self, employer_list: list) -> None:
        '''
        Заполняет созданные таблицы данными о работадателях
        и их вакансиях
        :param employer_list: список объектов класса Employer
        '''
        connection = self.__connection
        with connection.cursor() as cursor:
            for employer in employer_list:
                cursor.execute(
                    'INSERT INTO employers (name, type, area, description, employer_url, site_url, '
                    'open_vacancies) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    employer.get_employer_inf()
                )

                cursor.execute('SELECT COUNT(*) FROM employers')
                last_employer = cursor.fetchone()[0]

                # перебирает все вакансии работадателя
                for vacancy in Vacancy.get_vacancies_inf(employer.vacancies_list):
                    # добавляет в каждую вакансию employer_id
                    vacancy.insert(1, last_employer)
                    vacancy_inf = tuple(vacancy)

                    cursor.execute(
                        'INSERT INTO vacancies (name, employer_id, description, area, salary_from, '
                        'salary_to, salary, currency, experience, employment, address) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        vacancy_inf
                    )

            connection.commit()

    def close_connection(self):
        '''
        Закрывает соединение с базой данных
        '''
        connection = self.__connection
        connection.close()

    @property
    def db_name(self):
        '''
        Возвращает имя базы данных
        :return: имя базы данных
        '''
        return self.__db_name
