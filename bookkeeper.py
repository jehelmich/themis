#!/usr/bin/env python3

# Imports for core functionality
import sys
import csv
import datetime
import pandas

# Imports for logging
import logging

# Config for logging
logging.basicConfig(
    filename='bookkeeper.log',
    filemode='a',
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s', 
    datefmt='%d/%m/%Y %H:%M:%S')
# Set Logging level to debug. Default is warning
logging.getLogger().setLevel(logging.DEBUG)

# Could run this project under the title Themis, titaness of divine law and order
# Symbol is Bronze sword
# TODO: Add move feature for entries (theoretically requires way to index)
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

SHAPE_ROW_COUNT_INDEX = 0

# Find the list of partial matches, with an optional category given.
def find(query, category=TITLE):
    logging.info("Find method launched")
    db = open_db()
    # TODO: Ensure category matches one of the available ones.


    # Matches all entries in category.
    # case=False makes matches case insensitive.
    logging.info("Loading matching results for category " + category + " with query " + query)
    results = db.loc[db[category].str.contains(query, case=False)]
    logging.info("Results loaded.")
    logging.info(results)
    
    return(results)


def add(state, title, author, info, rating=5):
    logging.info("Add method launched")
    db = open_db()

    # Add entry to db if not already existing

    # When writing, simply add line with all content to CSV

    # Check for matching (case insensitive) 
    # - title
    # - author
    # Info and rating do not matter.

    # Matches all entries in category.
    # lower() works, would rather use casefold, though does not work.
    logging.info("Finding matches for title " + title + " and author " + author)
    matches = db[(db[TITLE].str.lower() == title.lower())&(db[AUTHOR].str.lower() == author.lower())]
    logging.info("Matches loaded.")
    logging.info(matches)
    match_count = matches.shape[SHAPE_ROW_COUNT_INDEX]

    if (match_count <= 0):
        logging.info("No matches found.")
        logging.info("Proceed to add content to Database")
        db_line = [title, author, info, rating, "", state]
        logging.info("Line content is " + str(db_line))
        add_to_db(db_line)
        logging.info("Content added to Database")
        print("Content added to Database")
    else:
        logging.info("Matching entries found")
        logging.info("Not proceeding to add content")
        print("Matching entries found")
        print("Not proceeding to add content")
        print("Matches found:")
        print(matches)


# Adds a given array line to the database.
# Currently simply uses the size and content of the provided array
# and adds it to the CSV file.
def add_to_db(content):
    logging.info("Begin writing to Database.")
    logging.info("Content to write:")
    logging.info(content)
    # TODO: Refactor to using dictionaries to avoid confusion with database in the future
    with open(DATABASE_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(content)
    logging.info("Writing to Database successfull.")

def open_db():
    # TODO: Find way to keep changes in sync without re-loading file every time.
    logging.info("Begin loading Database.")
    database = pandas.read_csv(DATABASE_FILE)
    logging.info("Loading Database successfull.")
    # print(database)        
    return database

if __name__ == '__main__':
    logging.info("Bookkeeper started.")
    logging.info("Number of arguments: " + str(len(sys.argv)))
    logging.info("Arguments are: ")
    logging.info(sys.argv)

    if (len(sys.argv) > 1):
        method = sys.argv[1]
        if (method == FIND):
            logging.info("Selected method FIND")
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
            logging.info("Selected method ADD")
            print("Add method.")
            if (len(sys.argv) < 6):
                print("Not enough parameters specified. Need file, title, author, info (,rating)")
            elif (len(sys.argv) == 6):
                add(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            else:
                add(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
            # initiate add method
        elif (method == MOVE):
            logging.info("Selected method MOVE")
            print("Move method")
            # initiate move method
        else:
            # No method matched. Issue response of failure.
            logging.info("Method " + method + " did not match.")
            logging.info("Issue user response.")
            print("Method name did not match any entry.")
            print("Please refer to readme for the correct syntax.")
    
    else:
        logging.info("No method parameter specified.")
        print("Please specify a method name.")