from src.database import DataBase


class DBManager:
    '''
    Класс для работы с данными базы данных
    '''

    def __init__(self, database: DataBase) -> None:
        self.database = database
        self.__connection = database.connection

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({type(self.database)})'

    def __str__(self) -> str:
        return 'Менеджер для работы с данными БД'

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        '''
        Получает список кортежей, в которых содержится название
        компании и количество вакансий
        :return: список кортежей с названием компании и кол-вом вакансий
        '''
        connection = self.__connection
        data_list = []

        with connection.cursor() as cursor:
            cursor.execute('SELECT name, open_vacancies FROM employers')
            data_list.extend(cursor.fetchall())

        return data_list

    def get_all_vacancies(self) -> list[tuple]:
        '''
        Получает список кортежей в котором содержится информация о
        вакансии с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        :return: список кортежей с информацией о вакансиях
        '''
        connection = self.__connection
        vacancy_list = []

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    employers.name,
                    vacancies.name,
                    vacancies.salary,
                    vacancies.currency,
                    vacancies.url
                FROM 
                    vacancies
                    JOIN employers USING(employer_id) 
            '''
                           )
            vacancy_list.extend(cursor.fetchall())

        return vacancy_list

    def get_avg_salary(self) -> int:
        '''
        Получает среднюю зарплату по вакансиям.
        :return: средняя зарплата по вакансиям
        '''
        connection = self.__connection

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    ROUND(AVG(salary))
                FROM
                    vacancies
                WHERE
                    salary IS NOT NULL
            ''')

            return cursor.fetchall()[0][0]

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        '''
        Получает список кортежей с вакансиями, у которых зарплата
        выше средней по всем вакансиям.
        :return: список информации по вакансям, зарплата которой выше средней
        '''
        connection = self.__connection
        avg_salary = self.get_avg_salary()
        vacancy_list = []

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    name,
                    description,
                    area,
                    salary_from,
                    salary_to,
                    salary,
                    currency,
                    experience,
                    employment,
                    address,
                    url
                FROM 
                    vacancies
                WHERE 
                    salary IS NOT NULL
                    AND salary > %s
            ''', (avg_salary,))

            vacancy_list.extend(cursor.fetchall())

        return vacancy_list

    def get_vacancies_with_keyword(self, keywords: str) -> list[tuple]:
        '''
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова,
        :param keywords: слова для поиска
        :return: список вакансий, найденных по переданным словам
        '''
        connection = self.__connection
        vacancy_list = []

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    name,
                    description,
                    area,
                    salary_from,
                    salary_to,
                    salary,
                    currency,
                    experience,
                    employment,
                    address,
                    url
                FROM
                    vacancies
                WHERE 
                    LOWER(name) LIKE %s
            ''', (f'%{keywords.lower().strip()}%',))

            vacancy_list.extend(cursor.fetchall())

        return vacancy_list


