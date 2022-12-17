#!/usr/bin/env python3

import argparse
import itertools
import os.path
import struct
import sys
import time
from datetime import datetime


class TarParser:
    _HEADER_FMT1 = '100s8s8s8s12s12s8sc100s255s'
    _HEADER_FMT2 = '6s2s32s32s8s8s155s12s'
    _HEADER_FMT3 = '6s2s32s32s8s8s12s12s112s31x'
    _READ_BLOCK = 16 * 2**20

    _FILE_TYPES = {
        b'0': 'Regular file',
        b'1': 'Hard link',
        b'2': 'Symbolic link',
        b'3': 'Character device node',
        b'4': 'Block device node',
        b'5': 'Directory',
        b'6': 'FIFO node',
        b'7': 'Reserved',
        b'D': 'Directory entry',
        b'K': 'Long linkname',
        b'L': 'Long pathname',
        b'M': 'Continue of last file',
        b'N': 'Rename/symlink command',
        b'S': "`sparse' regular file",
        b'V': "`name' is tape/volume header name"
    }
    
    @staticmethod
    def _parse_header(hdr):
        header1 = struct.unpack(TarParser._HEADER_FMT1, hdr)

        header2 = (header1[-1],)
        if header1[9].startswith(b'ustar\x00'):
            header2 = struct.unpack(TarParser._HEADER_FMT2, header1[-1])
        elif header1[9].startswith(b'ustar '):
            header2 = struct.unpack(TarParser._HEADER_FMT3, header1[-1])

        header = header1[:-1] + header2

        name = header[0]
        if len(header) > 16 and header[15]:
            name = b'/'.join((header[15], name))
        name = name.strip(b'\x00').decode()

        file_size = int(b'0' + header[4].strip(b'\x00'), 8)
        return header, name, file_size
    
    def _preprocess(self):
        self._files = {}
        self._fpts = []

        with open(self._filename, mode='rb') as f:
            hdr = f.read(512)
            while hdr:
                header, name, file_size = TarParser._parse_header(hdr)
                if header[7] == b'L':
                    name = f.read(512)[:file_size - 1].decode()
                    header, _, file_size = TarParser._parse_header(f.read(512))

                rest_bytes = (512 - file_size) % 512
                if name:
                    fdesc = (header, file_size, f.tell(), name)
                    self._files[name] = fdesc
                    self._fpts.append(fdesc)

                f.seek(file_size + rest_bytes, 1)
                hdr = f.read(512)
    
    def __init__(self, filename):
        '''
        Открывает tar-архив `filename` и производит его предобработку
        (если требуется)
        '''

        self._filename = filename
        self._preprocess()

    def extract(self, dest=os.getcwd()):
        '''
        Распаковывает данный tar-архив в каталог `dest`
        '''

        with open(self._filename, mode='rb') as tar:
            for descriptor in self._fpts:
                tar.seek(descriptor[2])

                if descriptor[3][-1] == '/':
                    os.makedirs(f'{dest}/{descriptor[3]}')
                else:
                    with open(f'{dest}/{descriptor[3]}', mode='wb') as file:
                        file.write(tar.read(descriptor[1]))

    def files(self):
        '''
        Возвращает итератор имён файлов (с путями) в архиве
        '''

        def key(file):
            return file[-1] == '/'

        return itertools.filterfalse(key, self._files.keys())

    def param(self, name_param, func=lambda x: x.decode()):
        def wrapper(value):
            return name_param, func(value)
        return wrapper

    def mtime(self, seconds):
        seconds = int(seconds.decode())
        time.monotonic()
        date = datetime.fromtimestamp(seconds)
        return date.strftime('%m %b %Y %X')

    def file_stat(self, filename):
        '''
        Возвращает информацию о файле `filename' в архиве.

        Пример (некоторые поля могут отсутствовать, подробности см. в описании
        формата tar):
        [
            ('Filename', '/NSimulator'),
            ('Type', 'Directory'),
            ('Mode', '0000755'),
            ('UID', '1000'),
            ('GID', '1000'),
            ('Size', '0'),
            ('Modification time', '29 Mar 2014 03:52:45'),
            ('Checksum', '5492'),
            ('User name', 'victor'),
            ('Group name', 'victor')
        ]
        '''

        if filename not in self._files:
            raise ValueError(filename)

        info = [('Filename', filename)]
        file = self._files.get(filename)

        index_param = {
            1: self.param('Mode'),
            2: self.param('UID'),
            3: self.param('GID'),
            4: self.param('Size', lambda x: int(x.decode())),
            5: self.param('Modification time', self.mtime),
            6: self.param('Checksum'),
            7: self.param('Type', lambda x: self._FILE_TYPES.get(x)),
            8: self.param('Link'),
            9: self.param('Magic'),
            10: self.param('Version'),
            11: self.param('User name'),
            12: self.param('Group name'),
            13: self.param('Device major'),
            14: self.param('Device minor'),
            15: self.param('Prefix'),
            16: self.param('Last access time'),
            17: self.param('Last change time')
        }
        params = file[0]

        for i in range(1, len(params)):
            value = params[i].strip(b' ').strip(b'\x00')

            if len(value):
                info.append(index_param[i](value))
        return info


def print_file_info(stat, f=sys.stdout):
    max_width = max(map(lambda s: len(s[0]), stat))
    for field in stat:
        print("{{:>{}}} : {{}}".format(max_width).format(*field), file=f)


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] FILE'.format(os.path.basename(sys.argv[0])),
        description='Tar extractor')
    parser.add_argument('-l', '--list', action='store_true', dest='ls',
                        help='list the contents of an archive')
    parser.add_argument('-x', '--extract', action='store_true', dest='extract',
                        help='extract files from an archive')
    parser.add_argument('-i', '--info', action='store_true', dest='info',
                        help='get information about files in an archive')
    parser.add_argument('fn', metavar='FILE',
                        help='name of an archive')

    args = parser.parse_args()

    if not (args.ls or args.extract or args.info):
        sys.exit("Error: action must be specified")

    try:
        tar = TarParser(args.fn)

        if args.info:
            for fn in sorted(tar.files()):
                print_file_info(tar.file_stat(fn))
                print()

        elif args.ls:
            for fn in sorted(tar.files()):
                print(fn)

        if args.extract:
            tar.extract()
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    main()
