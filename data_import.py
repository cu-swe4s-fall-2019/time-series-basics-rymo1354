import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import copy
import numpy as np


class ImportData:
    """Reads in data from data_csv and changes it by:

        - Swapping low and high values for 40 and 300
        - Bypasses non-numerical value entries

    Attributes:
        _time: array of times read in from .csv file
        _value: array of values read in from .csv file
        _type: same time conglomeration method; sum and average supported
    """

    def __init__(self, data_csv):
        """Initializes ImportData by reading in from data_csv"""
        self._time = []
        self._value = []
        self._type = 'average'

        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._type = 'sum'

        with open(data_csv, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['time'] == '':
                    continue
                else:
                    try:
                        tm = dateutil.parser.parse(row['time'])
                        if row['value'] == 'low':
                            print('Low to 40')
                            val = 40
                        elif row['value'] == 'high':
                            print('High to 300')
                            val = 300
                        else:
                            val = float(row['value'])
                        self._time.append(tm)
                        self._value.append(val)
                    except ValueError:
                        print('Invalid value ' + row['value'])

        return

    def linear_search_value(self, key_time):
        """
        linearly searches self._time based on provided key
        Arguments
        _________
        key_time : datetime object
            datetime object to search array for
        Returns
        _______
        i : integer
            index of key_time or -1 if not in array
        """

        for i in range(len(self._time)):
            curr = self._time[i]
            if key_time == curr:
                return i

        # print('invalid time')
        return -1

    def binary_sort(self):
        """
        sort lists in order to perform binary search
        Arguments
        _________
        Returns
        _______
        """

        times = self._time.copy()
        values = self._value.copy()
        zipped = zip(times, values)
        zipped_sort = sorted(zipped)

        times_tup, values_tup = zip(*zipped_sort)
        times_sorted = list(times_tup)
        values_sorted = list(values_tup)

        self._time = times_sorted
        self._value = values_sorted

        return

    def binary_search_value(self, key_time):
        """
        binary search of self._time based on provided key
        Arguments
        _________
        key_time : datetime object
            datetime object to search array for
        Returns
        _______
        i : integer
            index of key_time or -1 if not in array
        """

        # values must be sorted before this can work

        lo = -1
        hi = len(self._time)

        while (hi - lo > 1):
            mid = (hi + lo) // 2

            if key_time == self._time[mid]:
                return mid

            if key_time < self._time[mid]:
                hi = mid
            else:
                lo = mid

        # print('invalid time')
        return -1


def roundTimeArray(obj, resolution):
    """
    grouping of times based upon a resolution factor
    Arguments
    _________
    obj : ImportData object
        times taken from this object
    resolution : integer
        minute resolution of the time grouping
    Returns
    _______
    zipped object of the grouped times and values
        resolved times and associated values grouped this way
    """

    time_rounded_obj = copy.deepcopy(obj)
    rounded_times = []
    unique_rounded_times = []

    for time in time_rounded_obj._time:
        minminus = datetime.timedelta(minutes=(time.minute % resolution))
        minplus = datetime.timedelta(minutes=resolution) - minminus
        if (time.minute % resolution) <= (resolution/2):
            newtime = time - minminus
            if newtime not in rounded_times:
                unique_rounded_times.append(newtime)
            rounded_times.append(newtime)

        else:
            newtime = time + minplus
            if newtime not in rounded_times:
                unique_rounded_times.append(newtime)
            rounded_times.append(newtime)

    time_rounded_obj._time = rounded_times

    sorted_values = [[] for i in range(len(unique_rounded_times))]

    '''
    ###
    # linear search

    for unique_idx in range(len(unique_rounded_times)):
        value_idx = None
        time_rounded_obj._time = rounded_times
        time_rounded_obj._value = obj._value

        while value_idx != -1:
            if value_idx != None:
                value = time_rounded_obj._value.pop(value_idx)
                sorted_values[unique_idx].append(value)
                time_rounded_obj._time.pop(value_idx)
            value_idx = time_rounded_obj.linear_search_value(
                        unique_rounded_times[unique_idx])
    ###
    '''
    ###
    # binary search

    time_rounded_obj.binary_sort()
    sorted_rounded_times = time_rounded_obj._time
    sorted_rounded_values = time_rounded_obj._value

    for unique_idx in range(len(unique_rounded_times)):
        value_idx = None
        time_rounded_obj._time = sorted_rounded_times
        time_rounded_obj._value = sorted_rounded_values

        while value_idx != -1:
            if value_idx is not None:
                value = time_rounded_obj._value.pop(value_idx)
                sorted_values[unique_idx].append(value)
                time_rounded_obj._time.pop(value_idx)
            value_idx = time_rounded_obj.binary_search_value(
                        unique_rounded_times[unique_idx])
    ###

    final_values = []
    if time_rounded_obj._type == 'average':
        for idx in range(len(sorted_values)):
            final_values.append(np.mean(sorted_values[idx]))
    if time_rounded_obj._type == 'sum':
        for idx in range(len(sorted_values)):
            final_values.append(np.sum(sorted_values[idx]))

    return zip(unique_rounded_times, final_values)


def printArray(data_list, annotation_list, base_name, key_file):
    """
    write data from csvs to file, with key as the first column
    saves a new csv file to the present working directory
    Arguments
    _________
    data_list : list of ImportData objects
    annotation_list : list of the column titles
    base_name : base name of the saved csv file
    key_file : the first column of the written csv file
    Returns
    _______
    """
    data_key = []
    data_rest = []
    annotation_key = []
    annotation_rest = []

    # combine and print on the key_file
    if not (key_file in annotation_list):
        print('Cannot find sort_key')
        sys.exit(1)

    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                annotation_key.append(annotation_list[i])
                data_key.append(data_list[i])
            else:
                annotation_rest.append(annotation_list[i])
                data_rest.append(data_list[i])

    key_times = []
    key_values = []
    for tk, vk in data_key[0]:
        key_times.append(tk)
        key_values.append(vk)

    write_array = [[] for i in range(len(key_times))]
    for i in range(len(key_times)):
        write_array[i].append(key_times[i])
        write_array[i].append(key_values[i])

    for data in data_rest:
        rest_times = []
        rest_values = []
        for tr, vr in data:
            rest_times.append(tr)
            rest_values.append(vr)
        for i in range(len(key_times)):
            if key_times[i] in rest_times:
                idx = rest_times.index(key_times[i])
                write_array[i].append(rest_values[idx])
            else:
                write_array[i].append(0)

    attributes = ['time'] + annotation_key + annotation_rest

    with open(base_name + '.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(attributes)
        writer.writerows(write_array)

    return


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import, combine, \
                                     and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str, help='Name of the folder')

    parser.add_argument('output_file', type=str, help='Name of Output file')

    parser.add_argument('sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int, help="Number of Files",
                        required=False)

    args = parser.parse_args()

    # pull all the folders in the file
    try:
        files_lst = listdir(args.folder_name)
    except (FileNotFoundError, NameError) as e:
        print('Folder not found', file=sys.stderr)
        sys.exit(1)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for file in files_lst:
        data_lst.append(ImportData(join(args.folder_name, file)))

    if len(data_lst) == 0:
        print('No files in folder', file=sys.stderr)
        sys.exit(1)

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []
    for data_obj in data_lst:
        data_5.append(roundTimeArray(data_obj, 5))

    data_15 = []
    for data_obj in data_lst:
        data_15.append(roundTimeArray(data_obj, 15))

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
