# модуль отправки данных в сервис Касперского
from config_parser import *
import logger_module
import functions
import time


def send_ip_worker():
    logger = logger_module.logger()

    try:
        logger.info('Инициализация')
        while True:
            # получаем id еще не отправленных пакетов
            id_for_send_list, ip_for_send_list = functions.get_ip_id_for_send()

            # если есть что отправить
            if id_for_send_list:
                # ТУТ ОТПРАВЛЯЕМ ПАКЕТЫ!
                status, error = functions.add_ip_to_white(ip_for_send_list)
                if status:
                    logger.info('Добавлены в белый список адреса: %s' % functions.convert_iter_to_str(ip_for_send_list))
                else:
                    logger.critical('Текущая отправка адресов в белый список завершилась ошибкой: %s: %s' % (status,
                                                                                                             error))

                # после отправки помечаем все отправленные записи isSend = 1
                functions.sended_ip_setting(id_for_send_list)

            time.sleep(send_sleep_time)

    except Exception as e:
        logger.fatal('Fatal error! Exit', exc_info=True)
        print('Critical error: %s' % e)
        print('More information in log file')
        exit(1)


