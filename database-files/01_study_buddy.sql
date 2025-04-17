-- database
drop database if exists study_buddy_system;
create database study_buddy_system;
use study_buddy_system;

-- admin
drop table if exists admin;
create table admin (
    adminid int auto_increment primary key,
    name varchar(255) not null,
    role varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null
);

-- logs
drop table if exists systemlog;
create table systemlog (
    logid int auto_increment primary key,
    adminid int,
    action varchar(255) not null,
    actiontime timestamp default current_timestamp,
    foreign key (adminid) references admin(adminid)
);

-- server
drop table if exists serverstatus;
create table serverstatus (
    serverid int auto_increment primary key,
    cpu_usage decimal(5, 2) not null,
    memory_usage decimal(5, 2) not null,
    active_user_count int not null
);

-- interests
drop table if exists interests;
create table interests (
    interestid int auto_increment primary key,
    description text not null
);

-- feedback
drop table if exists effectiveness;
create table effectiveness (
    effectivenessid int auto_increment primary key,
    academic_improvement text,
    student_feedback text
);

-- university
drop table if exists university;
create table university (
    universityid int auto_increment primary key,
    name varchar(255) not null,
    coursecatalogid int
);

-- course
drop table if exists course;
create table course (
    courseid int auto_increment primary key,
    universityid int,
    department varchar(255) not null,
    course_name varchar(255) not null,
    foreign key (universityid) references university(universityid)
);

-- groups
drop table if exists study_group;
create table study_group (
    groupid int auto_increment primary key,
    group_name varchar(255) -- Added group name, allow NULL for existing groups?
    -- Make NOT NULL if all groups must have a name
);

-- users
drop table if exists user;
create table user (
    userid int auto_increment primary key,
    name varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null,
    major varchar(255),
    learning_style varchar(255),
    availability varchar(255)
    -- Removed groupid column and its foreign key constraint
    -- groupid int, 
    -- foreign key (groupid) references study_group(groupid)
);

-- update groups
alter table study_group
add column student_id int,
add foreign key (student_id) references user(userid);

-- compatibility
drop table if exists compatibility;
create table compatibility (
    userid int primary key,
    academic_goals text,
    learning_style text,
    schedule_conflicts text,
    foreign key (userid) references user(userid)
);

-- matches
drop table if exists matchhistory;
create table matchhistory (
    matchid int auto_increment primary key,
    userid int not null,
    matchscore decimal(5, 2) not null,
    matchdate date not null,
    foreign key (userid) references user(userid)
);

-- Table for established matches between two users
drop table if exists matched_with;
create table matched_with (
    user1_id int not null,
    user2_id int not null,
    match_date timestamp default current_timestamp, -- Optional: track when match occurred
    primary key (user1_id, user2_id), -- Composite primary key
    foreign key (user1_id) references user(userid),
    foreign key (user2_id) references user(userid),
    check (user1_id < user2_id)-- constraint to make it easier to get matches
);

-- resources
drop table if exists resource;
create table resource (
    resourceid int auto_increment primary key,
    resource_link text not null,
    resource_type varchar(255) not null
);

-- sessions
drop table if exists study_session;
create table study_session (
    session_id int auto_increment primary key,
    course_id int not null,
    matched_student_id int not null,
    study_type varchar(255) not null,
    session_date date not null,
    foreign key (course_id) references course(courseid),
    foreign key (matched_student_id) references user(userid)
);

-- user resources
drop table if exists user_resource;
create table user_resource (
    userid int not null,
    resourceid int not null,
    primary key (userid, resourceid),
    foreign key (userid) references user(userid),
    foreign key (resourceid) references resource(resourceid)
);

-- user interests
drop table if exists user_interests;
create table user_interests (
    userid int not null,
    interestid int not null,
    primary key (userid, interestid),
    foreign key (userid) references user(userid),
    foreign key (interestid) references interests(interestid)
);

-- Create Junction Table for Group Students (Many-to-Many)
drop table if exists group_student;
create table group_student (
    groupid int not null,
    studentid int not null, -- Corresponds to user.userid
    primary key (groupid, studentid), -- Composite primary key
    foreign key (groupid) references study_group(groupid),
    foreign key (studentid) references user(userid) -- FK to user table
);

-- data

-- admin
insert into admin (name, role, email, password) values
('john doe', 'system administrator', 'john.doe@example.com', 'adminpass1'),
('Sophia Chen', 'data analyst', 'sophia.chen@example.com', 'adminpass2'),
('robert johnson', 'support specialist', 'robert.johnson@example.com', 'adminpass3');

-- logs
insert into systemlog (adminid, action, actiontime) values
(1, 'system startup', '2025-03-30 08:00:00'),
(2, 'user management', '2025-03-30 09:30:00'),
(3, 'database backup', '2025-03-30 22:00:00');

-- server
insert into serverstatus (cpu_usage, memory_usage, active_user_count) values
(45.5, 60.2, 120),
(32.8, 55.7, 98),
(78.3, 87.1, 256);

-- interests
insert into interests (description) values
('machine learning'),
('web development'),
('database management');

-- feedback
insert into effectiveness (academic_improvement, student_feedback) values
('85% of students improved their grades by at least one letter grade', 'very positive feedback with 90% satisfaction rate'),
('74% of students reported better understanding of complex topics', 'good feedback with suggestions for improvement'),
('92% of students completed their assignments on time', 'excellent feedback on group dynamics');

-- university
insert into university (name, coursecatalogid) values
('harvard university', 101),
('stanford university', 102),
('mit', 103);

-- course
insert into course (universityid, department, course_name) values
(1, 'computer science', 'introduction to programming'),
(2, 'data science', 'machine learning fundamentals'),
(3, 'artificial intelligence', 'neural networks');

-- groups
insert into study_group (groupid) values (1), (2), (3);
UPDATE study_group SET group_name = 'CS Fundamentals' WHERE groupid = 1;
UPDATE study_group SET group_name = 'Data Science Intro' WHERE groupid = 2;
UPDATE study_group SET group_name = 'AI Concepts' WHERE groupid = 3;

-- Add new groups with names (will start from ID 4)
insert into study_group (group_name) values
('CS3000 Study Group'),   -- ID 4
('CS3200 Study Group'),   -- ID 5
('CS2510 Study Group'),   -- ID 6
('FINA2201 Study Group'),  -- ID 7
('General Programming Help'); -- ID 8 (Note: ID changed from 5 due to split inserts)

-- users
insert into user (name, email, password, major, learning_style, availability) values
-- Original sample users
('alice williams', 'alice.williams@example.com', 'password123', 'computer science', 'visual', 'evenings and weekends'),
('bob brown', 'bob.brown@example.com', 'password456', 'data science', 'auditory', 'weekdays'),
('charlie davis', 'charlie.davis@example.com', 'password789', 'artificial intelligence', 'kinesthetic', 'flexible'),
('Alex Chen', 'alex.chen@example.com', 'password', 'Computer Science', 'kinesthetic', 'flexible'),
('Emily Smith', 'emily.smith@example.com', 'emily123', 'Computer Science', 'visual', 'weekdays and weekends'),
-- Northeastern users with unique emails
('John Smith', 'john.smith@northeastern.edu', 'hashed_password_1', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
('Mary Johnson', 'mary.johnson@northeastern.edu', 'hashed_password_2', 'Psychology', 'Auditory', 'Weekday Mornings'),
('Robert Williams', 'robert.williams@northeastern.edu', 'hashed_password_3', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
('Patricia Brown', 'patricia.brown@northeastern.edu', 'hashed_password_4', 'International Business', 'Visual', 'Weekday Evenings'),
('David Jones', 'david.jones@northeastern.edu', 'hashed_password_5', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
('Linda Garcia', 'linda.garcia@northeastern.edu', 'hashed_password_6', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
('Michael Miller', 'michael.miller@northeastern.edu', 'hashed_password_7', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
('Barbara Wilson', 'barbara.wilson@northeastern.edu', 'hashed_password_8', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
('James Moore', 'james.moore@northeastern.edu', 'hashed_password_9', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
('Margaret Taylor', 'margaret.taylor@northeastern.edu', 'hashed_password_10', 'Business Administration', 'Visual', 'Weekday Evenings'),
('William Anderson', 'william.anderson@northeastern.edu', 'hashed_password_11', 'Computer Science and Biology', 'Auditory', 'Weekday Mornings'),
('Sarah Thomas', 'sarah.thomas@northeastern.edu', 'hashed_password_12', 'Health Science', 'Kinesthetic', 'Flexible'),
('Charles Jackson', 'charles.jackson@northeastern.edu', 'hashed_password_13', 'Computer Science and Game Design', 'Visual', 'Weekday Evenings'),
('Karen White', 'karen.white@northeastern.edu', 'hashed_password_14', 'Business Analytics', 'Auditory', 'Weekday Mornings'),
('Daniel Harris', 'daniel.harris@northeastern.edu', 'hashed_password_15', 'Computer Science and Music Technology', 'Kinesthetic', 'Flexible'),
('Jennifer Martin', 'jennifer.martin@northeastern.edu', 'hashed_password_16', 'Entrepreneurship and Innovation', 'Visual', 'Weekday Evenings'),
('Paul Lee', 'paul.lee@northeastern.edu', 'hashed_password_17', 'Computer Science and Design', 'Auditory', 'Weekday Mornings'),
('Nancy Thompson', 'nancy.thompson@northeastern.edu', 'hashed_password_18', 'Supply Chain Management', 'Kinesthetic', 'Flexible'),
('Kevin Clark', 'kevin.clark@northeastern.edu', 'hashed_password_19', 'Computer Science and Environmental Science', 'Visual', 'Weekday Evenings'),
('Laura Rodriguez', 'laura.rodriguez@northeastern.edu', 'hashed_password_20', 'International Affairs', 'Auditory', 'Weekday Mornings'),
-- Additional users with unique emails (21-40)
('Alex Smith', 'alex.smith21@northeastern.edu', 'hashed_password_21', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
('Emma Johnson', 'emma.johnson22@northeastern.edu', 'hashed_password_22', 'Neuroscience', 'Auditory', 'Weekday Mornings'),
('Matt Williams', 'matt.williams23@northeastern.edu', 'hashed_password_23', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
('Sophia Brown', 'sophia.brown24@northeastern.edu', 'hashed_password_24', 'International Business', 'Visual', 'Weekday Evenings'),
('Dylan Jones', 'dylan.jones25@northeastern.edu', 'hashed_password_25', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
('Lucas Garcia', 'lucas.garcia26@northeastern.edu', 'hashed_password_26', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
('Mia Miller', 'mia.miller27@northeastern.edu', 'hashed_password_27', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
('Ben Wilson', 'ben.wilson28@northeastern.edu', 'hashed_password_28', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
('Julia Moore', 'julia.moore29@northeastern.edu', 'hashed_password_29', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
('Max Taylor', 'max.taylor30@northeastern.edu', 'hashed_password_30', 'Business Administration', 'Visual', 'Weekday Evenings'),
('Willow Anderson', 'willow.anderson31@northeastern.edu', 'hashed_password_31', 'Computer Science and Biology', 'Auditory', 'Weekday Mornings'),
('Sam Thomas', 'sam.thomas32@northeastern.edu', 'hashed_password_32', 'Health Science', 'Kinesthetic', 'Flexible'),
('Chloe Jackson', 'chloe.jackson33@northeastern.edu', 'hashed_password_33', 'Computer Science and Game Design', 'Visual', 'Weekday Evenings'),
('Kyle White', 'kyle.white34@northeastern.edu', 'hashed_password_34', 'Business Analytics', 'Auditory', 'Weekday Mornings'),
('Daisy Harris', 'daisy.harris35@northeastern.edu', 'hashed_password_35', 'Computer Science and Music Technology', 'Kinesthetic', 'Flexible'),
('Jack Martin', 'jack.martin36@northeastern.edu', 'hashed_password_36', 'Entrepreneurship and Innovation', 'Visual', 'Weekday Evenings'),
('Piper Lee', 'piper.lee37@northeastern.edu', 'hashed_password_37', 'Computer Science and Design', 'Auditory', 'Weekday Mornings'),
('Noah Thompson', 'noah.thompson38@northeastern.edu', 'hashed_password_38', 'Supply Chain Management', 'Kinesthetic', 'Flexible'),
('Kate Clark', 'kate.clark39@northeastern.edu', 'hashed_password_39', 'Computer Science and Environmental Science', 'Visual', 'Weekday Evenings'),
('Liam Rodriguez', 'liam.rodriguez40@northeastern.edu', 'hashed_password_40', 'International Affairs', 'Auditory', 'Weekday Mornings'),
-- Additional users with unique emails (41-60)
('Ryan Green', 'ryan.green41@northeastern.edu', 'hashed_password_41', 'Computer Science and Business', 'Kinesthetic', 'Flexible'),
('Ava Hall', 'ava.hall42@northeastern.edu', 'hashed_password_42', 'Biochemistry', 'Visual', 'Weekday Evenings'),
('James Wright', 'james.wright43@northeastern.edu', 'hashed_password_43', 'Computer Science and Mathematics', 'Auditory', 'Weekday Mornings'),
('Sarah Lee', 'sarah.lee44@northeastern.edu', 'hashed_password_44', 'International Business', 'Kinesthetic', 'Flexible'),
('Michael King', 'michael.king45@northeastern.edu', 'hashed_password_45', 'Computer Science and Cognitive Psychology', 'Visual', 'Weekday Evenings'),
('Lily Scott', 'lily.scott46@northeastern.edu', 'hashed_password_46', 'Finance and Accounting', 'Auditory', 'Weekday Mornings'),
('Daniel Nguyen', 'daniel.nguyen47@northeastern.edu', 'hashed_password_47', 'Computer Science and Physics', 'Kinesthetic', 'Flexible'),
('Hannah Kim', 'hannah.kim48@northeastern.edu', 'hashed_password_48', 'Marketing and Communications', 'Visual', 'Weekday Evenings'),
('Jason Chen', 'jason.chen49@northeastern.edu', 'hashed_password_49', 'Computer Science and Economics', 'Auditory', 'Weekday Mornings'),
('Megan Wang', 'megan.wang50@northeastern.edu', 'hashed_password_50', 'Business Administration', 'Kinesthetic', 'Flexible'),
('Tyler Li', 'tyler.li51@northeastern.edu', 'hashed_password_51', 'Computer Science and Biology', 'Visual', 'Weekday Evenings'),
('Rachel Patel', 'rachel.patel52@northeastern.edu', 'hashed_password_52', 'Health Science', 'Auditory', 'Weekday Mornings'),
('Kevin Singh', 'kevin.singh53@northeastern.edu', 'hashed_password_53', 'Computer Science and Game Design', 'Kinesthetic', 'Flexible'),
('Priya Gupta', 'priya.gupta54@northeastern.edu', 'hashed_password_54', 'Business Analytics', 'Visual', 'Weekday Evenings'),
('David Shah', 'david.shah55@northeastern.edu', 'hashed_password_55', 'Computer Science and Music Technology', 'Auditory', 'Weekday Mornings'),
('Sneha Desai', 'sneha.desai56@northeastern.edu', 'hashed_password_56', 'Entrepreneurship and Innovation', 'Kinesthetic', 'Flexible'),
('Rahul Mehta', 'rahul.mehta57@northeastern.edu', 'hashed_password_57', 'Computer Science and Design', 'Visual', 'Weekday Evenings'),
('Neha Sharma', 'neha.sharma58@northeastern.edu', 'hashed_password_58', 'Supply Chain Management', 'Auditory', 'Weekday Mornings'),
('Arjun Kumar', 'arjun.kumar59@northeastern.edu', 'hashed_password_59', 'Computer Science and Environmental Science', 'Kinesthetic', 'Flexible'),
('Pooja Verma', 'pooja.verma60@northeastern.edu', 'hashed_password_60', 'International Affairs', 'Visual', 'Weekday Evenings'),
-- Additional users with unique emails (61-80)
('Ravi Reddy', 'ravi.reddy61@northeastern.edu', 'hashed_password_61', 'Computer Science and Business', 'Auditory', 'Weekday Mornings'),
('Sneha Rao', 'sneha.rao62@northeastern.edu', 'hashed_password_62', 'Chemical Engineering', 'Kinesthetic', 'Flexible'),
('Vijay Patel', 'vijay.patel63@northeastern.edu', 'hashed_password_63', 'Computer Science and Mathematics', 'Visual', 'Weekday Evenings'),
('Priyanka Desai', 'priyanka.desai64@northeastern.edu', 'hashed_password_64', 'International Business', 'Auditory', 'Weekday Mornings'),
('Meera Reddy', 'meera.reddy65@northeastern.edu', 'hashed_password_65', 'Computer Science and Cognitive Psychology', 'Kinesthetic', 'Flexible'),
('Sanjay Rao', 'sanjay.rao66@northeastern.edu', 'hashed_password_66', 'Finance and Accounting', 'Visual', 'Weekday Evenings'),
('Riya Patel', 'riya.patel67@northeastern.edu', 'hashed_password_67', 'Computer Science and Physics', 'Auditory', 'Weekday Mornings'),
('Anita Desai', 'anita.desai68@northeastern.edu', 'hashed_password_68', 'Marketing and Communications', 'Kinesthetic', 'Flexible'),
('Vikram Reddy', 'vikram.reddy69@northeastern.edu', 'hashed_password_69', 'Computer Science and Economics', 'Visual', 'Weekday Evenings'),
('Pooja Rao', 'pooja.rao70@northeastern.edu', 'hashed_password_70', 'Business Administration', 'Auditory', 'Weekday Mornings'),
('Rahul Patel', 'rahul.patel71@northeastern.edu', 'hashed_password_71', 'Computer Science and Biology', 'Kinesthetic', 'Flexible'),
('Sonia Desai', 'sonia.desai72@northeastern.edu', 'hashed_password_72', 'Health Science', 'Visual', 'Weekday Evenings'),
('Anand Reddy', 'anand.reddy73@northeastern.edu', 'hashed_password_73', 'Computer Science and Game Design', 'Auditory', 'Weekday Mornings'),
('Priya Rao', 'priya.rao74@northeastern.edu', 'hashed_password_74', 'Business Analytics', 'Kinesthetic', 'Flexible'),
('Vivek Patel', 'vivek.patel75@northeastern.edu', 'hashed_password_75', 'Computer Science and Music Technology', 'Visual', 'Weekday Evenings'),
('Sanjay Desai', 'sanjay.desai76@northeastern.edu', 'hashed_password_76', 'Entrepreneurship and Innovation', 'Auditory', 'Weekday Mornings'),
('Riya Reddy', 'riya.reddy77@northeastern.edu', 'hashed_password_77', 'Computer Science and Design', 'Kinesthetic', 'Flexible'),
('Anita Rao', 'anita.rao78@northeastern.edu', 'hashed_password_78', 'Supply Chain Management', 'Visual', 'Weekday Evenings'),
('Vikram Patel', 'vikram.patel79@northeastern.edu', 'hashed_password_79', 'Computer Science and Environmental Science', 'Auditory', 'Weekday Mornings'),
('Pooja Desai', 'pooja.desai80@northeastern.edu', 'hashed_password_80', 'International Affairs', 'Kinesthetic', 'Flexible'),
-- Additional users with unique emails (81-100)
('Ravi Reddy', 'ravi.reddy81@northeastern.edu', 'hashed_password_81', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
('Sneha Rao', 'sneha.rao82@northeastern.edu', 'hashed_password_82', 'Mechanical Engineering', 'Auditory', 'Weekday Mornings'),
('Vijay Patel', 'vijay.patel83@northeastern.edu', 'hashed_password_83', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
('Priyanka Desai', 'priyanka.desai84@northeastern.edu', 'hashed_password_84', 'International Business', 'Visual', 'Weekday Evenings'),
('Meera Reddy', 'meera.reddy85@northeastern.edu', 'hashed_password_85', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
('Sanjay Rao', 'sanjay.rao86@northeastern.edu', 'hashed_password_86', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
('Riya Patel', 'riya.patel87@northeastern.edu', 'hashed_password_87', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
('Anita Desai', 'anita.desai88@northeastern.edu', 'hashed_password_88', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
('Vikram Reddy', 'vikram.reddy89@northeastern.edu', 'hashed_password_89', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
('Pooja Rao', 'pooja.rao90@northeastern.edu', 'hashed_password_90', 'Business Administration', 'Visual', 'Weekday Evenings'),
('Rahul Patel', 'rahul.patel91@northeastern.edu', 'hashed_password_91', 'Computer Science and Biology', 'Auditory', 'Weekday Mornings'),
('Sonia Desai', 'sonia.desai92@northeastern.edu', 'hashed_password_92', 'Health Science', 'Kinesthetic', 'Flexible'),
('Anand Reddy', 'anand.reddy93@northeastern.edu', 'hashed_password_93', 'Computer Science and Game Design', 'Visual', 'Weekday Evenings'),
('Priya Rao', 'priya.rao94@northeastern.edu', 'hashed_password_94', 'Business Analytics', 'Auditory', 'Weekday Mornings'),
('Vivek Patel', 'vivek.patel95@northeastern.edu', 'hashed_password_95', 'Computer Science and Music Technology', 'Kinesthetic', 'Flexible'),
('Sanjay Desai', 'sanjay.desai96@northeastern.edu', 'hashed_password_96', 'Entrepreneurship and Innovation', 'Visual', 'Weekday Evenings'),
('Riya Reddy', 'riya.reddy97@northeastern.edu', 'hashed_password_97', 'Computer Science and Design', 'Auditory', 'Weekday Mornings'),
('Anita Rao', 'anita.rao98@northeastern.edu', 'hashed_password_98', 'Supply Chain Management', 'Kinesthetic', 'Flexible'),
('Vikram Patel', 'vikram.patel99@northeastern.edu', 'hashed_password_99', 'Computer Science and Environmental Science', 'Visual', 'Weekday Evenings'),
('Pooja Desai', 'pooja.desai100@northeastern.edu', 'hashed_password_100', 'International Affairs', 'Auditory', 'Weekday Mornings'),
-- Additional users with unique emails (101-120)
('Ravi Reddy', 'ravi.reddy101@northeastern.edu', 'hashed_password_101', 'Computer Science and Business', 'Kinesthetic', 'Flexible'),
('Sneha Rao', 'sneha.rao102@northeastern.edu', 'hashed_password_102', 'Electrical Engineering', 'Visual', 'Weekday Evenings'),
('Vijay Patel', 'vijay.patel103@northeastern.edu', 'hashed_password_103', 'Computer Science and Mathematics', 'Auditory', 'Weekday Mornings'),
('Priyanka Desai', 'priyanka.desai104@northeastern.edu', 'hashed_password_104', 'International Business', 'Kinesthetic', 'Flexible'),
('Meera Reddy', 'meera.reddy105@northeastern.edu', 'hashed_password_105', 'Computer Science and Cognitive Psychology', 'Visual', 'Weekday Evenings'),
('Sanjay Rao', 'sanjay.rao106@northeastern.edu', 'hashed_password_106', 'Finance and Accounting', 'Auditory', 'Weekday Mornings'),
('Riya Patel', 'riya.patel107@northeastern.edu', 'hashed_password_107', 'Computer Science and Physics', 'Kinesthetic', 'Flexible'),
('Anita Desai', 'anita.desai108@northeastern.edu', 'hashed_password_108', 'Marketing and Communications', 'Visual', 'Weekday Evenings'),
('Vikram Reddy', 'vikram.reddy109@northeastern.edu', 'hashed_password_109', 'Computer Science and Economics', 'Auditory', 'Weekday Mornings'),
('Pooja Rao', 'pooja.rao110@northeastern.edu', 'hashed_password_110', 'Business Administration', 'Kinesthetic', 'Flexible'),
('Rahul Patel', 'rahul.patel111@northeastern.edu', 'hashed_password_111', 'Computer Science and Biology', 'Visual', 'Weekday Evenings'),
('Sonia Desai', 'sonia.desai112@northeastern.edu', 'hashed_password_112', 'Health Science', 'Auditory', 'Weekday Mornings'),
('Anand Reddy', 'anand.reddy113@northeastern.edu', 'hashed_password_113', 'Computer Science and Game Design', 'Kinesthetic', 'Flexible'),
('Priya Rao', 'priya.rao114@northeastern.edu', 'hashed_password_114', 'Business Analytics', 'Visual', 'Weekday Evenings'),
('Vivek Patel', 'vivek.patel115@northeastern.edu', 'hashed_password_115', 'Computer Science and Music Technology', 'Auditory', 'Weekday Mornings'),
('Sanjay Desai', 'sanjay.desai116@northeastern.edu', 'hashed_password_116', 'Entrepreneurship and Innovation', 'Kinesthetic', 'Flexible'),
('Riya Reddy', 'riya.reddy117@northeastern.edu', 'hashed_password_117', 'Computer Science and Design', 'Visual', 'Weekday Evenings'),
('Anita Rao', 'anita.rao118@northeastern.edu', 'hashed_password_118', 'Supply Chain Management', 'Auditory', 'Weekday Mornings'),
('Vikram Patel', 'vikram.patel119@northeastern.edu', 'hashed_password_119', 'Computer Science and Environmental Science', 'Kinesthetic', 'Flexible'),
('Pooja Desai', 'pooja.desai120@northeastern.edu', 'hashed_password_120', 'International Affairs', 'Visual', 'Weekday Evenings'),
-- Additional users with unique emails (121-140)
('Ravi Reddy', 'ravi.reddy121@northeastern.edu', 'hashed_password_121', 'Computer Science and Business', 'Auditory', 'Weekday Mornings'),
('Sneha Rao', 'sneha.rao122@northeastern.edu', 'hashed_password_122', 'Civil Engineering', 'Kinesthetic', 'Flexible'),
('Vijay Patel', 'vijay.patel123@northeastern.edu', 'hashed_password_123', 'Computer Science and Mathematics', 'Visual', 'Weekday Evenings'),
('Priyanka Desai', 'priyanka.desai124@northeastern.edu', 'hashed_password_124', 'International Business', 'Auditory', 'Weekday Mornings'),
('Meera Reddy', 'meera.reddy125@northeastern.edu', 'hashed_password_125', 'Computer Science and Cognitive Psychology', 'Kinesthetic', 'Flexible'),
('Sanjay Rao', 'sanjay.rao126@northeastern.edu', 'hashed_password_126', 'Finance and Accounting', 'Visual', 'Weekday Evenings'),
('Riya Patel', 'riya.patel127@northeastern.edu', 'hashed_password_127', 'Computer Science and Physics', 'Auditory', 'Weekday Mornings'),
('Anita Desai', 'anita.desai128@northeastern.edu', 'hashed_password_128', 'Marketing and Communications', 'Kinesthetic', 'Flexible'),
('Vikram Reddy', 'vikram.reddy129@northeastern.edu', 'hashed_password_129', 'Computer Science and Economics', 'Visual', 'Weekday Evenings'),
('Pooja Rao', 'pooja.rao130@northeastern.edu', 'hashed_password_130', 'Business Administration', 'Auditory', 'Weekday Mornings'),
('Rahul Patel', 'rahul.patel131@northeastern.edu', 'hashed_password_131', 'Computer Science and Biology', 'Kinesthetic', 'Flexible'),
('Sonia Desai', 'sonia.desai132@northeastern.edu', 'hashed_password_132', 'Health Science', 'Visual', 'Weekday Evenings'),
('Anand Reddy', 'anand.reddy133@northeastern.edu', 'hashed_password_133', 'Computer Science and Game Design', 'Auditory', 'Weekday Mornings'),
('Priya Rao', 'priya.rao134@northeastern.edu', 'hashed_password_134', 'Business Analytics', 'Kinesthetic', 'Flexible'),
('Vivek Patel', 'vivek.patel135@northeastern.edu', 'hashed_password_135', 'Computer Science and Music Technology', 'Visual', 'Weekday Evenings'),
('Sanjay Desai', 'sanjay.desai136@northeastern.edu', 'hashed_password_136', 'Entrepreneurship and Innovation', 'Auditory', 'Weekday Mornings'),
('Riya Reddy', 'riya.reddy137@northeastern.edu', 'hashed_password_137', 'Computer Science and Design', 'Kinesthetic', 'Flexible'),
('Anita Rao', 'anita.rao138@northeastern.edu', 'hashed_password_138', 'Supply Chain Management', 'Visual', 'Weekday Evenings'),
('Vikram Patel', 'vikram.patel139@northeastern.edu', 'hashed_password_139', 'Computer Science and Environmental Science', 'Auditory', 'Weekday Mornings'),
('Pooja Desai', 'pooja.desai140@northeastern.edu', 'hashed_password_140', 'International Affairs', 'Kinesthetic', 'Flexible'),
-- Additional users with unique emails (141-150)
('Ravi Reddy', 'ravi.reddy141@northeastern.edu', 'hashed_password_141', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
('Sneha Rao', 'sneha.rao142@northeastern.edu', 'hashed_password_142', 'Industrial Engineering', 'Auditory', 'Weekday Mornings'),
('Vijay Patel', 'vijay.patel143@northeastern.edu', 'hashed_password_143', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
('Priyanka Desai', 'priyanka.desai144@northeastern.edu', 'hashed_password_144', 'International Business', 'Visual', 'Weekday Evenings'),
('Meera Reddy', 'meera.reddy145@northeastern.edu', 'hashed_password_145', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
('Sanjay Rao', 'sanjay.rao146@northeastern.edu', 'hashed_password_146', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
('Riya Patel', 'riya.patel147@northeastern.edu', 'hashed_password_147', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
('Anita Desai', 'anita.desai148@northeastern.edu', 'hashed_password_148', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
('Vikram Reddy', 'vikram.reddy149@northeastern.edu', 'hashed_password_149', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
('Pooja Rao', 'pooja.rao150@northeastern.edu', 'hashed_password_150', 'Business Administration', 'Visual', 'Weekday Evenings');


-- update groups (student_id link - kept as per original schema)
update study_group set student_id = 1 where groupid = 1;
update study_group set student_id = 2 where groupid = 2;
update study_group set student_id = 3 where groupid = 3;
-- Note: Groups 4+ don't have a single primary student via this mechanism

-- Populate group_student junction table consistently
-- Add users to their primary groups via this table
insert into group_student (groupid, studentid) values
(1, 1), -- Alice in CS Fundamentals
(2, 2), -- Bob in Data Science Intro
(3, 3), -- Charlie in AI Concepts
(1, 4); -- Alex in CS Fundamentals (his primary group)

-- Add Alex Chen (UserID 4) to his specific course groups
insert into group_student (groupid, studentid) values
(4, 4), -- Alex in CS3000 Group
(5, 4), -- Alex in CS3200 Group
(6, 4), -- Alex in CS2510 Group
(7, 4); -- Alex in FINA2201 Group

-- Add other memberships
-- Note: Group ID for General Programming Help is now 8
insert into group_student (groupid, studentid) values
(8, 1), -- Alice in General Programming Help
(8, 2); -- Bob in General Programming Help

-- compatibility
insert into compatibility (userid, academic_goals, learning_style, schedule_conflicts) values
(1, 'improve programming skills', 'visual', 'monday evenings'),
(2, 'master data analysis techniques', 'auditory', 'friday mornings'),
(3, 'understand ai algorithms', 'kinesthetic', 'none');

-- matches
insert into matchhistory (userid, matchscore, matchdate) values
(1, 89.5, '2025-03-15'),
(2, 92.7, '2025-03-16'),
(3, 78.3, '2025-03-17');

-- Add sample match for Alex Chen (UserID 4) with Alice Williams (UserID 1)
-- Ensure user1_id < user2_id
insert into matched_with (user1_id, user2_id, match_date) values
-- Original matches - ensuring user1_id < user2_id
(1, 2, '2024-03-01 10:00:00'),
(1, 4, '2025-03-15 12:00:00'), -- Alex (4) matches with Alice (1) - preserved earlier match
(3, 4, '2024-03-02 11:00:00'),
(5, 6, '2024-03-03 12:00:00'),
(7, 8, '2024-03-04 13:00:00'),
(9, 10, '2024-03-05 14:00:00'),
(11, 12, '2024-03-06 15:00:00'),
(13, 14, '2024-03-07 16:00:00'),
(15, 16, '2024-03-08 17:00:00'),
(17, 18, '2024-03-09 18:00:00'),
(19, 20, '2024-03-10 19:00:00'),
-- Additional matches - ensuring user1_id < user2_id  
(21, 22, '2024-03-11 10:00:00'),
(23, 24, '2024-03-12 11:00:00'),
(25, 26, '2024-03-13 12:00:00'),
(27, 28, '2024-03-14 13:00:00'),
(29, 30, '2024-03-15 14:00:00'),
(31, 32, '2024-03-16 15:00:00'),
(33, 34, '2024-03-17 16:00:00'),
(35, 36, '2024-03-18 17:00:00'),
(37, 38, '2024-03-19 18:00:00'),
(39, 40, '2024-03-20 19:00:00');

-- resources
insert into resource (resource_link, resource_type) values
('https://example.com/programming-tutorial', 'tutorial'),
('https://example.com/dataset.csv', 'dataset'),
('https://example.com/ai-research-paper.pdf', 'research paper'),
('https://example.com/software-design-patterns', 'guide'),
('https://example.com/interactive-coding-practice', 'platform');

-- sessions
insert into study_session (course_id, matched_student_id, study_type, session_date) values
(1, 1, 'group study', '2025-04-05'),
(2, 2, 'peer tutoring', '2025-04-06'),
(3, 3, 'project collaboration', '2025-04-07');

-- user resources
insert into user_resource (userid, resourceid) values
(1, 1),
(2, 2),
(3, 3),
(4, 1),
(4, 2),
(4, 3),
(5, 1),
(5, 4),
(5, 5);

-- user interests
insert into user_interests (userid, interestid) values
(1, 1),
(2, 2),
(3, 3);

-- Add some sample data for Emily's interests
insert into interests (description) values
('machine learning'),
('web development'),
('database management'),
('Software Engineering'),
('Web Development'),
('Data Structures');

-- Link Emily to her interests
insert into user_interests (userid, interestid) 
values (
    (SELECT userid FROM user WHERE email = 'emily.smith@example.com'),
    (SELECT interestid FROM interests WHERE description = 'Software Engineering')
);

-- Add Emily to a study group
insert into group_student (groupid, studentid)
values (
    1, -- CS Fundamentals group
    (SELECT userid FROM user WHERE email = 'emily.smith@example.com')
);

-- Insert all compatibilities
INSERT INTO compatibility (userid, academic_goals, learning_style, schedule_conflicts) VALUES
-- Original Compatibilities (1-10)
(1, 'Improve programming skills', 'Visual', 'None'),
(2, 'Master business concepts', 'Auditory', 'Monday mornings'),
(3, 'Excel in algorithms', 'Kinesthetic', 'None'),
(4, 'Understand finance', 'Visual', 'Friday afternoons'),
(5, 'Learn web development', 'Auditory', 'None'),
(6, 'Master supply chain', 'Kinesthetic', 'Wednesday evenings'),
(7, 'Study AI/ML', 'Visual', 'None'),
(8, 'Improve leadership', 'Auditory', 'Tuesday mornings'),
(9, 'Master databases', 'Kinesthetic', 'None'),
(10, 'Global business understanding', 'Visual', 'Thursday afternoons');

-- Note: matched_with data is now handled in the earlier section of the script

-- Insert all group memberships
INSERT INTO group_student (groupid, studentid) VALUES
-- CS 1800 Study Group (Group 1)
(1, 1), -- John Smith
(1, 3), -- Robert Williams
(1, 5), -- David Jones
-- Business Stats Team (Group 2)
(2, 2), -- Mary Johnson
(2, 4), -- Patricia Brown
(2, 6), -- Linda Garcia
-- Algorithms Study Group (Group 3)
(3, 3), -- Robert Williams
(3, 7), -- Michael Miller
(3, 9), -- James Moore
-- Marketing Project Team (Group 4)
(4, 4), -- Patricia Brown
(4, 8), -- Barbara Wilson
(4, 10), -- Margaret Taylor
-- OOD Study Group (Group 5)
(5, 5), -- David Jones
(5, 11), -- William Anderson
(5, 13), -- Charles Jackson
-- CS 3000 Study Group (Group 6)
(6, 21), -- Alex Smith
(6, 23), -- Matt Williams
(6, 25), -- Dylan Jones
-- Business Law Team (Group 7)
(7, 22), -- Emma Johnson
(7, 24), -- Sophia Brown
(7, 26), -- Lucas Garcia
-- Database Design Group (Group 8)
(8, 29), -- Julia Moore
(8, 31), -- Willow Anderson
(8, 33), -- Chloe Jackson
-- Web Dev Project Team (Group 9)
(9, 28), -- Ben Wilson
(9, 30), -- Max Taylor
(9, 32), -- Sam Thomas
-- AI Study Group (Group 10)
(10, 33), -- Chloe Jackson
(10, 35), -- Daisy Harris
(10, 37); -- Piper Lee 

-- SAMPLE DATA: 
USE study_buddy_system; 
-- Insert sample courses
INSERT INTO course (courseid, universityid, department, course_name) VALUES
-- Computer Science Courses
(1, 1, 'Computer Science', 'Discrete Structures'),
(2, 1, 'Computer Science', 'Algorithms and Data'),
(3, 1, 'Computer Science', 'Object-Oriented Design'),
(4, 1, 'Computer Science', 'Computer Systems'),
(5, 1, 'Computer Science', 'Theory of Computation'),
-- Business Courses
(6, 1, 'Business', 'Financial Accounting and Reporting'),
(7, 1, 'Business', 'Introduction to Marketing'),
(8, 1, 'Business', 'Supply Chain and Operations Management'),
(9, 1, 'Business', 'Organizational Behavior'),
(10, 1, 'Business', 'Business Statistics'),
-- Additional Computer Science Courses
(11, 1, 'Computer Science', 'Database Design'),
(12, 1, 'Computer Science', 'Web Development'),
(13, 1, 'Computer Science', 'Mobile Application Development'),
(14, 1, 'Computer Science', 'Artificial Intelligence'),
(15, 1, 'Computer Science', 'Machine Learning'),
-- Additional Business Courses
(16, 1, 'Business', 'Business Law'),
(17, 1, 'Business', 'Managerial Accounting'),
(18, 1, 'Business', 'Business Finance'),
(19, 1, 'Business', 'International Business'),
(20, 1, 'Business', 'Business Strategy');

-- Insert all user interests
INSERT INTO user_interests (userid, interestid) VALUES
-- Original Users (1-20)
(1, 1), -- Programming
(1, 2), -- Web Development
(2, 3), -- Database Management
(2, 1), -- Programming
(3, 2), -- Web Development
(3, 3), -- Database Management
(4, 1), -- Programming
(4, 2), -- Web Development
(5, 3), -- Database Management
(5, 1), -- Programming
(6, 2), -- Web Development
(6, 3), -- Database Management
(7, 1), -- Programming
(7, 2), -- Web Development
(8, 3), -- Database Management
(8, 1), -- Programming
(9, 2), -- Web Development
(9, 3), -- Database Management
(10, 1), -- Programming
(10, 2), -- Web Development
-- Additional Users (21-30)
(21, 1), -- Programming
(21, 2), -- Web Development
(22, 3), -- Database Management
(22, 1), -- Programming
(23, 2), -- Web Development
(23, 3), -- Database Management
(24, 1), -- Programming
(24, 2), -- Web Development
(25, 3), -- Database Management
(25, 1), -- Programming
(26, 2), -- Web Development
(26, 3), -- Database Management
(27, 1), -- Programming
(27, 2), -- Web Development
(28, 3), -- Database Management
(28, 1), -- Programming
(29, 2), -- Web Development
(29, 3), -- Database Management
(30, 1), -- Programming
(30, 2); -- Web Development

-- Insert all study groups
INSERT INTO study_group (groupid, group_name, student_id) VALUES
(1, 'CS 1800 Study Group', 1),
(2, 'Business Stats Team', 2),
(3, 'Algorithms Study Group', 3),
(4, 'Marketing Project Team', 4),
(5, 'OOD Study Group', 5),
(6, 'CS 3000 Study Group', 21),
(7, 'Business Law Team', 22),
(8, 'Database Design Group', 29),
(9, 'Web Dev Project Team', 28),
(10, 'AI Study Group', 33);

-- Insert all study sessions
INSERT INTO study_session (session_id, course_id, matched_student_id, study_type, session_date) VALUES
(1, 1, 1, 'Group Study', '2024-03-15'),
(2, 10, 2, 'Group Study', '2024-03-16'),
(3, 2, 3, 'Group Study', '2024-03-17'),
(4, 7, 4, 'Group Study', '2024-03-18'),
(5, 3, 5, 'Group Study', '2024-03-19'),
(6, 2, 21, 'Group Study', '2024-03-20'),
(7, 16, 22, 'Group Study', '2024-03-21'),
(8, 11, 29, 'Group Study', '2024-03-22'),
(9, 12, 28, 'Group Study', '2024-03-23'),
(10, 14, 33, 'Group Study', '2024-03-24');

-- Insert all compatibilities
INSERT INTO compatibility (userid, academic_goals, learning_style, schedule_conflicts) VALUES
-- Original Compatibilities (1-10)
(1, 'Improve programming skills', 'Visual', 'None'),
(2, 'Master business concepts', 'Auditory', 'Monday mornings'),
(3, 'Excel in algorithms', 'Kinesthetic', 'None'),
(4, 'Understand finance', 'Visual', 'Friday afternoons'),
(5, 'Learn web development', 'Auditory', 'None'),
(6, 'Master supply chain', 'Kinesthetic', 'Wednesday evenings'),
(7, 'Study AI/ML', 'Visual', 'None'),
(8, 'Improve leadership', 'Auditory', 'Tuesday mornings'),
(9, 'Master databases', 'Kinesthetic', 'None'),
(10, 'Global business understanding', 'Visual', 'Thursday afternoons');

-- Note: matched_with data is now handled in the earlier section of the script

-- Insert all group memberships 