import requests

from src.vacancy import Vacancy


class Employer:
    '''
    Класс работадателей сайта
    https://hh.ru/
    '''

    def __init__(
            self, name: str, type: str, area: str,
            description: str, employer_url: str, site_url: str,
            vacancies_url: str, open_vacancies: int
    ) -> None:
        self.name = name
        self.type = type
        self.area = area
        self.description = description
        self.__employer_url = employer_url
        self.__site_url = site_url
        self.__vacancies_url = vacancies_url
        self.open_vacancies = open_vacancies
        self.vacancies_list = []

        self.__get_vacancies()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name}, {self.type}, {self.area}, ' \
               f'{self.description}, {self.__employer_url}, {self.__site_url}, ' \
               f'{self.__vacancies_url}, {self.open_vacancies})'

    def __str__(self) -> str:
        return f'Работадель {self.name}'

    def __get_vacancies(self) -> None:
        '''
        Получает все вакансии работадателя, создавая на их основе
        объекты класса Vacancy с дальнейшим помещением их в
        список self.vacancies_list
        '''
        page = 0

        # цикл перебирает все вакансии автора
        while True:
            vacancies = requests.get(url=self.__vacancies_url, params={'page': page, 'per_page': 100}).json()

            if page == 20 or len(vacancies['items']) == 0:
                break

            for vacancy in vacancies['items']:
                vacancy_name = vacancy['name']

                try:
                     vacancy_requirement = vacancy['snippet']['requirement']
                     if vacancy_requirement is None:
                         raise AttributeError
                except AttributeError:
                    vacancy_requirement = ''

                try:
                    vacancy_responsibility = vacancy['snippet']['responsibility']
                    if vacancy_responsibility is None:
                        raise AttributeError
                except AttributeError:
                    vacancy_responsibility = ''

                vacancy_description = f'{vacancy_requirement} {vacancy_responsibility}'.strip()
                vacancy_area = vacancy['area']['name']

                # проверка на то, что у вакансии указана зарплата
                if vacancy['salary'] is None:
                    vacancy_salary_from = 0
                    vacancy_salary_to = 0
                    vacancy_currency = 'RUR'
                else:
                    vacancy_salary_from = vacancy['salary']['from']
                    vacancy_salary_to = vacancy['salary']['to']
                    vacancy_currency = vacancy['salary']['currency']

                vacancy_experience = vacancy['experience']['name']
                vacancy_employment = vacancy['employment']['name']
                vacancy_address = vacancy['address']
                vacancy_url = vacancy['alternate_url']

                # проверка на то, что у вакансии указан адрес
                if vacancy_address is None:
                    vacancy_address = 'Адресс не указан'
                else:
                    if vacancy['address']['raw'] is None:
                        vacancy_address = 'Адресс не указан'
                    else:
                        vacancy_address = vacancy['address']['raw']

                # устанавливает мин. зарплату 0, если её значение None
                if vacancy_salary_from is None:
                    vacancy_salary_from = 0

                # устанавливает макс. зарплату 0, если её значение None
                if vacancy_salary_to is None:
                    vacancy_salary_to = 0

                # создание объекта класса Vacancy и помещение его в список вакансий работадателя
                self.vacancies_list.append(
                    Vacancy(
                        vacancy_name, vacancy_description, vacancy_area,
                        vacancy_salary_from, vacancy_salary_to, vacancy_currency,
                        vacancy_experience, vacancy_employment, vacancy_address,
                        vacancy_url
                    )
                )

            page += 1

    def get_employer_inf(self) -> tuple:
        '''
        Возвращает кортеж, в котором содержится
        вся информация о работадателе
        :return: кортеж с информацией о работадателе
        '''
        # заменяет значение аттрибутов, содержащих в себе пустую строку, на None
        for attribute_name, attribute_value in vars(self).items():
            if attribute_value == '':
                setattr(self, attribute_name, None)

        employers_inf = (
            self.name,
            self.type,
            self.area,
            self.description,
            self.employer_url,
            self.site_url,
            self.open_vacancies
        )

        return employers_inf

    @property
    def employer_url(self) -> str:
        '''
        Возвращает ссылку на страницу работадателя
        :return: self.__employer_url
        '''
        return self.__employer_url

    @property
    def site_url(self) -> str:
        '''
        Возвращает ссылку на сайт работадателя
        :return: self.__site_url
        '''
        return self.__site_url

    @property
    def vacancies_url(self) -> str:
        '''
        Возвращает ссылку на список вакансий работадателя
        в формате JSON
        :return: self.__vacancies_url
        '''
        return self.__vacancies_url
