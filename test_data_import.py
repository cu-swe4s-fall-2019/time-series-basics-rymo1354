import unittest
import os
import datetime
import data_import
from os.path import join


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

    def test_print_array(self):
        files_lst = os.listdir('./smallData/')
        data_lst = []
        for f in files_lst:
            data_lst.append(data_import.ImportData(join('./smallData/', f)))

        data_5 = []
        for obj in data_lst:
            data_5.append(data_import.roundTimeArray(obj, 5))

        r = data_import.printArray(data_5, files_lst, 'out_5', 'smbg_small.csv')
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')


if __name__ == '__main__':
    unittest.main()
