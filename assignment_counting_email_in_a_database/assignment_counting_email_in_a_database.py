# Counting Email in a Database
# ============================
# Source: https://www.py4e.com/tools/sql-intro/?PHPSESSID=d58f703485b43a11aca4a2a3bf3d21da
#
# Assignment: Counting Organizations
# ----------------------------------
#
# This application will read the mailbox data (mbox.txt) and count the number of email messages per organization (i.e. domain name of the email 
# address) using a database with the following schema to maintain the counts.
# 
#   CREATE TABLE Counts (org TEXT, count INTEGER)
#
# When you have run the program on mbox.txt upload the resulting database file above for grading.
# If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.
# 
# You can use this code as a starting point for your application: http://www.py4e.com/code3/emaildb.py.
# 
# The data file for this application is the same as in previous assignments: http://www.py4e.com/code3/mbox.txt.
# 
# Because the sample code is using an UPDATE statement and committing the results to the database as each record is read in the loop, it might 
# take as long as a few minutes to process all the data. The commit insists on completely writing all the data to disk every time it is called.
# 
# The program can be speeded up greatly by moving the commit operation outside of the loop. In any database program, there is a balance between 
# the number of operations you execute between commits and the importance of not losing the results of operations that have not yet been committed.

import sqlite3

db_connection = sqlite3.connect('organizations.sqlite')
cursor = db_connection.cursor()

# Drop table is it exists to prevent corrupted data
cursor.execute('''
    DROP TABLE IF EXISTS Counts
''')

# Create table
cursor.execute('''
    CREATE TABLE Counts (org TEXT, count INTEGER)
''')

# Load file data
file_name = input('Enter file name: ')
if (len(file_name) < 1): file_name = 'mbox.txt'
file_handle = open(file_name)

for line in file_handle:
    if not line.startswith('From: '): continue

    pieces = line.split()
    organisation = pieces[1].split('@')[1]
    
    # Get existing records
    cursor.execute('SELECT count FROM Counts WHERE org = ?', (organisation,))
    record = cursor.fetchone()
    if record is None:
        # If record is non existing, initialise it
        cursor.execute('''
            INSERT INTO Counts (org, count)
            VALUES (?, 1)
        ''', (organisation,))
    else:
        # If records exists, add 1 to its count
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (organisation,))
    db_connection.commit()

# Get the data from the database
sql_string = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 100'

for row in cursor.execute(sql_string):
    print(str(row[0]), row[1])

cursor.close()

# Output:
# Enter file name: 
# iupui.edu 536
# umich.edu 491
# indiana.edu 178
# caret.cam.ac.uk 157
# vt.edu 110
# uct.ac.za 96
# media.berkeley.edu 56
# ufp.pt 28
# gmail.com 25
# et.gatech.edu 17
# txstate.edu 17
# whitman.edu 17
# lancaster.ac.uk 14
# bu.edu 14
# stanford.edu 12
# unicon.net 9
# loi.nl 9
# rsmart.com 8
# ucdavis.edu 1
# fhda.edu 1
# utoronto.ca 1