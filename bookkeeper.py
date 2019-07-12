#!/usr/bin/env python
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

TITLE = "title"
AUTHOR = "author"
INFO = "info"

ADD = "add"
FIND = "find"
MOVE = "move"

def test(arg):
    print("Hello " + arg)

# Find by title in any of the lists of files
def find(query, category="title"):
    query = query.lower() # make lowercase for better comparison
    category = category.lower()
    result = []
    result.extend(find_in_file(READ_FILE, query, category))
    result.extend(find_in_file(READING_FILE, query, category))
    result.extend(find_in_file(TO_READ_FILE, query, category))
    return(result)


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

def find_in_file(file, query, category):
    result = []

    array_index = map_category(category)

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (line_count > 0):
                entry_content = row[array_index].lower()
                # TODO: Find way to match more widely then just total string.
                if (entry_content == query):
                    result_row = row[:]
                    result_row.append(file)
                    result_row.append(line_count)
                    result.append(result_row)
            line_count += 1
    return(result)

def add(file, title, author, info, rating=5):
    found = False
    existing_titles = find(title)
    if (find(title) != []):
        for entry in find(title):
            if (entry[1] == author):
                found = True

    if (found):
        print("Entry already exists.")
    else:
        if (file == READ):
            print("Add to read")
            with open(READ_FILE, 'a') as f:
                f.write(title+","+author+","+info+","+str(datetime.datetime.now().year)+"\n")
        elif (file == READING):
            print("Add to reading")
            with open(READING_FILE, 'a') as f:
                f.write(title+","+author+","+info+"\n")
        elif (file == TO_READ):
            print("Add to to_read")
            with open(TO_READ_FILE, 'a') as f:
                f.write(title+","+author+","+info+","+rating+"\n")
        else:
            print(file + " not supported as list.")

def open_db():
    database = pandas.read_csv(DATABASE_FILE)
    print(database)        
    

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