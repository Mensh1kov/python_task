import re
from urllib.request import urlopen
from urllib.parse import quote
from urllib.parse import unquote
from urllib.error import URLError, HTTPError


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """

    try:
        link_wiki = 'https://ru.wikipedia.org/wiki/'
        with urlopen(link_wiki + quote(name)) as response:
            return response.read().decode('utf-8', errors='ignore')
    except (URLError, HTTPError):
        return None


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором
    заканчивается содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """

    if page:
        begin = page.find('<div id="bodyContent"')
        end = page.find('<div id="catlinks"')
        return begin, end
    else:
        return 0, 0


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все
    имеющиеся ссылки на другие вики-страницы без повторений и с учётом
    регистра.
    """

    if page:
        regex = r'[\'"]/wiki/([^:#]+?)[\'"]'
        list_titles = re.findall(regex, page[begin:end])
        return set(map(lambda title: unquote(title), list_titles))
    else:
        return None


class Article:
    def __init__(self, title, last_article):
        self.title = title
        self.last_article = last_article

    def get_jump_list(self):
        if self.last_article:
            return self.last_article.get_jump_list() + [self.title]
        return [self.title]


def find_chain(start, finish='Философия'):
    """
    Функция принимает на вход название начальной и конечной статьи и
    возвращает список переходов, позволяющий добраться из начальной статьи в
    конечную. Первым элементом результата должен быть start, последним —
    finish.
    Если построить переходы невозможно, возвращается None.
    """

    titles_visited = {start}
    articles = [Article(start, None)]
    for article in articles:
        page = get_content(article.title)
        if page:
            article_pos = extract_content(page)
            begin = article_pos[0]
            end = article_pos[1]
            titles_following = extract_links(page, begin, end)
            if finish not in titles_following:
                for title in titles_following:
                    if title not in titles_visited:
                        titles_visited.add(title)
                        articles.append(Article(title, article))
            else:
                return article.get_jump_list() + [finish]
    return None


def main():
    pass


if __name__ == '__main__':
    main()
