import datetime
import operator
import re
import unittest


class PageAndTime:
    def __init__(self):
        self.__page = None
        self.__time = None

    def update_if_faster(self, page, time):
        if not self.__page or (time and self.__time >= time):
            self.__page = page
            self.__time = time

    def update_if_slower(self, page, time):
        if not self.__page or (time and self.__time <= time):
            self.__page = page
            self.__time = time

    def get_page(self):
        return self.__page


class StatTime:
    __count_objects = 0

    def __init__(self, page):
        self.__page = page
        self.__all_time = 0
        self.__count = 0
        self.__num = StatTime.__count_objects
        StatTime.__count_objects += 1

    def __gt__(self, other):
        self_av_time = self.get_average_time()
        other_av_time = other.get_average_time()
        if self_av_time and other_av_time:
            if self_av_time > other_av_time:
                return True
            elif self_av_time == other_av_time:
                return self.__num < other.__num
        elif self_av_time or other_av_time:
            return True
        return False

    def get_page(self):
        return self.__page

    def get_count(self):
        return self.__count

    def add(self, time):
        if time:
            self.__all_time += time
            self.__count += 1

    def get_average_time(self):
        if not self.__count:
            return None
        return self.__all_time / self.__count


class StatPage:
    def __init__(self, page):
        self.__page = page
        self.__count = 0
        self.__time_stat = StatTime(page)

    def __lt__(self, other):
        if self.__count < other.__count:
            return True
        elif self.__count == other.__count:
            return self.__page < other.__page
        else:
            return False

    def get_time_stat(self):
        return self.__time_stat

    def update(self, time=None):
        self.__count += 1
        self.__time_stat.add(time)

    def get_page(self):
        return self.__page

    def get_count(self):
        return self.__count


class AllStatPages:
    def __init__(self):
        self.__faster_page = PageAndTime()
        self.__slower_page = PageAndTime()
        self.__all_pages = {}

    def add(self, page, time=None):
        if not self.__all_pages.get(page):
            self.__all_pages[page] = StatPage(page)
        self.__all_pages[page].update(time)
        self.__faster_page.update_if_faster(page, time)
        self.__slower_page.update_if_slower(page, time)

    def get_popular(self):
        if len(self.__all_pages):
            stat = self.__all_pages.items()
            return max(stat, key=operator.itemgetter(1))[0]
        return None

    def get_fastest_page(self):
        return self.__faster_page.get_page()

    def get_slowest_page(self):
        return self.__slower_page.get_page()

    def get_slowest_average_page(self):
        slower_average_page = StatTime(None)
        for stat_page in self.__all_pages.values():
            time_stat = stat_page.get_time_stat()
            if time_stat > slower_average_page:
                slower_average_page = time_stat
        return slower_average_page.get_page()


class StatObjects:
    def __init__(self):
        self.__all_objects = {}

    def add(self, client):
        if not self.__all_objects.get(client):
            self.__all_objects[client] = 1
        else:
            self.__all_objects[client] += 1

    def get_popular(self):
        if len(self.__all_objects):
            stat = sorted(self.__all_objects.items())
            return max(stat, key=operator.itemgetter(1))[0]
        return None


class AllStatClients:
    def __init__(self):
        self.__all_clients = StatObjects()
        self.__stat_by_date = {}

    def add(self, client, date):
        date = datetime.datetime.strptime(date, '%d/%b/%Y').date()
        self.__all_clients.add(client)
        if not self.__stat_by_date.get(date):
            self.__stat_by_date[date] = StatObjects()
        self.__stat_by_date[date].add(client)

    def get_popular_by_day(self):
        stat = {}
        for date in sorted(self.__stat_by_date):
            stat[date] = self.__stat_by_date[date].get_popular()
        return stat

    def get_popular(self):
        return self.__all_clients.get_popular()


class Parts:
    def __init__(self, parsed_line):
        self.__client = parsed_line.group(1)
        self.__date = parsed_line.group(2)
        self.__page = parsed_line.group(3)
        self.__browser = parsed_line.group(4)
        if parsed_line.group(5):
            self.__response_time = int(parsed_line.group(5))
        else:
            self.__response_time = None

    def get_client(self):
        return self.__client

    def get_date(self):
        return self.__date

    def get_page(self):
        return self.__page

    def get_browser(self):
        return self.__browser

    def get_response_time(self):
        return self.__response_time


class Parser:
    __regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(\d+?/' \
              r'\S+?/\d+):\d\d:\d\d:\d\d .+?] "[A-Z]{3,7} (\S+) ' \
              r'.+?" \d+ \d+ ".+?" "(.+?)"(?: (\d*))?'

    def __init__(self):
        self.__stat_browsers = StatObjects()
        self.__stat_pages = AllStatPages()
        self.__stat_clients = AllStatClients()

    def add_line(self, line):
        parsed_line = re.search(self.__regex, line)
        if parsed_line:
            parts = Parts(parsed_line)
            client = parts.get_client()
            date = parts.get_date()
            page = parts.get_page()
            browser = parts.get_browser()
            response_time = parts.get_response_time()
            self.__stat_browsers.add(browser)
            self.__stat_pages.add(page, response_time)
            self.__stat_clients.add(client, date)

    def results(self):
        key1 = 'MostActiveClientByDay'
        key2 = 'SlowestAveragePage'
        return {'FastestPage': self.__stat_pages.get_fastest_page(),
                'MostActiveClient': self.__stat_clients.get_popular(),
                key1: self.__stat_clients.get_popular_by_day(),
                'MostPopularBrowser': self.__stat_browsers.get_popular(),
                'MostPopularPage': self.__stat_pages.get_popular(),
                key2: self.__stat_pages.get_slowest_average_page(),
                'SlowestPage': self.__stat_pages.get_slowest_page()}


def make_stat():
    return Parser()


class LogStatTests(unittest.TestCase):
    def test_empty_line(self):
        parser = Parser()
        line = ''
        parser.add_line(line)
        key = {'FastestPage': None,
               'MostActiveClient': None,
               'MostActiveClientByDay': {},
               'MostPopularBrowser': None,
               'MostPopularPage': None,
               'SlowestAveragePage': None,
               'SlowestPage': None}
        self.assertEqual(parser.results(), key)

    def test_popular_browser(self):
        parser = Parser()
        line = '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET /tv/' \
               'useUser HTTP/1.1" 200 432 "http://callider" "Mozilla" 2878948'
        parser.add_line(line)
        self.assertEqual(parser.results()['MostPopularBrowser'], 'Mozilla')

    def test_slowest_page(self):
        parser = Parser()
        lines = ['192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET /tv1'
                 ' HTTP/1.1" 200 432 "http://callider" "Mozilla" 2',
                 '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET /tv2'
                 ' HTTP/1.1" 200 432 "http://callider" "Mozilla" 2',
                 '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET /tv3'
                 ' HTTP/1.1" 200 432 "http://callider" "Mozilla" 1']
        for line in lines:
            parser.add_line(line)
        self.assertEqual(parser.results()['SlowestPage'], '/tv2')

    def test_most_active_client(self):
        parser = Parser()
        lines = ['192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET /tv1'
                 ' HTTP/1.1" 200 432 "http://callider" "Mozilla" 2',
                 '192.168.12.11 - - [17/Feb/2013:06:37:21 +0600] "GET /tv2'
                 ' HTTP/1.1" 200 432 "http://callider" "Mozilla" 2',
                 '192.168.12.12 - - [17/Feb/2013:06:37:21 +0600] "GET /tv3'
                 ' HTTP/1.1" 200 432 "http://callider" "Mozilla" 1']
        for line in lines:
            parser.add_line(line)
        stat = 'MostActiveClient'
        self.assertEqual(parser.results()[stat], '192.168.12.10')
