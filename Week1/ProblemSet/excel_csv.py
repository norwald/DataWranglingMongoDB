#!/usr/bin/python
# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)

    data.append(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
    time_values = sheet.col_values(0, start_rowx=1, end_rowx=None)
    for col in range(1, sheet.ncols - 1):
        region_name = sheet.cell_value(0, col)
        region_values = sheet.col_values(col, start_rowx=1, end_rowx=None)
        max_value = max(region_values)
        time = time_values[region_values.index(max_value)]
        time_list = xlrd.xldate_as_tuple(time, 0)
        data.append([region_name, time_list[0], time_list[1], time_list[2], time_list[3], max_value])
  
    #print data        
    return data


def save_file(data, filename):
    with open(filename, "wb") as out:
        writer = csv.writer(out, delimiter = "|")
        for row in data:
            writer.writerow(row)

    
def test():
    #open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}
    
    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]

        
test()
