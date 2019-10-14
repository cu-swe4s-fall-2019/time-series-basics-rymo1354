# time-series-basics
Time Series basics - importing, cleaning, printing to csv

Note: date files are synthetic data.

## Travis Status
![](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-rymo1354.svg?branch=master)

## Usage
`data_import.py` is the main program used to generate csv files from the csv files in the `smallData` folder. The following is example usage of `data_import.py`: 

```
python3 data_import.py smallData smdg smdg.csv
```

The first argument is the folder used to get the raw data csvs, the second is the name of the final csv, and the third is the csv with data values that are the first column of the final csv (not including the time column.) For this build, time resolutions of 5 and 15 are used to group values based upon time. Grouping occurs as follows:

* `activity_small.csv`: summation 
* `bolus_small.csv`: summation 
* `meal_small.csv`: summation 
* `smbg_small.csv`: summation 
* `hr_small.csv`: average 
* `cgm_small.csv`: average 
* `basal_small.csv`: average  

## Installation
To use this package, you should have [Python3](https://www.python.org/download/releases/3.6/) in your environment. You should also have numpy installed.

## Utilized Packages
* pycodestyle
* python-dateutil
* numpy

All other packages come preinstalled with python 3.6.

## Profiling and Benchmarking (Extra Credit)
Profiling and benchmarking performed using cProfile:
```
python -m cProfile -s time data_import.py smallData smdg smdg.csv
```

* linear_search:
    * tottime: 3.389s
    * cumtime: 3.394s

* binary_search:
    * tottime: 0.339s
    * cumtime: 0.350s

* binary_sort: 
    * tottime: 0.024s
    * cumtime: 0.082s

Even after including pre-sorting, the binary search method is almost 10x faster than the linear search method. 


