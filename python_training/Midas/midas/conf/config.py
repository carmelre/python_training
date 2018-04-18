from datetime import datetime
import pkg_resources


DB_FILE = pkg_resources.resource_filename('midas', 'db/midas.db')

OPERATIONAL_DB = f'sqlite:///{DB_FILE}'

MEMBERS_INFO = [{'first_name': 'carmel', 'last_name': 'reubinoff', 'role': 'dev', 'location': 'Tozeret Haaretz'},
                {'first_name': 'Anya', 'last_name': 'tch', 'role': 'dev', 'location': 'Zikim'},
                {'first_name': 'Alon', 'last_name': 'Shenkler', 'role': 'dev', 'location': 'Tozeret Haaretz'}]
ORGANIZATIONS_INFO = [{'name': 'Sygnia', 'prime_location': 'Tozeret Haaretz'},
                      {'name': 'Claroty', 'prime_location': 'Tozeret Haaretz'}]
EVENTS_INFO = [{'date': datetime.now(), 'location': 'Mizpe Hayamim'},
               {'date': datetime.now(), 'location': 'Zappa Herzliya'}]
