from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
GEN_HP_AMOUNT = int(config.get('hp_generate', 'amount'))
GEN_HP_INTERVAL = int(config.get('hp_generate', 'interval'))
