from ets.ets_kaspersky_api_lib import KasperskyWorker
from ets.ets_mysql_lib import MysqlConnection as MyConn
from queries import *

# создаем подключение к бд логов
log_connection = MyConn(connection=MyConn.MS_44_LOG_CONNECT)
# создаем подключение к бд касперского
kaspersky_connection = MyConn(connection=MyConn.MS_KASPERSKY_CONNECT)
# создаем подключение к бд sectionks
sectionks_connection = MyConn(connection=MyConn.MS_44_2_CONNECT)


# login_ip_module
def get_max_id():
    with log_connection.open():
        return log_connection.execute_query(max_id_query)[0][0]


def get_ip(dictionary):
    with log_connection.open():
        data = log_connection.execute_query(get_ip_query % dictionary)
    return set(ip[0] for ip in data)


def get_bot_ip(dictionary):
    with log_connection.open():
        data = log_connection.execute_query(get_bot_ip_query % dictionary)
    return set(bot[0] for bot in data)


def add_ip(ip_set, add_type):
    kaspersky_connection.connect()
    for ip in ip_set:
        kaspersky_connection.execute_query(add_ip_query, ip, add_type)
    kaspersky_connection.disconnect()


# send_ip_module
def get_ip_id_for_send():
    with kaspersky_connection.open():
        data = kaspersky_connection.execute_query(get_ip_for_send_query)
    return [str(ip_id[0]) for ip_id in data], [str(ip[1]) for ip in data]


def sended_ip_setting(id_for_send_list):
    sended_ip_id_str = ', '.join(id_for_send_list)
    with kaspersky_connection.open():
        kaspersky_connection.execute_query(sended_ip_setting_query % sended_ip_id_str)


# функция отправки пакетов для добавления в белый список
def add_ip_to_white(ip_list):
    kaspersky_sender = KasperskyWorker()
    # return kaspersky_sender.add_ip_list(ip_list, list_type='white')
    return True, False

# delete_ip_module
def delete_ip_from_white(ip_list):
    kaspersky_sender = KasperskyWorker()
    # return kaspersky_sender.delete_ip_list(ip_list, list_type='white')
    return True, False


def get_kaspersky_delete_login_ip(dictionary):
    with kaspersky_connection.open():
        data = kaspersky_connection.execute_query(get_kaspersky_delete_login_ip_query % dictionary)
    return [ip[0] for ip in data]


def delete_login_ip(dictionary):
    with kaspersky_connection.open():
        kaspersky_connection.execute_query(delete_login_ip_query % dictionary)


def get_kaspersky_delete_trade_ip(dictionary):
    with kaspersky_connection.open():
        data = kaspersky_connection.execute_query(get_kaspersky_delete_trade_ip_query % dictionary)
    return [ip[0] for ip in data]


def delete_trade_ip(dictionary):
    with kaspersky_connection.open():
        kaspersky_connection.execute_query(delete_trade_ip_query % dictionary)


def get_hand_setted_for_delete():
    with kaspersky_connection.open():
        data = kaspersky_connection.execute_query(get_hand_setted_for_delete_query)
    return [str(ip[0]) for ip in data]


def delete_hand_setted_ip(dictionary):
    with kaspersky_connection.open():
        kaspersky_connection.execute_query(delete_hand_setted_for_delete_query % dictionary)


# trade_ip_module
def get_trade_ip():
    with sectionks_connection.open():
        data = sectionks_connection.execute_query(get_trade_ip_query)
    return [str(ip[0]) for ip in data]


def convert_iter_to_str(iter_data):
    return ', '.join(iter_data)





