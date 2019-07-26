#!/usr/bin/env python3
import sys
import csv
import datetime
import pandas

# Could run this project under the title Themis, titaness of divine law and order
# Symbol is Bronze sword
# TODO: Add move feature for entries
# TODO: Add proper logging
# TODO: Devise good success codes and feedback for web service compatibility

DATABASE_FILE = "db.csv"

READ_FILE = "read.csv"
READING_FILE = "reading.csv"
TO_READ_FILE = "to_read.csv"

READ = "read"
READING = "reading"
TO_READ = "to_read"

TITLE = "TITLE"
AUTHOR = "AUTHOR"
INFO = "INFO"

ADD = "add"
FIND = "find"
MOVE = "move"

def test(arg):
    print("Hello " + arg)

# Find the list of partial matches, with an optional category given.
def find(query, category=TITLE):
    db = open_db()
    # TODO: Ensure category matches one of the available ones.


    # Matches all entries in category.
    # case=False makes matches case insensitive.
    results = db.loc[db[category].str.contains(query, case=False)]
    print(db.filter(like=query))
    return(results)


def map_category(category):
    if (category == TITLE):
        return 0
    elif (category == AUTHOR):
        return 1
    elif (category == INFO):
        return 2
    else:
        print(category + " not supported. Will match title instead.")
        return 0

def add(state, title, author, info, rating=5):

    db = open_db()
    # Add entry to db if not already existing

    # When writing, simply add line with all content to CSV

    # Check for matching (case insensitive) 
    # - title
    # - author
    # Info and rating do not matter.

    # Matches all entries in category.
    # case=False makes matches case insensitive.
    results = db.loc[db[TITLE].str.upper().equals(title)]
    print(results)
    return(results)



def open_db():
    # TODO: Find way to keep changes in sync without re-loading file every time.
    database = pandas.read_csv(DATABASE_FILE)
    # print(database)        
    return database

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        method = sys.argv[1]
        if (method == FIND):
            if (len(sys.argv) == 2):
                print("No title for search specified.")
            elif (len(sys.argv) == 3):
                print("Find title=" + sys.argv[2] + " in database.")
                print(find(sys.argv[2]))
            else:
                print("Find " + sys.argv[3] + "=" + sys.argv[2] + " in database.")
                print(find(sys.argv[2], sys.argv[3]))
            # initiate find method
        elif (method == ADD):
            print("Add method.")
            if (len(sys.argv) < 6):
                print("Not enough parameters specified. Need file, title, author, info (,rating)")
            elif (len(sys.argv) == 6):
                add(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            else:
                add(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
            # initiate add method
        elif (method == MOVE):
            print("Move method")
            # initiate move method
        elif (method == "open_db"):
            print("Open Database")
            open_db()
        else:
            # No method matched. Issue response of failure.
            print("Method name did not match any entry.")
            print("Please refer to readme for the correct syntax.")
    
    else:
        print("Please specify a method name.")