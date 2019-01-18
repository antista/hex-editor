# -*- coding: utf-8 -*-
import argparse
import strings


class Redactor():
    def __init__(self, filename, new_file, max_count_of_strings):
        self.filename = filename
        self.finished = False
        self.max_count_of_strings = max_count_of_strings
        self.offset = 1
        self.new_file = new_file

    def start(self):
        if self.new_file:
            f = open(self.filename, 'w')
            text = input('Input text of file in utf8: ')
            f.write(text)
            print('File saved.')
            f.close()
            return
        self.file = open(self.filename, 'r')
        self.byte_file = open(self.filename, 'rb')
        self.read_file()
        import keyboard
        keyboard.add_hotkey('right', self.read_file)
        while not self.finished:
            try:
                if keyboard.is_pressed('q'):
                    break
                else:
                    pass
            except:
                break

    def read_file(self):
        self.tmp = self.byte_file.read(8 * self.max_count_of_strings)
        if self.tmp == b'':
            print('File is over.')
            self.finished = True
            return
        import struct

        for i in range(0, self.max_count_of_strings):
            tmp = str(hex(self.offset - 1))[2:]
            res = '0' * (8 - len(tmp) % 8) + tmp + '    '
            self.offset += 8
            s = self.tmp[8 * i:i * 8 + 8]
            if len(s) == 0:
                self.finished = True
                print('File is over.')
                return
            for c in s:
                c = str(hex(c))[2:]
                if len(c) == 1:
                    res += '0' + c
                else:
                    res += c
                res += '  '
            if len(s) < 8:
                res += '    ' * (8 - len(s) % 8)
            res += '     '
            for c in s:
                if struct.pack('B', c) == b'\xc4' or struct.pack('B', c) == b'\x0e' \
                        or struct.pack('B', c) == b'\x00':
                    res += '..'
                    continue
                try:
                    t = struct.pack('B', c).decode('utf8')
                except:
                    res += '..'
                    continue
                if t != '\n' and t != '\t':
                    res += t
                res += ' '
            print(res)
        print('\nPress arrow right to continue read file or Q to exit.\n')


def parse_args():
    '''Парсер аргументов командной строки'''
    parser = argparse.ArgumentParser(description='Hex-редактор.')
    parser.add_argument('filename', help=strings.FILENAME)
    parser.add_argument('-m', '--max_strings', help=strings.MAX_STRINGS,
                        type=int, default=10)
    parser.add_argument('-n', '--new_file', action='store_const',
                        const=True, default=False, help=strings.NEW_FILE)
    return parser


def main():
    parser = parse_args()
    args = parser.parse_args()
    print(args)
    b = Redactor(filename=args.filename, new_file=args.new_file, max_count_of_strings=args.max_strings)
    b.start()

# ToDo Консольный интерфейс
# Возможность создания файла
# Чтение  -------------------------------------------------- done
# Cохранение файлов
# Не читать файл в память целиком -------------------------- done
# Стандартный интерфейс: смещение, ------------------------- done
# 16 колонок с HEX-значениями, ----------------------------- done
# 16 колонок символьного представления --------------------- done
# Редактирование как HEX-значений, так и символов
# Вставка и удаление данных
if __name__ == "__main__":
    main()
