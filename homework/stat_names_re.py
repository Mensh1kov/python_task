import re
from urllib.request import urlopen
from collections import Counter


def without_re(html_page):
    pos = 0
    names = []
    while True:
        start = html_page.find('/>', pos)
        if start == -1:
            break
        end = html_page.find('</a', start)
        _, name = html_page[start + 2: end].split()
        names.append(name)
        pos = end

    names_stat = Counter(names)
    return names_stat.most_common(len(names_stat))


def with_re(html_page):
    regex = r'/>[а-яА-ЯёЁ]+ ([а-яА-ЯёЁ]+)'
    names = re.findall(regex, html_page)
    names_stat = Counter(names)
    return names_stat.most_common()


if __name__ == '__main__':
    URL = 'http://shannon.usu.edu.ru/ftp/python/hw2/home.html'
    with urlopen(URL) as response:
        html_page = response.read().decode('cp1251')
    print("Without re:", without_re(html_page))
    print("With re:", with_re(html_page))
    if with_re(html_page) == without_re(html_page):
        print("eq")
    else:
        print("not eq")