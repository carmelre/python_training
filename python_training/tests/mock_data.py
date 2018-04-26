from python_training.interface import Entry
import datetime as dt

MOCK_DATA_BASE = [['1.1.1.1', 'TCP', dt.datetime(2016, 1, 1)],
                  ['1.1.1.1', 'HTTP', dt.datetime(2017, 1, 1)],
                  ['1.1.1.1', 'HTTP', dt.datetime(2017, 2, 1)],
                  ['2.2.2.2', 'HTTP', dt.datetime(2017, 2, 2)]]

MOCK_DATA_SET = [Entry(*data) for data in MOCK_DATA_BASE]
