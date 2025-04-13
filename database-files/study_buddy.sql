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
    email varchar(255) not null unique
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
    groupid int auto_increment primary key
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
    availability varchar(255),
    groupid int,
    foreign key (groupid) references study_group(groupid)
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

-- data

-- admin
insert into admin (name, role, email) values
('john doe', 'system administrator', 'john.doe@example.com'),
('jane smith', 'content manager', 'jane.smith@example.com'),
('robert johnson', 'support specialist', 'robert.johnson@example.com');

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

-- users
insert into user (name, email, password, major, learning_style, availability, groupid) values
('alice williams', 'alice.williams@example.com', 'password123', 'computer science', 'visual', 'evenings and weekends', 1),
('bob brown', 'bob.brown@example.com', 'password456', 'data science', 'auditory', 'weekdays', 2),
('charlie davis', 'charlie.davis@example.com', 'password789', 'artificial intelligence', 'kinesthetic', 'flexible', 3);

-- update groups
update study_group set student_id = 1 where groupid = 1;
update study_group set student_id = 2 where groupid = 2;
update study_group set student_id = 3 where groupid = 3;

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

-- resources
insert into resource (resource_link, resource_type) values
('https://example.com/programming-tutorial', 'tutorial'),
('https://example.com/dataset.csv', 'dataset'),
('https://example.com/ai-research-paper.pdf', 'research paper');

-- sessions
insert into study_session (course_id, matched_student_id, study_type, session_date) values
(1, 1, 'group study', '2025-04-05'),
(2, 2, 'peer tutoring', '2025-04-06'),
(3, 3, 'project collaboration', '2025-04-07');

-- user resources
insert into user_resource (userid, resourceid) values
(1, 1),
(2, 2),
(3, 3);

-- user interests
insert into user_interests (userid, interestid) values
(1, 1),
(2, 2),
(3, 3);
