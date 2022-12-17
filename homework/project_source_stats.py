import os
import sys
import itertools


def project_stats(path, extensions):
    """
    Вернуть число строк в исходниках проекта.
    
    Файлами, входящими в проект, считаются все файлы
    в папке ``path`` (и подпапках), имеющие расширение
    из множества ``extensions``.
    """

    return sum(map(number_of_lines,
                   with_extensions(extensions, iter_filenames(path))))


def total_number_of_lines(filenames):
    """
    Вернуть общее число строк в файлах ``filenames``.
    """

    return sum(map(number_of_lines, filenames))


def number_of_lines(filename):
    """ 
    Вернуть число строк в файле.
    """

    n = 1

    def func(line):
        if b'\n' not in line:
            nonlocal n
            n = 0
        return 1

    with open(filename, mode='rb') as file:
        count = sum(map(func, file))
        return count + n if count else 0


def iter_filenames(path):
    """
    Итератор по именам файлов в дереве.
    """

    def func(args):
        return map(lambda x: '\\'.join([args[0], x]), args[2])

    return itertools.chain(*map(func, os.walk(path)))


def with_extensions(extensions, filenames):
    """
    Оставить из итератора ``filenames`` только
    имена файлов, у которых расширение - одно из ``extensions``.
    """

    def my_filter(file):
        return get_extension(file) not in extensions

    return itertools.filterfalse(my_filter, filenames)


def get_extension(filename):
    """ Вернуть расширение файла """

    _, file_extension = os.path.splitext(filename)
    return file_extension


def print_usage():
    print("Usage: python project_sourse_stats.py <project_path>")


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print_usage()
    #     sys.exit(1)
    # project_path = sys.argv[1]
    # print(project_stats(project_path, {'.cs'}))
    print(project_stats(r'NSimulator', {'.cs'}))
    print(total_number_of_lines(iter_filenames(r'NSimulator')))
