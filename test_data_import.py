import unittest
import os
import datetime
import data_import


class TestDataImport(unittest.TestCase):
    def test_import_data(self):
        filename = './smallData/activity_small.csv'
        obj = data_import.ImportData(filename)
        self.assertEqual(len(obj._time), len(obj._value))


if __name__ == '__main__':
    unittest.main()
