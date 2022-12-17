import datetime
import re
import unittest


def merge(*iterables, key=None):
    """Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.

    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций"""

    def default(x):
        return x

    if not key:
        key = default

    iter_dict = {}

    for iterable in iterables:
        it = iter(sorted(iterable, key=key))
        try:
            iter_dict[it] = next(it)
        except StopIteration:
            continue

    while iter_dict:
        el = min(iter_dict.items(), key=lambda x: key(x[1]))
        yield el[1]
        it = el[0]
        try:
            iter_dict[it] = next(it)
        except StopIteration:
            del iter_dict[it]


def log_key(s):
    """Функция по строке лога возвращает ключ для её сравнения по времени"""

    reg = r'\[(.+?) '
    res = re.search(reg, s)
    if res:
        str_time = res.group(1)
        format_time = r'%d/%b/%Y:%H:%M:%S'
        return datetime.datetime.strptime(str_time, format_time)
    else:
        return None


class TestTest(unittest.TestCase):
    def test_log_right(self):
        test_string = '...[23/Sep/2016:12:37:21 +0600]...'
        time = datetime.datetime(2016, 9, 23, 12, 37, 21)
        self.assertEqual(time, log_key(test_string))

    def test_log_wrong(self):
        test_string = '...[wrong_time...'
        self.assertEqual(None, log_key(test_string))

    def test_iter_works(self):
        iter1 = [1, 2, 4, 2]
        iter2 = [3, 5]
        result = [1, 2, 2, 3, 4, 5]
        i = 0
        for elem in merge(iter1, iter2):
            self.assertEqual(result[i], elem)
            i += 1

    def test_iter_works_with_str(self):
        iter1 = ['c', 'b', 'a']
        iter2 = ['e', 'd']
        result = ['a', 'b', 'c', 'd', 'e']
        i = 0
        for elem in merge(iter1, iter2):
            self.assertEqual(result[i], elem)
            i += 1

    def test_iter_with_date(self):
        log1 = ['a [01/Sep/2016:12:37:21 +0600]',
                '[02/Sep/2016:12:37:21 +0600]',
                '[03/Sep/2016:12:37:21 +0600]']
        log2 = ['b [01/Sep/2016:12:37:21 +0600]',
                '[12/Sep/2016:12:37:21 +0600]']
        res = ['a [01/Sep/2016:12:37:21 +0600]',
               'b [01/Sep/2016:12:37:21 +0600]',
               '[02/Sep/2016:12:37:21 +0600]',
               '[03/Sep/2016:12:37:21 +0600]',
               '[12/Sep/2016:12:37:21 +0600]']
        i = 0
        for elem in merge(log1, log2, key=log_key):
            self.assertEqual(res[i], elem)
            i += 1


if __name__ == '__main__':
    unittest.main()
