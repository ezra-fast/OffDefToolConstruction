# Filename: m3p2.py
# Author: Ezra Fast
# Course: ITSC-203, Scripting for Tool Construction
# Details: This script is the solution for Lab 3b, problem 1, ITSC-203; It deals with the Linux file system programmatically.

import os 
import datetime
import prettytable
from datetime import datetime

def usageWarning():                                 # usage warning function
    print('This code must be run in the folder that contains the directory to be analyzed!')

def formatProvider():                               # format function
    print('-'*86)

def directorySolicitor():                           # soliciting the name of the directory to analyze
    formatProvider()
    usageWarning()
    directoryPath = ''
    while not os.path.exists(directoryPath):
        directoryPath = input('Enter the name of a directory to analyze: ')
        if os.path.exists(directoryPath):
            break
        else:
            print("Enter the name of a valid directory and ensure you are in the directory that contains it.")
    return directoryPath

def initialPrintDir(directoryPath):                 # printing the directory structure in columns
    formatProvider()
    table = prettytable.PrettyTable()
    dictOfSubDirs = {}
    listOfSubDirs = []
    for dir in os.listdir(directoryPath):
        dictOfSubDirs[dir] = []
        listOfSubDirs.append(dir)
    for direct in listOfSubDirs:
        # print(listOfSubDirs)
        currentDir = os.getcwd()
        for file in os.listdir(f'{currentDir}/{directoryPath}/{direct}'):
            # print(f'{direct}: {file}')
            dictOfSubDirs[direct].append(file)
    for subDir in dictOfSubDirs:
        table.add_column(subDir, dictOfSubDirs[subDir])
    print(table)

def dateRangeSolicitor():                           # soliciting the date range to apply to the directory
    formatProvider()
    try:
        dateRange = input('Enter the file date range YYYY/MM/DD - YYYY/MM/DD to filter for: ')
    except:
        print('User error.\nExiting...')
    return dateRange

def dateStringsExtractor(dateRange):                # extracting the datetime objects from the input string
    try:
        dates = dateRange.split(' - ')
        date1 = datetime.strptime(dates[0], "%Y/%m/%d")
        date2 = datetime.strptime(dates[1], "%Y/%m/%d")
        datesUpdated = []
        datesUpdated.append(date1)
        datesUpdated.append(date2)
        return datesUpdated
    except Exception as reason:                     # simple error handling
        print(f"Error Message: {reason}\nExiting...")
        exit(-1)

def beforeAndAfter(earlyDate, laterDate, directoryPath):            # this is the meat and potatoes of the program
    try:                                                            # printing the files that come before and after the given date range
        formatProvider()
        withinRange = []
        outsideRange = []
        for dir in os.listdir(directoryPath):
            for file in os.listdir(f'{directoryPath}/{dir}'):
                fullPath = f"{directoryPath}/{dir}/{file}"
                fileTime = os.path.getmtime(fullPath)               # Returning the MODIFIED date of the file, as per the requirements
                fileTime = datetime.fromtimestamp(fileTime)
                if fileTime >= earlyDate and fileTime <= laterDate:
                    # print(f'Within Range: {file} Date: {fileTime.strftime("%b %d, %Y - %H:%M:%S")}')
                    withinRange.append(f"{directoryPath}/{dir}/{file}")
                    withinRange.append(f'Date: {fileTime.strftime("%b %d, %Y - %H:%M:%S")}')
                else:
                    # print(f'Outside of Range: {file}')
                    outsideRange.append(f"{directoryPath}/{dir}/{file}")
                    outsideRange.append(f'Date: {fileTime.strftime("%b %d, %Y - %H:%M:%S")}')
        # print(f"{'-'*5}Within Date Range{'-'*5}")
        print('Files that meet the date criteria:\n')
        for i in range(0, len(withinRange), 2):
            print(f"{withinRange[i]}\t\t{withinRange[i + 1]}")
        # print(f"{'-'*5}Outside Date Range{'-'*5}")
        formatProvider()
        print("Files that don't meet the date criteria:\n")
        for i in range(0, len(outsideRange), 2):
            print(f"{outsideRange[i]}\t\t{outsideRange[i + 1]}")
        formatProvider()
    except Exception as reason:
        print(f"Error Message: {reason}\nExiting...")
        exit(-2)

if __name__ == "__main__":                                          # This is the main function
    directoryPath = directorySolicitor()
    initialPrintDir(directoryPath)
    dateRange = dateRangeSolicitor()
    dates = dateStringsExtractor(dateRange)
    earlyDate = dates[0]
    laterDate = dates[1]
    beforeAndAfter(earlyDate, laterDate, directoryPath)
    exit(0)
