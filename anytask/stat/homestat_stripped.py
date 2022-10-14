from enum import Enum
from collections import Counter


class Key(Enum):
    MALE_NAME = 0,
    FEMALE_NAME = 1,
    ALL_MALE_NAME = 2,
    ALL_FEMALE_NAME = 3,
    YEARS = 4


def is_female_name(name):
    endings = ['а', 'я', 'ь']
    exceptions = ['Илья', 'Игорь', 'Никита', 'Лёва']
    if name[-1] in endings and not (name in exceptions):
        return True
    return False


def make_stat(filename):
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """

    with open(filename, encoding='cp1251') as file:
        text = file.read()
    start_name = text.find('/>', 0) + 3
    start_year = text.find('<h3>') + 4
    year = text[start_year:start_year + 4]
    start_year = text.find('<h3>', start_year) + 4
    stat = {Key.YEARS: {year: {Key.MALE_NAME: [],
                               Key.FEMALE_NAME: []
                               }
                        },
            Key.ALL_MALE_NAME: [],
            Key.ALL_FEMALE_NAME: []
            }
    while True:
        if start_name < start_year or start_year == 3:
            if start_name == 2:
                break
            end_name = text.find('</a>', start_name)
            last_name, first_name = text[start_name:end_name].split()
            if is_female_name(first_name):
                stat[Key.YEARS][year][Key.FEMALE_NAME].append(first_name)
                stat[Key.ALL_FEMALE_NAME].append(first_name)
            else:
                stat[Key.YEARS][year][Key.MALE_NAME].append(first_name)
                stat[Key.ALL_MALE_NAME].append(first_name)
            start_name = text.find('/>', start_name) + 3
        else:
            if start_year != 3:
                year = text[start_year:start_year + 4]
                stat[Key.YEARS][year] = {Key.MALE_NAME: [],
                                         Key.FEMALE_NAME: []
                                         }
            start_year = text.find('<h3>', start_year) + 4
    return stat


def extract_years(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """

    return sorted(list(stat[Key.YEARS].keys()))


def extract_general(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """

    all_names = stat[Key.ALL_MALE_NAME] + stat[Key.ALL_FEMALE_NAME]
    name_and_count = Counter(all_names)
    return name_and_count.most_common(len(name_and_count))


def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """

    name_and_count = Counter(stat[Key.ALL_MALE_NAME])
    return name_and_count.most_common(len(name_and_count))


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """

    name_and_count = Counter(stat[Key.ALL_FEMALE_NAME])
    return name_and_count.most_common(len(name_and_count))


def extract_year(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """

    stat_of_year = stat[Key.YEARS][year]
    all_names = stat_of_year[Key.MALE_NAME] + stat_of_year[Key.FEMALE_NAME]
    name_and_count = Counter(all_names)
    return name_and_count.most_common(len(name_and_count))


def extract_year_male(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """

    name_and_count = Counter(stat[Key.YEARS][year][Key.MALE_NAME])
    return name_and_count.most_common(len(name_and_count))


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """

    name_and_count = Counter(stat[Key.YEARS][year][Key.FEMALE_NAME])
    return name_and_count.most_common(len(name_and_count))


if __name__ == '__main__':
    pass
