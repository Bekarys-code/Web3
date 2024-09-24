# Made by Bekarys Balaganov
# Section Leader: Tingting Thompson
# Date : 11/09/2024
# ISTA 131 Homework2


import pandas as pd
import numpy as np
import math
import csv
import sqlite3

def is_power_of_2(int1):
    """
    When given an integer as its only input, this Boolean function returns True if the integer is a power of two and False otherwise.
    """
    if int1 < 1:
        return False
    return (int1 & (int1 - 1)) == 0

def all_power_of_2(nm):
    """
    With a numpy matrix as its only input, this Boolean function returns True when every element is a power of two and False otherwise.
      if the argument is empty, returns True.

    """
    for row in nm:
        for item in row:
            if is_power_of_2(item):
                continue
            else:
                return False
    return True

def first_divisible(nmatrix, int1=2):
    """
    The indices of the first element divisible by the second parameter are returned as a list or a 1-D array by this function,
      which accepts a nonempty integer numpy matrix as input and an integer with a default value of 2. 
      Return None if no element can be divided by the number.


    """
    for row in range(len(nmatrix)):
        for elem in range(len(nmatrix[row])):
            if nmatrix[row][elem] % int1 == 0:
                return [row, elem]
    return None

def multiples_of_4(nm):
    """
    This function takes a nonempty numpy matrix as input and outputs a list of all items
      whose indices add up to four multiples of the element count.

    """
    result = []
    for x in range(len(nm)):
        for y in range(len(nm[x])):
            if (x + y) % 4 == 0:
                result.append(nm[x, y])
    return result

def to_array(dic):
    """
    This function accepts a dictionary that associates keys with numerical lists, 
    and it outputs a numpy matrix with the numbers from the lists. Go through the dictionary's keys in a sorted sequence.


    """
    result = []
    keys = dic.keys()
    for key in sorted(keys):
        dic_list = dic.get(key)
        result.append(dic_list)
    return np.array(result)

def to_table(csvFile, sqlFile, tableName='new1'):
    """
    A CSV filename, a SQLite filename, and a table name with the default value "new1" are required for this function to work.
    The data from the CSV file is added to a new table in the database with the given name.
    The column names are in the first row of the CSV file. Every column is of type TEXT.

    The primary key appears in the first column.


    """
    conn = sqlite3.connect(sqlFile)
    c = conn.cursor()

    with open(csvFile) as openFile:
        reader = csv.reader(openFile)
        headerNames = tuple(next(reader))
        
        # Create table with TEXT columns and the first column as the primary key
        create_query = f"CREATE TABLE {tableName} ({', '.join([col + ' TEXT' for col in headerNames])}, PRIMARY KEY ({headerNames[0]}));"
        c.execute(create_query)

        # Insert rows into the table
        insert_query = f"INSERT INTO {tableName} VALUES ({', '.join(['?' for _ in headerNames])});"
        for row in reader:
            c.execute(insert_query, row)

    conn.commit()
    conn.close()

def to_csv(sqlFile, tableName, fileName="data.csv"):
    """
    The parameters for this function are a table name, a SQLite filename, and a CSV filename, with "data.csv" being the default option.
    It writes the information to the CSV file after obtaining it from the table.

    """
    conn = sqlite3.connect(sqlFile)
    c = conn.cursor()
    c.execute(f"SELECT * FROM {tableName}")

    headerNames = [description[0] for description in c.description]
    with open(fileName, "w") as file:
        writer = csv.writer(file)
        writer.writerow(headerNames)  # Write headers
        writer.writerows(c.fetchall())  # Write rows

    conn.close()

def get_students(conn, tableName, grade):
    """
    This function provides a list of all the student names in sorted order who received that grade in that table,
      given a grade, a table name, and a connection object to a student database.
    Names of students should follow the "last, first" format.


    """
    c = conn.cursor()
    query = f'SELECT last, first FROM {tableName} WHERE grade = ? ORDER BY last, first;'
    c.execute(query, (grade,))
    result = [f'{last}, {first}' for last, first in c.fetchall()]
    return result

