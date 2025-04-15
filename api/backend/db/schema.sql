-- User table
CREATE TABLE IF NOT EXISTS User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    major VARCHAR(50),
    learning_style VARCHAR(50),
    availability INT DEFAULT 0  -- Bitmap for availability
);

-- Course table
CREATE TABLE IF NOT EXISTS Course (
    CourseID INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT
);

-- Enrollment table (many-to-many relationship between User and Course)
CREATE TABLE IF NOT EXISTS Enrollment (
    UserID INT,
    Course_ID INT,
    enrolled_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (UserID, Course_ID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (Course_ID) REFERENCES Course(CourseID)
);

-- Study Session table
CREATE TABLE IF NOT EXISTS Study_Session (
    SessionID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Matched_Student_ID INT,
    Course_ID INT,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Start_Date DATETIME,
    End_Date DATETIME,
    learning_style_match BOOLEAN,
    schedule_match BOOLEAN,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (Matched_Student_ID) REFERENCES User(UserID),
    FOREIGN KEY (Course_ID) REFERENCES Course(CourseID)
);

-- Insert some sample data
INSERT INTO User (name, email, password, major, learning_style, availability) VALUES
('John Doe', 'john@example.com', 'password123', 'Computer Science', 'visual', 127),
('Jane Smith', 'jane@example.com', 'password123', 'Computer Science', 'auditory', 63),
('Bob Wilson', 'bob@example.com', 'password123', 'Mathematics', 'kinesthetic', 31);

INSERT INTO Course (course_name, course_code, description) VALUES
('Introduction to Programming', 'CS101', 'Basic programming concepts'),
('Data Structures', 'CS201', 'Advanced data structures and algorithms'),
('Calculus I', 'MATH101', 'Introduction to calculus');

INSERT INTO Enrollment (UserID, Course_ID) VALUES
(1, 1), -- John enrolled in CS101
(1, 2), -- John enrolled in CS201
(2, 1), -- Jane enrolled in CS101
(3, 3); -- Bob enrolled in MATH101 