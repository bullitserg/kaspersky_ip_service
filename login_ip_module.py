# модуль сбора сведений о недавно залогиненных пользователях
import logger_module
import functions
import time


def login_ip_worker():
    # импортируем переменные из config_parser внутри функции, поскольку они необходимы нам в vars()
    from config_parser import login_sleep_time, bot_check_time, bot_authorization_limit
    logger = logger_module.logger()
    try:
        logger.info('Инициализация')
        while True:
            # получаем текущий actualMaxId
            actual_max_id = functions.get_max_id()
            # если last_max_id еще не определен, то определяем его
            if 'last_max_id' not in vars():
                # используем актуальный
                last_max_id = actual_max_id
                add_ip_set = set()
            else:
                add_ip_set = functions.get_ip(vars())
            # если найдены данные
            if add_ip_set:
                bot_ip_set = functions.get_bot_ip(vars())
                # если обнаружены боты, то убираем их адреса из add_ip_set
                if bot_ip_set:
                    add_ip_set = add_ip_set.difference(bot_ip_set)
                    logger.info('Проигнорированы боты: %s' % functions.convert_iter_to_str(bot_ip_set))
                # если после удаления ботов остались адреса
                if add_ip_set:
                    functions.add_ip(add_ip_set, 'login')
                    logger.info('Добавлены в БД адреса: %s' % functions.convert_iter_to_str(add_ip_set))

            last_max_id = actual_max_id
            time.sleep(login_sleep_time)

    except Exception as e:
        logger.fatal('Fatal error! Exit', exc_info=True)
        print('Critical error: %s' % e)
        print('More information in log file')
        exit(1)
