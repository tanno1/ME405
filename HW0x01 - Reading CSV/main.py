"""
@file                                   main.py
@author                                 noah tanner
@assignment                             hw0x01 - reading csv files and using matplotlib
@brief                                  this is the main script for my python application for hw0x01, this script will plot data from a csv file on a graph and includes proper error handling to accomodate different data points and whitespace or other errors that may be encountered in a csv file
@section dependencies Dependencies
                                        This script relies on the following python libraries:
                                            - 'matplotlib': for plotting data from the csv file
"""

# imports
from matplotlib import pyplot as plt
import csv

if __name__ == '__main__':

    # list for valid data to plot
    x_data = []
    y_data = []

    with open('data.csv', 'r') as file:
        # read csv file
        csv_read = csv.reader(file)
        # take header row and add as axis labels
        header_row = next(csv_read)
        xlabel = header_row[0]
        ylabel = header_row[1]
        
        # iterate through rows and add data to x or y data list
        for row in csv_read:
            # check through only non-empty row
            if not row:
                continue
            try:
                x_data.append(float(row[0].split('#')[0].strip()))          # the .split() and .strip() methods I learned about from https://www.freecodecamp.org/news/the-string-strip-method-in-python-explained/
                y_data.append(float(row[1].split('#')[0].strip()))
            except ( ValueError, IndexError ):
                continue
    
    # create and plot data
    plt.plot(x_data, y_data)

    # add x and y axis labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # uncomment to print to terminal to visually check data
    #for x, y in zip(x_data, y_data):
        #print(x, y)

    # display plot
    plt.show()




