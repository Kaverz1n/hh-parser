import requests

from src.employer import Employer


class HHAPI:
    '''
    Класс для работы с API сайта
    https://hh.ru/
    '''

    def __init__(self, employers_id_list: list) -> None:
        self.__api = 'https://api.hh.ru/'
        self.employers_list = employers_id_list

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.employers_list})'

    def __str__(self) -> str:
        return 'API сайта https://hh.ru/'

    def get_employers(self) -> list:
        '''
        Получает список работадателей, созданных
        на основе класса Employer
        :return: список объектов класса Employer
        '''
        employer_list = []
        for employer_id in self.employers_list:
            response = requests.get(url=f'{self.__api}employers/{employer_id}').json()

            employer = Employer(
                response['name'],
                response['type'],
                response['area']['name'],
                response['description'],
                response['alternate_url'],
                response['site_url'],
                response['vacancies_url'],
                response['open_vacancies']
            )

            employer_list.append(employer)

        return employer_list
