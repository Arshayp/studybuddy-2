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

-- Insert all users (1-150)
INSERT INTO user (userid, name, email, password, major, learning_style, availability) VALUES
-- Original Users (1-20)
(1, 'John Smith', 'john.smith@northeastern.edu', 'hashed_password_1', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
(2, 'Mary Johnson', 'mary.johnson@northeastern.edu', 'hashed_password_2', 'Psychology', 'Auditory', 'Weekday Mornings'),
(3, 'Robert Williams', 'robert.williams@northeastern.edu', 'hashed_password_3', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
(4, 'Patricia Brown', 'patricia.brown@northeastern.edu', 'hashed_password_4', 'International Business', 'Visual', 'Weekday Evenings'),
(5, 'David Jones', 'david.jones@northeastern.edu', 'hashed_password_5', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
(6, 'Linda Garcia', 'linda.garcia@northeastern.edu', 'hashed_password_6', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
(7, 'Michael Miller', 'michael.miller@northeastern.edu', 'hashed_password_7', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
(8, 'Barbara Wilson', 'barbara.wilson@northeastern.edu', 'hashed_password_8', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
(9, 'James Moore', 'james.moore@northeastern.edu', 'hashed_password_9', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
(10, 'Margaret Taylor', 'margaret.taylor@northeastern.edu', 'hashed_password_10', 'Business Administration', 'Visual', 'Weekday Evenings'),
(11, 'William Anderson', 'william.anderson@northeastern.edu', 'hashed_password_11', 'Computer Science and Biology', 'Auditory', 'Weekday Mornings'),
(12, 'Sarah Thomas', 'sarah.thomas@northeastern.edu', 'hashed_password_12', 'Health Science', 'Kinesthetic', 'Flexible'),
(13, 'Charles Jackson', 'charles.jackson@northeastern.edu', 'hashed_password_13', 'Computer Science and Game Design', 'Visual', 'Weekday Evenings'),
(14, 'Karen White', 'karen.white@northeastern.edu', 'hashed_password_14', 'Business Analytics', 'Auditory', 'Weekday Mornings'),
(15, 'Daniel Harris', 'daniel.harris@northeastern.edu', 'hashed_password_15', 'Computer Science and Music Technology', 'Kinesthetic', 'Flexible'),
(16, 'Jennifer Martin', 'jennifer.martin@northeastern.edu', 'hashed_password_16', 'Entrepreneurship and Innovation', 'Visual', 'Weekday Evenings'),
(17, 'Paul Lee', 'paul.lee@northeastern.edu', 'hashed_password_17', 'Computer Science and Design', 'Auditory', 'Weekday Mornings'),
(18, 'Nancy Thompson', 'nancy.thompson@northeastern.edu', 'hashed_password_18', 'Supply Chain Management', 'Kinesthetic', 'Flexible'),
(19, 'Kevin Clark', 'kevin.clark@northeastern.edu', 'hashed_password_19', 'Computer Science and Environmental Science', 'Visual', 'Weekday Evenings'),
(20, 'Laura Rodriguez', 'laura.rodriguez@northeastern.edu', 'hashed_password_20', 'International Affairs', 'Auditory', 'Weekday Mornings'),
-- Additional Users (21-150)
(21, 'Alex Smith', 'alex.smith@northeastern.edu', 'hashed_password_21', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
(22, 'Emma Johnson', 'emma.johnson@northeastern.edu', 'hashed_password_22', 'Neuroscience', 'Auditory', 'Weekday Mornings'),
(23, 'Matt Williams', 'matt.williams@northeastern.edu', 'hashed_password_23', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
(24, 'Sophia Brown', 'sophia.brown@northeastern.edu', 'hashed_password_24', 'International Business', 'Visual', 'Weekday Evenings'),
(25, 'Dylan Jones', 'dylan.jones@northeastern.edu', 'hashed_password_25', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
(26, 'Lucas Garcia', 'lucas.garcia@northeastern.edu', 'hashed_password_26', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
(27, 'Mia Miller', 'mia.miller@northeastern.edu', 'hashed_password_27', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
(28, 'Ben Wilson', 'ben.wilson@northeastern.edu', 'hashed_password_28', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
(29, 'Julia Moore', 'julia.moore@northeastern.edu', 'hashed_password_29', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
(30, 'Max Taylor', 'max.taylor@northeastern.edu', 'hashed_password_30', 'Business Administration', 'Visual', 'Weekday Evenings'),
(31, 'Willow Anderson', 'willow.anderson@northeastern.edu', 'hashed_password_31', 'Computer Science and Biology', 'Auditory', 'Weekday Mornings'),
(32, 'Sam Thomas', 'sam.thomas@northeastern.edu', 'hashed_password_32', 'Health Science', 'Kinesthetic', 'Flexible'),
(33, 'Chloe Jackson', 'chloe.jackson@northeastern.edu', 'hashed_password_33', 'Computer Science and Game Design', 'Visual', 'Weekday Evenings'),
(34, 'Kyle White', 'kyle.white@northeastern.edu', 'hashed_password_34', 'Business Analytics', 'Auditory', 'Weekday Mornings'),
(35, 'Daisy Harris', 'daisy.harris@northeastern.edu', 'hashed_password_35', 'Computer Science and Music Technology', 'Kinesthetic', 'Flexible'),
(36, 'Jack Martin', 'jack.martin@northeastern.edu', 'hashed_password_36', 'Entrepreneurship and Innovation', 'Visual', 'Weekday Evenings'),
(37, 'Piper Lee', 'piper.lee@northeastern.edu', 'hashed_password_37', 'Computer Science and Design', 'Auditory', 'Weekday Mornings'),
(38, 'Noah Thompson', 'noah.thompson@northeastern.edu', 'hashed_password_38', 'Supply Chain Management', 'Kinesthetic', 'Flexible'),
(39, 'Kate Clark', 'kate.clark@northeastern.edu', 'hashed_password_39', 'Computer Science and Environmental Science', 'Visual', 'Weekday Evenings'),
(40, 'Liam Rodriguez', 'liam.rodriguez@northeastern.edu', 'hashed_password_40', 'International Affairs', 'Auditory', 'Weekday Mornings'),
(41, 'Ryan Green', 'ryan.green@northeastern.edu', 'hashed_password_41', 'Computer Science and Business', 'Kinesthetic', 'Flexible'),
(42, 'Ava Hall', 'ava.hall@northeastern.edu', 'hashed_password_42', 'Biochemistry', 'Visual', 'Weekday Evenings'),
(43, 'James Wright', 'james.wright@northeastern.edu', 'hashed_password_43', 'Computer Science and Mathematics', 'Auditory', 'Weekday Mornings'),
(44, 'Sarah Lee', 'sarah.lee@northeastern.edu', 'hashed_password_44', 'International Business', 'Kinesthetic', 'Flexible'),
(45, 'Michael King', 'michael.king@northeastern.edu', 'hashed_password_45', 'Computer Science and Cognitive Psychology', 'Visual', 'Weekday Evenings'),
(46, 'Lily Scott', 'lily.scott@northeastern.edu', 'hashed_password_46', 'Finance and Accounting', 'Auditory', 'Weekday Mornings'),
(47, 'Daniel Nguyen', 'daniel.nguyen@northeastern.edu', 'hashed_password_47', 'Computer Science and Physics', 'Kinesthetic', 'Flexible'),
(48, 'Hannah Kim', 'hannah.kim@northeastern.edu', 'hashed_password_48', 'Marketing and Communications', 'Visual', 'Weekday Evenings'),
(49, 'Jason Chen', 'jason.chen@northeastern.edu', 'hashed_password_49', 'Computer Science and Economics', 'Auditory', 'Weekday Mornings'),
(50, 'Megan Wang', 'megan.wang@northeastern.edu', 'hashed_password_50', 'Business Administration', 'Kinesthetic', 'Flexible'),
(51, 'Tyler Li', 'tyler.li@northeastern.edu', 'hashed_password_51', 'Computer Science and Biology', 'Visual', 'Weekday Evenings'),
(52, 'Rachel Patel', 'rachel.patel@northeastern.edu', 'hashed_password_52', 'Health Science', 'Auditory', 'Weekday Mornings'),
(53, 'Kevin Singh', 'kevin.singh@northeastern.edu', 'hashed_password_53', 'Computer Science and Game Design', 'Kinesthetic', 'Flexible'),
(54, 'Priya Gupta', 'priya.gupta@northeastern.edu', 'hashed_password_54', 'Business Analytics', 'Visual', 'Weekday Evenings'),
(55, 'David Shah', 'david.shah@northeastern.edu', 'hashed_password_55', 'Computer Science and Music Technology', 'Auditory', 'Weekday Mornings'),
(56, 'Sneha Desai', 'sneha.desai@northeastern.edu', 'hashed_password_56', 'Entrepreneurship and Innovation', 'Kinesthetic', 'Flexible'),
(57, 'Rahul Mehta', 'rahul.mehta@northeastern.edu', 'hashed_password_57', 'Computer Science and Design', 'Visual', 'Weekday Evenings'),
(58, 'Neha Sharma', 'neha.sharma@northeastern.edu', 'hashed_password_58', 'Supply Chain Management', 'Auditory', 'Weekday Mornings'),
(59, 'Arjun Kumar', 'arjun.kumar@northeastern.edu', 'hashed_password_59', 'Computer Science and Environmental Science', 'Kinesthetic', 'Flexible'),
(60, 'Pooja Verma', 'pooja.verma@northeastern.edu', 'hashed_password_60', 'International Affairs', 'Visual', 'Weekday Evenings'),
(61, 'Ravi Reddy', 'ravi.reddy@northeastern.edu', 'hashed_password_61', 'Computer Science and Business', 'Auditory', 'Weekday Mornings'),
(62, 'Sneha Rao', 'sneha.rao@northeastern.edu', 'hashed_password_62', 'Chemical Engineering', 'Kinesthetic', 'Flexible'),
(63, 'Vijay Patel', 'vijay.patel@northeastern.edu', 'hashed_password_63', 'Computer Science and Mathematics', 'Visual', 'Weekday Evenings'),
(64, 'Priyanka Desai', 'priyanka.desai@northeastern.edu', 'hashed_password_64', 'International Business', 'Auditory', 'Weekday Mornings'),
(65, 'Meera Reddy', 'meera.reddy@northeastern.edu', 'hashed_password_65', 'Computer Science and Cognitive Psychology', 'Kinesthetic', 'Flexible'),
(66, 'Sanjay Rao', 'sanjay.rao@northeastern.edu', 'hashed_password_66', 'Finance and Accounting', 'Visual', 'Weekday Evenings'),
(67, 'Riya Patel', 'riya.patel@northeastern.edu', 'hashed_password_67', 'Computer Science and Physics', 'Auditory', 'Weekday Mornings'),
(68, 'Anita Desai', 'anita.desai@northeastern.edu', 'hashed_password_68', 'Marketing and Communications', 'Kinesthetic', 'Flexible'),
(69, 'Vikram Reddy', 'vikram.reddy@northeastern.edu', 'hashed_password_69', 'Computer Science and Economics', 'Visual', 'Weekday Evenings'),
(70, 'Pooja Rao', 'pooja.rao@northeastern.edu', 'hashed_password_70', 'Business Administration', 'Auditory', 'Weekday Mornings'),
(71, 'Rahul Patel', 'rahul.patel@northeastern.edu', 'hashed_password_71', 'Computer Science and Biology', 'Kinesthetic', 'Flexible'),
(72, 'Sonia Desai', 'sonia.desai@northeastern.edu', 'hashed_password_72', 'Health Science', 'Visual', 'Weekday Evenings'),
(73, 'Anand Reddy', 'anand.reddy@northeastern.edu', 'hashed_password_73', 'Computer Science and Game Design', 'Auditory', 'Weekday Mornings'),
(74, 'Priya Rao', 'priya.rao@northeastern.edu', 'hashed_password_74', 'Business Analytics', 'Kinesthetic', 'Flexible'),
(75, 'Vivek Patel', 'vivek.patel@northeastern.edu', 'hashed_password_75', 'Computer Science and Music Technology', 'Visual', 'Weekday Evenings'),
(76, 'Sanjay Desai', 'sanjay.desai@northeastern.edu', 'hashed_password_76', 'Entrepreneurship and Innovation', 'Auditory', 'Weekday Mornings'),
(77, 'Riya Reddy', 'riya.reddy@northeastern.edu', 'hashed_password_77', 'Computer Science and Design', 'Kinesthetic', 'Flexible'),
(78, 'Anita Rao', 'anita.rao@northeastern.edu', 'hashed_password_78', 'Supply Chain Management', 'Visual', 'Weekday Evenings'),
(79, 'Vikram Patel', 'vikram.patel@northeastern.edu', 'hashed_password_79', 'Computer Science and Environmental Science', 'Auditory', 'Weekday Mornings'),
(80, 'Pooja Desai', 'pooja.desai@northeastern.edu', 'hashed_password_80', 'International Affairs', 'Kinesthetic', 'Flexible'),
(81, 'Ravi Reddy', 'ravi.reddy@northeastern.edu', 'hashed_password_81', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
(82, 'Sneha Rao', 'sneha.rao@northeastern.edu', 'hashed_password_82', 'Mechanical Engineering', 'Auditory', 'Weekday Mornings'),
(83, 'Vijay Patel', 'vijay.patel@northeastern.edu', 'hashed_password_83', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
(84, 'Priyanka Desai', 'priyanka.desai@northeastern.edu', 'hashed_password_84', 'International Business', 'Visual', 'Weekday Evenings'),
(85, 'Meera Reddy', 'meera.reddy@northeastern.edu', 'hashed_password_85', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
(86, 'Sanjay Rao', 'sanjay.rao@northeastern.edu', 'hashed_password_86', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
(87, 'Riya Patel', 'riya.patel@northeastern.edu', 'hashed_password_87', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
(88, 'Anita Desai', 'anita.desai@northeastern.edu', 'hashed_password_88', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
(89, 'Vikram Reddy', 'vikram.reddy@northeastern.edu', 'hashed_password_89', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
(90, 'Pooja Rao', 'pooja.rao@northeastern.edu', 'hashed_password_90', 'Business Administration', 'Visual', 'Weekday Evenings'),
(91, 'Rahul Patel', 'rahul.patel@northeastern.edu', 'hashed_password_91', 'Computer Science and Biology', 'Auditory', 'Weekday Mornings'),
(92, 'Sonia Desai', 'sonia.desai@northeastern.edu', 'hashed_password_92', 'Health Science', 'Kinesthetic', 'Flexible'),
(93, 'Anand Reddy', 'anand.reddy@northeastern.edu', 'hashed_password_93', 'Computer Science and Game Design', 'Visual', 'Weekday Evenings'),
(94, 'Priya Rao', 'priya.rao@northeastern.edu', 'hashed_password_94', 'Business Analytics', 'Auditory', 'Weekday Mornings'),
(95, 'Vivek Patel', 'vivek.patel@northeastern.edu', 'hashed_password_95', 'Computer Science and Music Technology', 'Kinesthetic', 'Flexible'),
(96, 'Sanjay Desai', 'sanjay.desai@northeastern.edu', 'hashed_password_96', 'Entrepreneurship and Innovation', 'Visual', 'Weekday Evenings'),
(97, 'Riya Reddy', 'riya.reddy@northeastern.edu', 'hashed_password_97', 'Computer Science and Design', 'Auditory', 'Weekday Mornings'),
(98, 'Anita Rao', 'anita.rao@northeastern.edu', 'hashed_password_98', 'Supply Chain Management', 'Kinesthetic', 'Flexible'),
(99, 'Vikram Patel', 'vikram.patel@northeastern.edu', 'hashed_password_99', 'Computer Science and Environmental Science', 'Visual', 'Weekday Evenings'),
(100, 'Pooja Desai', 'pooja.desai@northeastern.edu', 'hashed_password_100', 'International Affairs', 'Auditory', 'Weekday Mornings'),
(101, 'Ravi Reddy', 'ravi.reddy@northeastern.edu', 'hashed_password_101', 'Computer Science and Business', 'Kinesthetic', 'Flexible'),
(102, 'Sneha Rao', 'sneha.rao@northeastern.edu', 'hashed_password_102', 'Electrical Engineering', 'Visual', 'Weekday Evenings'),
(103, 'Vijay Patel', 'vijay.patel@northeastern.edu', 'hashed_password_103', 'Computer Science and Mathematics', 'Auditory', 'Weekday Mornings'),
(104, 'Priyanka Desai', 'priyanka.desai@northeastern.edu', 'hashed_password_104', 'International Business', 'Kinesthetic', 'Flexible'),
(105, 'Meera Reddy', 'meera.reddy@northeastern.edu', 'hashed_password_105', 'Computer Science and Cognitive Psychology', 'Visual', 'Weekday Evenings'),
(106, 'Sanjay Rao', 'sanjay.rao@northeastern.edu', 'hashed_password_106', 'Finance and Accounting', 'Auditory', 'Weekday Mornings'),
(107, 'Riya Patel', 'riya.patel@northeastern.edu', 'hashed_password_107', 'Computer Science and Physics', 'Kinesthetic', 'Flexible'),
(108, 'Anita Desai', 'anita.desai@northeastern.edu', 'hashed_password_108', 'Marketing and Communications', 'Visual', 'Weekday Evenings'),
(109, 'Vikram Reddy', 'vikram.reddy@northeastern.edu', 'hashed_password_109', 'Computer Science and Economics', 'Auditory', 'Weekday Mornings'),
(110, 'Pooja Rao', 'pooja.rao@northeastern.edu', 'hashed_password_110', 'Business Administration', 'Kinesthetic', 'Flexible'),
(111, 'Rahul Patel', 'rahul.patel@northeastern.edu', 'hashed_password_111', 'Computer Science and Biology', 'Visual', 'Weekday Evenings'),
(112, 'Sonia Desai', 'sonia.desai@northeastern.edu', 'hashed_password_112', 'Health Science', 'Auditory', 'Weekday Mornings'),
(113, 'Anand Reddy', 'anand.reddy@northeastern.edu', 'hashed_password_113', 'Computer Science and Game Design', 'Kinesthetic', 'Flexible'),
(114, 'Priya Rao', 'priya.rao@northeastern.edu', 'hashed_password_114', 'Business Analytics', 'Visual', 'Weekday Evenings'),
(115, 'Vivek Patel', 'vivek.patel@northeastern.edu', 'hashed_password_115', 'Computer Science and Music Technology', 'Auditory', 'Weekday Mornings'),
(116, 'Sanjay Desai', 'sanjay.desai@northeastern.edu', 'hashed_password_116', 'Entrepreneurship and Innovation', 'Kinesthetic', 'Flexible'),
(117, 'Riya Reddy', 'riya.reddy@northeastern.edu', 'hashed_password_117', 'Computer Science and Design', 'Visual', 'Weekday Evenings'),
(118, 'Anita Rao', 'anita.rao@northeastern.edu', 'hashed_password_118', 'Supply Chain Management', 'Auditory', 'Weekday Mornings'),
(119, 'Vikram Patel', 'vikram.patel@northeastern.edu', 'hashed_password_119', 'Computer Science and Environmental Science', 'Kinesthetic', 'Flexible'),
(120, 'Pooja Desai', 'pooja.desai@northeastern.edu', 'hashed_password_120', 'International Affairs', 'Visual', 'Weekday Evenings'),
(121, 'Ravi Reddy', 'ravi.reddy@northeastern.edu', 'hashed_password_121', 'Computer Science and Business', 'Auditory', 'Weekday Mornings'),
(122, 'Sneha Rao', 'sneha.rao@northeastern.edu', 'hashed_password_122', 'Civil Engineering', 'Kinesthetic', 'Flexible'),
(123, 'Vijay Patel', 'vijay.patel@northeastern.edu', 'hashed_password_123', 'Computer Science and Mathematics', 'Visual', 'Weekday Evenings'),
(124, 'Priyanka Desai', 'priyanka.desai@northeastern.edu', 'hashed_password_124', 'International Business', 'Auditory', 'Weekday Mornings'),
(125, 'Meera Reddy', 'meera.reddy@northeastern.edu', 'hashed_password_125', 'Computer Science and Cognitive Psychology', 'Kinesthetic', 'Flexible'),
(126, 'Sanjay Rao', 'sanjay.rao@northeastern.edu', 'hashed_password_126', 'Finance and Accounting', 'Visual', 'Weekday Evenings'),
(127, 'Riya Patel', 'riya.patel@northeastern.edu', 'hashed_password_127', 'Computer Science and Physics', 'Auditory', 'Weekday Mornings'),
(128, 'Anita Desai', 'anita.desai@northeastern.edu', 'hashed_password_128', 'Marketing and Communications', 'Kinesthetic', 'Flexible'),
(129, 'Vikram Reddy', 'vikram.reddy@northeastern.edu', 'hashed_password_129', 'Computer Science and Economics', 'Visual', 'Weekday Evenings'),
(130, 'Pooja Rao', 'pooja.rao@northeastern.edu', 'hashed_password_130', 'Business Administration', 'Auditory', 'Weekday Mornings'),
(131, 'Rahul Patel', 'rahul.patel@northeastern.edu', 'hashed_password_131', 'Computer Science and Biology', 'Kinesthetic', 'Flexible'),
(132, 'Sonia Desai', 'sonia.desai@northeastern.edu', 'hashed_password_132', 'Health Science', 'Visual', 'Weekday Evenings'),
(133, 'Anand Reddy', 'anand.reddy@northeastern.edu', 'hashed_password_133', 'Computer Science and Game Design', 'Auditory', 'Weekday Mornings'),
(134, 'Priya Rao', 'priya.rao@northeastern.edu', 'hashed_password_134', 'Business Analytics', 'Kinesthetic', 'Flexible'),
(135, 'Vivek Patel', 'vivek.patel@northeastern.edu', 'hashed_password_135', 'Computer Science and Music Technology', 'Visual', 'Weekday Evenings'),
(136, 'Sanjay Desai', 'sanjay.desai@northeastern.edu', 'hashed_password_136', 'Entrepreneurship and Innovation', 'Auditory', 'Weekday Mornings'),
(137, 'Riya Reddy', 'riya.reddy@northeastern.edu', 'hashed_password_137', 'Computer Science and Design', 'Kinesthetic', 'Flexible'),
(138, 'Anita Rao', 'anita.rao@northeastern.edu', 'hashed_password_138', 'Supply Chain Management', 'Visual', 'Weekday Evenings'),
(139, 'Vikram Patel', 'vikram.patel@northeastern.edu', 'hashed_password_139', 'Computer Science and Environmental Science', 'Auditory', 'Weekday Mornings'),
(140, 'Pooja Desai', 'pooja.desai@northeastern.edu', 'hashed_password_140', 'International Affairs', 'Kinesthetic', 'Flexible'),
(141, 'Ravi Reddy', 'ravi.reddy@northeastern.edu', 'hashed_password_141', 'Computer Science and Business', 'Visual', 'Weekday Evenings'),
(142, 'Sneha Rao', 'sneha.rao@northeastern.edu', 'hashed_password_142', 'Industrial Engineering', 'Auditory', 'Weekday Mornings'),
(143, 'Vijay Patel', 'vijay.patel@northeastern.edu', 'hashed_password_143', 'Computer Science and Mathematics', 'Kinesthetic', 'Flexible'),
(144, 'Priyanka Desai', 'priyanka.desai@northeastern.edu', 'hashed_password_144', 'International Business', 'Visual', 'Weekday Evenings'),
(145, 'Meera Reddy', 'meera.reddy@northeastern.edu', 'hashed_password_145', 'Computer Science and Cognitive Psychology', 'Auditory', 'Weekday Mornings'),
(146, 'Sanjay Rao', 'sanjay.rao@northeastern.edu', 'hashed_password_146', 'Finance and Accounting', 'Kinesthetic', 'Flexible'),
(147, 'Riya Patel', 'riya.patel@northeastern.edu', 'hashed_password_147', 'Computer Science and Physics', 'Visual', 'Weekday Evenings'),
(148, 'Anita Desai', 'anita.desai@northeastern.edu', 'hashed_password_148', 'Marketing and Communications', 'Auditory', 'Weekday Mornings'),
(149, 'Vikram Reddy', 'vikram.reddy@northeastern.edu', 'hashed_password_149', 'Computer Science and Economics', 'Kinesthetic', 'Flexible'),
(150, 'Pooja Rao', 'pooja.rao@northeastern.edu', 'hashed_password_150', 'Business Administration', 'Visual', 'Weekday Evenings');

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

-- Insert all matches
INSERT INTO matched_with (user1_id, user2_id, match_date) VALUES
-- Original Users (1-20)
(1, 2, '2024-03-01 10:00:00'),
(3, 4, '2024-03-02 11:00:00'),
(5, 6, '2024-03-03 12:00:00'),
(7, 8, '2024-03-04 13:00:00'),
(9, 10, '2024-03-05 14:00:00'),
(11, 12, '2024-03-06 15:00:00'),
(13, 14, '2024-03-07 16:00:00'),
(15, 16, '2024-03-08 17:00:00'),
(17, 18, '2024-03-09 18:00:00'),
(19, 20, '2024-03-10 19:00:00'),
-- Additional Users (21-30)
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