from datetime import datetime

OPERATIONAL_DB_FILE_NAME = 'midas.db'

OPERATIONAL_DB = f'sqlite:///{OPERATIONAL_DB_FILE_NAME}'

MEMBERS_INFO = [{'first_name': 'carmel', 'last_name': 'reubinoff', 'role': 'dev', 'location': 'Tozeret Haaretz'},
                {'first_name': 'Anya', 'last_name': 'tch', 'role': 'dev', 'location': 'Zikim'},
                {'first_name': 'Alon', 'last_name': 'Shenkler', 'role': 'dev', 'location': 'Tozeret Haaretz'}]
ORGANIZATIONS_INFO = [{'name': 'Sygnia', 'prime_location': 'Tozeret Haaretz'},
                      {'name': 'Claroty', 'prime_location': 'Tozeret Haaretz'}]
EVENTS_INFO = [{'date': datetime.now(), 'location': 'Mizpe Hayamim'},
               {'date': datetime.now(), 'location': 'Zappa Herzliya'}]
