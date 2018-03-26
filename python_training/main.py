from python_training.utils import get_engine_and_session, create_tables
from python_training.member import add_member

def main():
    engine, session = get_engine_and_session()
    create_tables(engine)
    add_member(session, 'anya', 'tch', 'dev', 'sygnia')


if __name__ == '__main__':
    main()
