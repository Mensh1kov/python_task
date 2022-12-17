import argparse
import operator
import re
from enum import Enum


class Key(Enum):
    CLIENTS = 0,
    RESOURCES = 1


class StatData:
    def __init__(self):
        self.stat = {}

    def add(self, component):
        if component in self.stat:
            self.stat[component] += 1
        else:
            self.stat[component] = 1

    def get_stat(self):
        return self.stat


def get_stat(log_name, is_client, is_resource):
    regex_client = re.compile(r'(.+?),')
    regex_resource = re.compile(r' (/.+?),')
    clients = StatData()
    resources = StatData()
    try:
        with open(log_name, errors='ignore') as logs:
            for line in logs:
                if is_client:
                    client = re.match(regex_client, line)
                    if client:
                        clients.add(client.group(1))
                if is_resource:
                    resource = re.search(regex_resource, line)
                    if resource:
                        resources.add(resource.group(1))
    except IOError:
        return None
    return {Key.CLIENTS: clients,
            Key.RESOURCES: resources}


def get_popular(dict_stat):
    return max(dict_stat.items(), key=operator.itemgetter(1))[0]


def get_arg_parser():
    usage = '%(prog)s [-h] key [key ...] log_name'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('log_name',
                        help='file with logs for parse')
    group = parser.add_argument_group('keys')
    group.add_argument('-r', '--resource',
                       action='store_true',
                       help='get the most popular resource from log')
    group.add_argument('-c', '--client',
                       action='store_true',
                       help='get the most popular client from log')
    return parser


if __name__ == '__main__':
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    if not (args.client or args.resource):
        print(f'{arg_parser.prog}: error: need a key')
    elif stat := get_stat(args.log_name, args.client, args.resource):
        if args.client:
            print(get_popular(stat[Key.CLIENTS].get_stat()))
        if args.resource:
            print(get_popular(stat[Key.RESOURCES].get_stat()))
    else:
        print(f'{arg_parser.prog}: error: {args.log_name} is not found')
