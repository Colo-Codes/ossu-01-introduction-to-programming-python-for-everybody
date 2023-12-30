# Many Students in Many Courses
# =============================
# Source: https://www.py4e.com/tools/sql-intro/?PHPSESSID=2bfa0957d9a869a029d6d34a79023cfc
#
# Assignment: Many Students in Many Courses
# -----------------------------------------
# 
# This application will read roster data in JSON format, parse the file, and then produce an SQLite database that contains a User, Course, 
# and Member table and populate the tables from the data file.
# 
# You can base your solution on this code: http://www.py4e.com/code3/roster/roster.py - this code is incomplete as you need to modify the 
# program to store the role column in the Member table to complete the assignment.
# 
# Each student gets their own file for the assignment. Download this file and save it as roster_data.json. Move the downloaded file into the 
# same folder as your roster.py program.
# 
# Once you have made the necessary changes to the program and it has been run successfully reading the above JSON data, run the following 
# SQL command:
# 
#       SELECT User.name,Course.title, Member.role FROM 
#           User JOIN Member JOIN Course 
#           ON User.id = Member.user_id AND Member.course_id = Course.id
#           ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
# 
# The output should look as follows:
# 
#       Zoha|si301|0
#       Zishan|si363|0
# 
# Once that query gives the correct data, run this query:
# 
#       SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
#           User JOIN Member JOIN Course 
#           ON User.id = Member.user_id AND Member.course_id = Course.id
#           ORDER BY X LIMIT 1;
# 
# You should get one row with a string that looks like XYZZY53656C696E613333.

import json
import sqlite3

# Create database
sql_connection = sqlite3.connect('roster_assignmend_db.sqlite')
cursor = sql_connection.cursor()

# Create database schema
cursor.executescript('''
    DROP TABLE IF EXISTS User;
    DROP TABLE IF EXISTS Member;
    DROP TABLE IF EXISTS Course;

    CREATE TABLE User (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE
    );

    CREATE TABLE Course (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title  TEXT UNIQUE
    );

    CREATE TABLE Member (
        user_id     INTEGER,
        course_id   INTEGER,
        role        INTEGER,
        PRIMARY KEY (user_id, course_id)
    )
''')

# Get the roaster file name
file_name = input('Enter file name: ')
if len(file_name) < 1: file_name = 'roster_data.json'

# Read file data
string_data = open(file_name).read()
json_data = json.loads(string_data)

# Parse file data
for entry in json_data:
    if len(entry) < 1: continue

    user_name = entry[0]
    course_title = entry[1]
    role = entry[2]

    # Insert User data
    cursor.execute('''
        INSERT OR IGNORE INTO User (name) VALUES (?)
    ''', (user_name, ))
    cursor.execute('''
        SELECT id FROM User WHERE User.name = ?
    ''', (user_name, ))
    user_id = cursor.fetchone()[0]
    
    # Insert Course data
    cursor.execute('''
        INSERT OR IGNORE INTO Course (title) VALUES (?)
    ''', (course_title, ))
    cursor.execute('''
        SELECT id FROM Course WHERE Course.title = ?
    ''', (course_title, ))
    course_id = cursor.fetchone()[0]

    # Insert join table data
    cursor.execute('''
        INSERT OR IGNORE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)
        ''', (user_id, course_id, role))
    
    # Commit transactions
    sql_connection.commit()

# Close connection to database
sql_connection.close()