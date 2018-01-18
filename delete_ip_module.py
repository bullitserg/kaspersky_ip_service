# модуль удаления адресов из сервиса Касперского
import logger_module
import functions


def delete_ip_worker():
    # импортируем переменные из config_parser внутри функции, поскольку они необходимы нам в vars()
    from config_parser import delete_login_time, delete_trade_time  # не удалять!
    logger = logger_module.logger()

    def ip_deleter(iter_data, delete_type):
        status, error = functions.delete_ip_from_white(iter_data)

        if status:
            logger.info('Удалены из белого списка адреса (%s): %s' % (delete_type,
                                                                      functions.convert_iter_to_str(iter_data)))
        else:
            logger.critical('Удаление адресов из белого списка завершилось с ошибкой (%s): %s: %s' % (delete_type,
                                                                                                      status,
                                                                                                      error))

    try:
        logger.info('Инициализация')

        # удаляются только активные 'login' записи старше deleteLoginTime,
        # которые не добавлялись как 'login' позже и отсутствуют в 'trade', 'static'
        kaspersky_delete_login_ip_list = functions.get_kaspersky_delete_login_ip(locals())

        # если найдены данные
        # УДАЛЯЕМ ДАННЫЕ ИЗ БЕЛОГО СПИСКА
        if kaspersky_delete_login_ip_list:
            ip_deleter(kaspersky_delete_login_ip_list, 'login')

        # Из бд устаревшие записи в любом случае удаляем
        functions.delete_login_ip(locals())
        logger.info('Записи удалены из БД (login)')

        # удаляются только активные 'trade' записи старше deleteTradeTime,
        # которые 'login', 'static'

        kaspersky_delete_trade_ip_list = functions.get_kaspersky_delete_trade_ip(locals())

        # если найдены данные, то удаляем их из белого списка
        if kaspersky_delete_trade_ip_list:
            ip_deleter(kaspersky_delete_trade_ip_list, 'trade')

        # Из бд устаревшие записи в любом случае удаляем
        functions.delete_trade_ip(locals())
        logger.info('Записи удалены из БД (trade)')

        # Ищем адреса, помеченные для удаления вручную
        ip_for_delete_list = functions.get_hand_setted_for_delete()

        if ip_for_delete_list:
            # УДАЛЯЕМ АДРЕСА ИЗ БЕЛОГО СПИСКА
            ip_deleter(ip_for_delete_list, 'handle')

            # удаляем адреса из БД
            functions.delete_hand_setted_ip('"' + '","'.join(ip_for_delete_list) + '"')
            logger.info('Записи удалены из БД: %s' % functions.convert_iter_to_str(ip_for_delete_list))

    except Exception as e:
        logger.fatal('Fatal error! Exit', exc_info=True)
        print('Critical error: %s' % e)
        print('More information in log file')
        exit(1)
