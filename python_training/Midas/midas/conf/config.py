import pkg_resources

DB_FILE = pkg_resources.resource_filename('midas', 'db/midas.db')

OPERATIONAL_DB = f'sqlite:///{DB_FILE}'
