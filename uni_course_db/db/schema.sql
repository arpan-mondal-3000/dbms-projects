-- =========================================
-- DEPARTMENT
-- =========================================
CREATE TABLE Department (
    name VARCHAR(100) PRIMARY KEY,
    location VARCHAR(100)
);

-- =========================================
-- SUBJECT AREAS
-- =========================================
CREATE TABLE SubjectAreas (
    name VARCHAR(100) PRIMARY KEY
);

-- =========================================
-- COURSE
-- =========================================
CREATE TABLE Course (
    title VARCHAR(150),
    year VARCHAR(10),
    duration VARCHAR(50),
    syllabus TEXT,
    offeredBy VARCHAR(100),
    PRIMARY KEY (title, year),
    FOREIGN KEY (offeredBy)
        REFERENCES Department(name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =========================================
-- USER
-- =========================================
CREATE TABLE User (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE
);

-- =========================================
-- STUDENT
-- =========================================
CREATE TABLE Student (
    studentId INT PRIMARY KEY,
    FOREIGN KEY (studentId)
        REFERENCES User(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- INSTRUCTOR
-- =========================================
CREATE TABLE Instructor (
    instructorId INT PRIMARY KEY,
    salary INT,
    FOREIGN KEY (instructorId)
        REFERENCES User(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- COURSE CLASSIFICATION
-- =========================================
CREATE TABLE CourseClassification (
    courseTitle VARCHAR(150),
    courseYear VARCHAR(10),
    subjectArea VARCHAR(100),
    PRIMARY KEY (courseTitle, courseYear, subjectArea),
    FOREIGN KEY (courseTitle, courseYear)
        REFERENCES Course(title, year)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subjectArea)
        REFERENCES SubjectAreas(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- ENROLLMENTS
-- =========================================
CREATE TABLE Enrollments (
    enrollmentDate DATE,
    grade VARCHAR(10),
    userId INT,
    courseTitle VARCHAR(150),
    courseYear VARCHAR(10),
    PRIMARY KEY (userId, courseTitle, courseYear),
    FOREIGN KEY (userId)
        REFERENCES User(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (courseTitle, courseYear)
        REFERENCES Course(title, year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- FINAL PROJECTS
-- =========================================
CREATE TABLE FinalProjects (
    title VARCHAR(150),
    userId INT,
    courseTitle VARCHAR(150),
    courseYear VARCHAR(10),
    PRIMARY KEY (userId, courseTitle, courseYear),
    FOREIGN KEY (userId)
        REFERENCES User(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (courseTitle, courseYear)
        REFERENCES Course(title, year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- PROJECT SUBMISSION
-- =========================================
CREATE TABLE ProjectSubmission (
    userId INT,
    courseTitle VARCHAR(150),
    courseYear VARCHAR(10),
    PRIMARY KEY (userId, courseTitle, courseYear),
    FOREIGN KEY (userId)
        REFERENCES User(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (courseTitle, courseYear)
        REFERENCES Course(title, year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- COURSE FACULTY
-- =========================================
CREATE TABLE CourseFaculty (
    instructorId INT,
    courseTitle VARCHAR(150),
    courseYear VARCHAR(10),
    PRIMARY KEY (instructorId, courseTitle, courseYear),
    FOREIGN KEY (instructorId)
        REFERENCES Instructor(instructorId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (courseTitle, courseYear)
        REFERENCES Course(title, year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================
-- DEPARTMENT COURSES
-- =========================================
CREATE TABLE DepartmentCourses (
    departmentName VARCHAR(100),
    courseTitle VARCHAR(150),
    courseYear VARCHAR(10),
    PRIMARY KEY (departmentName, courseTitle, courseYear),
    FOREIGN KEY (departmentName)
        REFERENCES Department(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (courseTitle, courseYear)
        REFERENCES Course(title, year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
