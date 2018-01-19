# модуль инициации логгера
import inspect
import logging
import ets.ets_log_preformat_lib as l_p
from config_parser import log_file

# описываем формат лога
logging.basicConfig(format=l_p.LOG_FORMAT_1,
                    datefmt=l_p.DATE_FORMAT_4,
                    level=logging.INFO,
                    filename=log_file)


# описываем функцию, которая будет возвращать логгер с нужным именем
# (названием главной функции, в которой произошло событие)
def logger():
    return logging.getLogger(str(inspect.stack()[1][3]).ljust(17, ' '))
