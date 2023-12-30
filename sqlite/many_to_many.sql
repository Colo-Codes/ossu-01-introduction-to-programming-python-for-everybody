-- Source: https://www.coursera.org/learn/python-databases/lecture/2rkHv/15-8-many-to-many-relationships

-- The database is located in the databases/manytomany.db and was created using DB Browser for SQLite

-- CREATING TABLES
-- ---------------

CREATE TABLE Users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT
);

CREATE TABLE Courses (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT
);

CREATE TABLE Enrolements (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id) -- Building a primary key based on two foreign keys
);

-- INSERTING DATA
-- --------------

INSERT INTO Users (name) VALUES ('Jane');
INSERT INTO Users (name) VALUES ('Ed');
INSERT INTO Users (name) VALUES ('Sue');

INSERT INTO Courses (title) VALUES ('Python');
INSERT INTO Courses (title) VALUES ('Ruby on Rails');
INSERT INTO Courses (title) VALUES ('SQL');

-- Inserting Enrolements (role = 0 is a student, role = 1 is a teacher):
INSERT INTO Enrolements (user_id, Course_id, role) VALUES (1, 1, 1);
INSERT INTO Enrolements (user_id, Course_id, role) VALUES (2, 1, 0);
INSERT INTO Enrolements (user_id, Course_id, role) VALUES (3, 1, 0);

INSERT INTO Enrolements (user_id, Course_id, role) VALUES (1, 2, 0);
INSERT INTO Enrolements (user_id, Course_id, role) VALUES (2, 2, 1);

INSERT INTO Enrolements (user_id, Course_id, role) VALUES (2, 3, 1);
INSERT INTO Enrolements (user_id, Course_id, role) VALUES (3, 3, 0);

-- RECONSTRUCTING DATA
-- -------------------

SELECT Users.name, Enrolements.role, Courses.title
FROM Users JOIN Enrolements JOIN Courses
ON Enrolements.user_id = Users.id AND Enrolements.course_id = Courses.id
ORDER BY Courses.title, Enrolements.role DESC, Users.name
