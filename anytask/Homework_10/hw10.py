import argparse
import os
import pathlib
import re
import signal
import sys
import urllib.request
from typing import Optional
from urllib.error import URLError, HTTPError
import threading


def load_content(url: str) -> Optional[bytes]:
    try:
        return urllib.request.urlopen(url, timeout=10).read()
    except (HTTPError, URLError):
        return None


def correct_name_folder(name):
    invalid_char = r'\/:*?<>|'

    for char in invalid_char:
        name = name.replace(char, '')
    return name


def extract_articles(articles: int):
    url = 'https://habr.com'
    regex = r'href="(.+?)".*?"tm-article-snippet__title-link"><span>(.+?)<'
    regex2 = r'href="(.+?)".+?"pagination-next-page"'
    if page := load_content(url):
        page = page.decode()
    else:
        return
    arts = re.finditer(regex, page)
    count = 0

    while count < articles:
        try:
            art = next(arts).groups()
            if count == articles:
                break
            yield url + art[0], art[1]
            count += 1
        except StopIteration:
            if url_next_page := re.search(regex2, page):
                if page := load_content(url + url_next_page.group(1)).decode():
                    arts = re.finditer(regex, page)
            else:
                break


def extract_content(page):
    begin = page.find(r'class="tm-article-body"')
    end = page.rfind(r'<br/>')
    if end == -1:
        end = page.rfind(r'/p')
    return begin, end


def extract_picture_urls(page, begin, end):
    regex = r'<img src="(.+?)"'
    return re.findall(regex, page[begin:end])


def save_picture(url, path: pathlib.Path):
    if content := load_content(url):
        if not path.is_dir():
            path.mkdir(parents=True)
        (path / pathlib.Path(url).name).write_bytes(content)


def save_all_pictures(urls, path: pathlib.Path):
    for link in urls:
        save_picture(link, path)


def save_all_pictures_from_art(url, path: pathlib.Path):
    if page := load_content(url).decode():
        save_all_pictures(extract_picture_urls(page,
                                               *extract_content(page)), path)


def run_scraper(threads: int, articles: int, out_dir: pathlib.Path) -> None:
    lock = threading.Lock()
    arts = extract_articles(articles)

    def get_art():
        with lock:
            try:
                return next(arts)
            except StopIteration:
                return None

    def thread():
        while True:
            if not (art := get_art()) or event.is_set():
                break
            title = correct_name_folder(art[1])
            save_all_pictures_from_art(art[0], out_dir / pathlib.Path(title))

    for _ in range(threads):
        threading.Thread(target=thread).start()


def main():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} [ARTICLES_NUMBER] THREAD_NUMBER OUT_DIRECTORY',
        description='Habr parser',
    )
    parser.add_argument(
        '-n', type=int, default=25, help='Number of articles to be processed',
    )
    parser.add_argument(
        'threads', type=int, help='Number of threads to be run',
    )
    parser.add_argument(
        'out_dir', type=pathlib.Path, help='Directory to download habr images',
    )
    args = parser.parse_args()

    run_scraper(args.threads, args.n, args.out_dir)


event = threading.Event()
signal.signal(signal.SIGINT, lambda *args: event.set())

if __name__ == '__main__':
    main()
