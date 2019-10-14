#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle data_import.py
assert_no_stdout
run test_style pycodestyle test_data_import.py
assert_no_stdout

run bad_sort_key python data_import.py smallData bad_attempt bad
assert_stdout
assert_exit_code 1

run bad_folder python data_import.py bad bad_attempt smbg_small
assert_no_stdout
assert_exit_code 1

run basic_test python data_import.py smallData smdg_test smbg_small.csv
assert_stdout
assert_exit_code 0
rm smdg_test_5.csv
rm smdg_test_15.csv
