from python_training.utils import get_engine_and_session, create_tables


def main():
    engine, session = get_engine_and_session()
    create_tables(engine)


if __name__ == '__main__':
    main()
