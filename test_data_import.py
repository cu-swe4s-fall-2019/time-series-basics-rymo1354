import unittest
import os
import datetime
import data_import


class TestDataImport(unittest.TestCase):
    def test_import_data(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        self.assertEqual(len(obj._time), len(obj._value))

    def test_linear_search_true(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        d = datetime.datetime(2018, 3, 16, 8, 46)
        index = obj.linear_search_value(d)
        self.assertEqual(index, 0)

    def test_linear_search_false(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        d = datetime.datetime(2018, 2, 16, 8, 46)
        index = obj.linear_search_value(d)
        self.assertEqual(index, -1)

    def test_binary_search_true(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        obj.binary_sort()
        d = datetime.datetime(2018, 3, 16, 8, 46)
        index = obj.binary_search_value(d)
        self.assertEqual(index, 0)

    def test_binary_search_false(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        obj.binary_sort()
        d = datetime.datetime(2018, 2, 16, 8, 46)
        index = obj.binary_search_value(d)
        self.assertEqual(index, -1)



if __name__ == '__main__':
    unittest.main()