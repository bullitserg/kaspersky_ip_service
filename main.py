import argparse
from send_ip_module import send_ip_worker
from trade_ip_module import trade_ip_worker
from login_ip_module import login_ip_worker
from delete_ip_module import delete_ip_worker


PROGNAME = 'Kaspersky IP Service'
DESCRIPTION = '''Сервис для online-работы листами Касперского'''
VERSION = '1.1'
AUTHOR = 'Belim S.'
RELEASE_DATE = '2018-01-17'


def show_version():
    print('\n', PROGNAME, '\n', VERSION, '\n', DESCRIPTION, '\nAuthor:', AUTHOR, '\nRelease date:', RELEASE_DATE, '\n')


# обработчик параметров командной строки
def create_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-v', '--version', action='store_true',
                        help="Show version")

    parser.add_argument('-s', '--send', action='store_true',
                        help="Start as ip sender process (daemon mode)")

    parser.add_argument('-l', '--login', action='store_true',
                        help="Start as login ip get process (daemon mode)")

    parser.add_argument('-t', '--trade', action='store_true',
                        help="Start as trade ip get process")

    parser.add_argument('-d', '--delete', action='store_true',
                        help="Start as delete ip process")

    return parser


def main_function():
    # парсим аргументы командной строки
    parser = create_parser()
    namespace = parser.parse_args()

    # вывод версии
    if namespace.version:
        show_version()
        exit(0)

    # режим отправки ip
    elif namespace.send:
        send_ip_worker()
        exit(0)

    # режим сбора ip при логине
    elif namespace.login:
        login_ip_worker()
        exit(0)

    # режим сбора ip по торгам
    elif namespace.trade:
        trade_ip_worker()
        exit(0)

    # режим удаления адресов
    elif namespace.delete:
        delete_ip_worker()
        exit(0)

    # режим удаления адресов
    else:
        show_version()
        print('For more information run use --help')
        exit(0)


# ОСНОВНОЙ КОД
if __name__ == '__main__':
    main_function()
