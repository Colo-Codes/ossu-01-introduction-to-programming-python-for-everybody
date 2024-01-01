-- Our First Database
-- ==================
-- Source: https://www.py4e.com/tools/sql-intro/?PHPSESSID=56f4f7cf7a3ef77a1a09fb49033fae71
--
-- Assignment: Our First Database
-- ------------------------------
--
-- If you don't already have it, install the SQLite Browser from http://sqlitebrowser.org/.
-- 
-- Then, create a SQLITE database or use an existing database and create a table in the database called "Ages":
-- 
--      CREATE TABLE Ages ( 
--        name VARCHAR(128), 
--        age INTEGER
--      )
--
-- Then make sure the table is empty by deleting any rows that you previously inserted, and insert these rows and only these rows with the following commands:
-- 
--      DELETE FROM Ages;
--      INSERT INTO Ages (name, age) VALUES ('Zakiyya', 30);
--      INSERT INTO Ages (name, age) VALUES ('Kenzy', 38);
--      INSERT INTO Ages (name, age) VALUES ('Ameelia', 22);
--      INSERT INTO Ages (name, age) VALUES ('Aliyaan', 28);
--      INSERT INTO Ages (name, age) VALUES ('Josan', 40);
--      INSERT INTO Ages (name, age) VALUES ('Glen', 30);
--
-- Once the inserts are done, run the following SQL command:
--      SELECT hex(name || age) AS X FROM Ages ORDER BY X
--
-- Find the first row in the resulting record set and enter the long string that looks like 53656C696E613333.
-- Note: This assignment must be done using SQLite - in particular, the SELECT query above will not work in any other database. So you cannot use MySQL or Oracle 
-- for this assignment.

CREATE TABLE Ages ( 
  name VARCHAR(128), 
  age INTEGER
);

DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Zakiyya', 30);
INSERT INTO Ages (name, age) VALUES ('Kenzy', 38);
INSERT INTO Ages (name, age) VALUES ('Ameelia', 22);
INSERT INTO Ages (name, age) VALUES ('Aliyaan', 28);
INSERT INTO Ages (name, age) VALUES ('Josan', 40);
INSERT INTO Ages (name, age) VALUES ('Glen', 30);

SELECT hex(name || age) AS X FROM Ages ORDER BY X;
-- Output:
-- 416C697961616E3238 <-- This is the answer
-- 416D65656C69613232
-- 476C656E3330
-- 4A6F73616E3430
-- 4B656E7A793338
-- 5A616B697979613330