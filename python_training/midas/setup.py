from setuptools import setup


def main():
    setup(
        name='midas',
        version='0.1',
        description='Finding Stuff',
        packages=['midas'],
        package_dir={'midas': 'midas'},
        package_data={'midas': ['db/*.db']}
    )


if __name__ == '__main__':
    main()