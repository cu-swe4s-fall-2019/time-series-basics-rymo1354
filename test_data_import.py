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

    def test_low_high_handling(self):
        f = open('low_high.csv', 'w')
        f.write('time,value\n')
        f.write('3/16/19 4:16,low\n')
        f.write('3/16/19 5:23,high')
        f.close()
        obj = data_import.ImportData('low_high.csv')
        self.assertEqual(obj._value[0], 40)
        self.assertEqual(obj._value[1], 300)
        os.remove('low_high.csv')

    def test_round_time(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        rounded = data_import.roundTimeArray(obj, 5)
        for (time, value) in rounded:
            self.assertEqual(value, 254.0)
            d = datetime.datetime(2018, 3, 16, 8, 45)
            self.assertEqual(time, d)
            break


if __name__ == '__main__':
    unittest.main()
