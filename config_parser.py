from ets.ets_small_config_parser import ConfigParser as Parser
from inspect import getsourcefile
from os.path import dirname, normpath
from os import chdir

PATH = normpath(dirname(getsourcefile(lambda: 0)))
chdir(PATH)

CONFIG_FILE = 'kaspersky.conf'


config = Parser(config_file=CONFIG_FILE)

log_file = config.get_option('main', 'log', string=True)

send_sleep_time = config.get_option('send_ip_module', 'sleep_time')

login_sleep_time = config.get_option('login_ip_module', 'sleep_time')
bot_check_time = config.get_option('login_ip_module', 'bot_check_time')
bot_authorization_limit = config.get_option('login_ip_module', 'bot_authorization_limit')


delete_login_time = config.get_option('delete_ip_module', 'delete_login_time')
delete_trade_time = config.get_option('delete_ip_module', 'delete_trade_time')


