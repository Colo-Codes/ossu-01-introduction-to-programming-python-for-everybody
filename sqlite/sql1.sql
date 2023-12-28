-- Creating a table
CREATE TABLE Users (
	name VARCHAR(128),
	email VARCHAR(128)
);

-- Inserting records in a table: (C)RUD
INSERT INTO Users (name, email) VALUES ('Damian', 'contact@damiandemasi.com');
INSERT INTO Users (name, email) VALUES ('Chuck', 'csev@umich.edu');

-- Deleting records in a table: CRU(D)
DELETE FROM Users WHERE email = 'contact@damiandemasi.com';

-- Updating records in a table: CR(U)D
UPDATE Users SET name = 'Charles' WHERE email = 'csev@umich.edu';

-- Retrieving/Reading records in a table: C(R)UD
SELECT name FROM Users WHERE email = 'csev@umich.edu';
SELECT * FROM Users;
SELECT * FROM Users ORDER BY name;