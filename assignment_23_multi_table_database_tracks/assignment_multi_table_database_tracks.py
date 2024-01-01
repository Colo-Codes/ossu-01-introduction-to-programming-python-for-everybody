# Multi-Table Database - Tracks
# =============================
# Source: https://www.py4e.com/tools/sql-intro/?PHPSESSID=d01dd14fc7076e16d8cd0a11c1603031
# 
# Assignment: Musical Track Database
# ----------------------------------
#
# This application will read an iTunes export file in XML and produce a properly normalized database with this structure:
# 
#       CREATE TABLE Artist (
#           id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#           name    TEXT UNIQUE
#       );
#       
#       CREATE TABLE Genre (
#           id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#           name    TEXT UNIQUE
#       );
#       
#       CREATE TABLE Album (
#           id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#           artist_id  INTEGER,
#           title   TEXT UNIQUE
#       );
#       
#       CREATE TABLE Track (
#           id  INTEGER NOT NULL PRIMARY KEY 
#               AUTOINCREMENT UNIQUE,
#           title TEXT  UNIQUE,
#           album_id  INTEGER,
#           genre_id  INTEGER,
#           len INTEGER, rating INTEGER, count INTEGER
#       );
#
# If you run the program multiple times in testing or with different files, make sure to empty out the data before each 
# run.
# 
# You can use this code as a starting point for your application: http://www.py4e.com/code3/tracks.zip. The ZIP file 
# contains the Library.xml file to be used for this assignment. You can export your own tracks from iTunes and create a 
# database, but for the database that you turn in for this assignment, only use the Library.xml data that is provided.
# 
# To grade this assignment, the program will run a query like this on your uploaded database and look for the data it 
# expects to see:
# 
#       SELECT Track.title, Artist.name, Album.title, Genre.name 
#           FROM Track JOIN Genre JOIN Album JOIN Artist 
#           ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
#               AND Album.artist_id = Artist.id
#           ORDER BY Artist.name LIMIT 3
#
# The expected result of the modified query on your database is: (shown here as a simple HTML table with titles)
#
# | Track                                       | Artist | Album        | Genre |
# |---------------------------------------------|--------|--------------|-------|
# | Chase the Ace                               | AC/DC  | Who Made Who | Rock  |
# | D.T.                                        | AC/DC  | Who Made Who | Rock  |
# | For Those About To Rock (We Salute You)     | AC/DC  | Who Made Who | Rock  |

import xml.etree.ElementTree as ET
import sqlite3

# Establish DB and connection
db_connection = sqlite3.connect('tracks_assignment_db.sqlite')
cursor = db_connection.cursor()

# Create tables
cursor.executescript('''
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;
                     
    CREATE TABLE Artist (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE Genre (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE Album (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        artist_id  INTEGER,
        title   TEXT UNIQUE
    );

    CREATE TABLE Track (
        id  INTEGER NOT NULL PRIMARY KEY 
            AUTOINCREMENT UNIQUE,
        title TEXT  UNIQUE,
        album_id  INTEGER,
        genre_id  INTEGER,
        len INTEGER, rating INTEGER, count INTEGER
    );
''')

# Set the file name
file_name = input('Enter file name: ')
if (len(file_name) < 1): file_name = 'Library.xml'

# Lookup function
def lookup(dict_element, key):
    found = False
    for element in dict_element:
        if found: return element.text
        if element.tag == 'key' and element.text == key:
            found = True
    return None

# XML parsing
xml_data = ET.parse(file_name)
dict_elements = xml_data.findall('dict/dict/dict')
print('Dict count:', len(dict_elements))

for dict_element in dict_elements:
    if(lookup(dict_element, 'Track ID') is None): continue

    track_title = lookup(dict_element, 'Name')
    track_len = lookup(dict_element, 'Total Time')
    track_rating = lookup(dict_element, 'Rating')
    track_count = lookup(dict_element, 'Play Count')
    album_title = lookup(dict_element, 'Album')
    genre_name = lookup(dict_element, 'Genre')
    artist_name = lookup(dict_element, 'Artist')

    if track_title is None or track_len is None or album_title is None or genre_name is None or artist_name is None:
        continue
    print(track_title, track_len, album_title, genre_name, artist_name)

    # Insert data into the database
    cursor.execute('''
        INSERT OR IGNORE INTO Artist (name) VALUES (?)
    ''', (artist_name,))
    cursor.execute('SELECT id FROM Artist WHERE name = ? ', (artist_name, ))
    artist_id = cursor.fetchone()[0]
    
    cursor.execute('''
        INSERT OR IGNORE INTO Genre (name) VALUES (?)
    ''', (genre_name,))
    cursor.execute('SELECT id FROM Genre WHERE name = ? ', (genre_name, ))
    genre_id = cursor.fetchone()[0]
    
    cursor.execute('''
        INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?, ?)
    ''', (artist_id, album_title))
    cursor.execute('SELECT id FROM Album WHERE title = ? ', (album_title, ))
    album_id = cursor.fetchone()[0]
    
    cursor.execute('''
        INSERT OR IGNORE INTO Track (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)
    ''', (track_title, album_id, genre_id, track_len, track_rating, track_count))

    # Commit changes
    db_connection.commit()

db_connection.close()