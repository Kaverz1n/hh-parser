class Vacancy:
    '''
    Класс вакансий работадателей с сайта
    https://hh.ru/
    '''

    def __init__(
            self, name: str, description: str, area: str,
            salary_from: int, salary_to: int, currency: int,
            experience: str, employment: str, address: str
    ) -> None:
        self.name = name
        self.description = description
        self.area = area
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__currency = currency
        self.experience = experience
        self.employment = employment
        self.address = address

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name}, {self.description},' \
               f'{self.area}, {self.__salary_from},' \
               f'{self.__salary_to}, {self.__currency}, {self.experience},' \
               f'{self.employment}, {self.address}'

    def __str__(self) -> str:
        return f'Вакансия {self.name}'

    @property
    def salary(self) -> int or None:
        '''
        Возвращает среднюю зарплату вакансии
        :return: средняя зарплата
        '''
        if (self.__salary_from + self.__salary_to) == 0:
            return None

        if self.__salary_from == 0:
            return self.__salary_to

        if self.__salary_to == 0:
            return self.salary_from

        salary = int((self.__salary_from + self.__salary_to) / 2)
        return salary

    @property
    def salary_from(self) -> int:
        '''
        Возвращает минимальную зарплату вакансии
        :return: минимальная зарплата вакансии
        '''
        return self.__salary_from

    @property
    def salary_to(self) -> int:
        '''
        Возвращает максимальную зарплату вакансии
        :return: максимальная зарплата вакансии
        '''
        return self.__salary_to

    @staticmethod
    def get_vacancies_inf(vacancies_list) -> list[list]:
        '''
        Возвращает список, в котором содержатся
        списки. Каждый содержит всю информацию о вакансии
        :return: список списков с информацией о вакансиях
        '''
        vacancies_inf_list = []

        for vacancy in vacancies_list:
            # заменяет значение аттрибутов, содержащих в себе пустую строку, на None
            for attribute_name, attribute_value in vars(vacancy).items():
                if attribute_value == '':
                    setattr(vacancy, attribute_name, None)

            vacancies_inf_list.append(
                [
                    vacancy.name,
                    vacancy.description,
                    vacancy.area,
                    vacancy.__salary_from,
                    vacancy.__salary_to,
                    vacancy.salary,
                    vacancy.__currency,
                    vacancy.experience,
                    vacancy.employment,
                    vacancy.address
                ]
            )

        return vacancies_inf_list
