-- SQL FUNDAMENTALS | PostgreSQL practice notes
-- Open this file in VS Code to edit and save your notes.
-- Execute statements in pgAdmin's Query Tool (highlight only the SQL you want to run).
-- Connect to the database named sql_practice before executing these statements.

-- 1. CREATE A TABLE (run once)
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INTEGER,
    year INTEGER
);

-- 2. INSERT EXAMPLE DATA (safe to repeat: existing IDs will not be inserted again)
INSERT INTO students (id, name, age, year)
VALUES
    (1, 'John', 22, 3),
    (2, 'Paige', 24, 2),
    (3, 'Anna', 21, 1)
ON CONFLICT (id) DO NOTHING;

-- 3. SELECT: retrieve data
SELECT * FROM students;

-- 4. WHERE: filter rows
SELECT name, age FROM students WHERE age > 21;

-- 5. ORDER BY: sort results
SELECT name, age FROM students ORDER BY age DESC;

-- 6. UPDATE: edit matching rows
-- Try the following yourself, then remove the comment markers:
-- UPDATE students SET age = 25 WHERE id = 2;

-- 7. INSERT: add a student with id 4, name Alex, age 20, year 2
-- Write your query here:

-- 8. DELETE: remove student with id 3
-- Write your query here:

-- 9. Verify your changes
-- SELECT * FROM students ORDER BY id;

-- NOTES
-- CREATE TABLE: defines columns and their types.
-- PRIMARY KEY: unique, non-NULL identifier for each row.
-- VARCHAR(50): text up to 50 characters.
-- NOT NULL: column requires a value.
-- UPDATE or DELETE without WHERE may affect every row: be careful.
-- SQL comments start with -- and SQL statements typically end with ;
