# модуль для сбора адресов по торгам на следующий день
import logger_module
import functions


def trade_ip_worker():
    logger = logger_module.logger()

    try:
        # получаем множество адресов по торгам за следующий день
        add_ip_list = functions.get_trade_ip()

        # если адреса нашлись, то обрабатываем их
        if add_ip_list:
            # добавляем эти адреса в БД
            functions.add_ip(add_ip_list, 'trade')
            logger.info('Добавлены в БД адреса: %s' % functions.convert_iter_to_str(add_ip_list))

        else:
            logger.info('Адреса для добавления отсутствуют')

    except Exception as e:
        logger.fatal('Fatal error! Exit', exc_info=True)
        print('Critical error: %s' % e)
        print('More information in log file')
        exit(1)
