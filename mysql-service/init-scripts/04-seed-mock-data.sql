INSERT INTO Users (Name, Email, Password, Role_ID) VALUES
('Alice Johnson', 'alice.johnson@educaplan.com', 'alice123', 1),
('Bob Smith', 'bob.smith@educaplan.com', 'bob123', 2),
('Charlie Brown', 'charlie.brown@educaplan.com', 'charlie123', 3),
('Diana Prince', 'diana.prince@educaplan.com', 'diana123', 3),
('Evan Wright', 'evan.wright@educaplan.com', 'evan123', 2),
('Fiona Taylor', 'fiona.taylor@educaplan.com', 'fiona123', 3),
('George Hill', 'george.hill@educaplan.com', 'george123', 3),
('Hannah Lewis', 'hannah.lewis@educaplan.com', 'hannah123', 2),
('Ian Clark', 'ian.clark@educaplan.com', 'ian123', 3),
('Julia Scott', 'julia.scott@educaplan.com', 'julia123', 3);

INSERT INTO Entities (Name, Type) VALUES
('Educaplan University', 'University'),
('Tech Academy', 'Training Center'),
('Language Learning Hub', 'Institute'),
('Data Science Institute', 'Institute'),
('Creative Coding School', 'Bootcamp');

INSERT INTO Courses (Name, Description, Entity_ID) VALUES
('Introduction to Programming', 'Learn the basics of programming.', 1),
('Web Development Bootcamp', 'Comprehensive web development course.', 2),
('Advanced English Grammar', 'Master complex English grammar.', 3),
('Data Analysis 101', 'Learn the fundamentals of data analysis.', 4),
('Creative Coding for Beginners', 'Explore creative projects with coding.', 5);

INSERT INTO Modules (Name, Description, Course_ID) VALUES
('Programming Fundamentals', 'Basics of programming languages.', 1),
('HTML and CSS', 'Learn to create websites using HTML and CSS.', 2),
('Grammar Structures', 'Focus on advanced grammar structures.', 3),
('Excel for Data Analysis', 'Using Excel for data processing.', 4),
('Introduction to Creative Coding', 'Build fun projects with code.', 5),
('JavaScript Essentials', 'Learn the basics of JavaScript.', 2),
('Python for Data Science', 'Dive into Python for data analysis.', 4);

INSERT INTO Topics (Name, Description, Module_ID) VALUES
('Variables and Data Types', 'Understanding basic variables.', 1),
('Flexbox and Grid', 'Learn modern CSS layout techniques.', 2),
('Complex Sentences', 'Dependent and independent clauses.', 3),
('Data Cleaning in Excel', 'Techniques for cleaning datasets.', 4),
('Canvas Basics', 'Drawing with the HTML5 Canvas API.', 5),
('Loops and Conditionals', 'Control flow in JavaScript.', 6),
('Pandas Library', 'Using Pandas for data manipulation.', 7);

INSERT INTO Materials (Name, Type, URL, Topic_ID) VALUES
('Variables Tutorial', 'Document', 'https://docs.variables.com', 1),
('Flexbox Guide', 'Video', 'https://videos.flexbox.com', 2),
('Grammar Workbook', 'Document', 'https://docs.grammarworkbook.com', 3),
('Excel Cleaning Cheatsheet', 'Document', 'https://docs.excelcleaning.com', 4),
('Canvas Drawing Video', 'Video', 'https://videos.canvasdrawing.com', 5),
('JavaScript Loops PDF', 'Document', 'https://docs.javascriptloops.com', 6),
('Pandas DataFrame Basics', 'Video', 'https://videos.pandasdf.com', 7);

INSERT INTO Sessions (Date_Time, Duration, Module_ID) VALUES
('2024-12-10 10:00:00', 120, 1),
('2024-12-11 14:00:00', 90, 2),
('2024-12-12 09:00:00', 60, 3),
('2024-12-13 15:00:00', 150, 4),
('2024-12-14 11:00:00', 120, 5),
('2024-12-15 13:00:00', 180, 6),
('2024-12-16 10:30:00', 200, 7);

INSERT INTO Users_Courses (User_ID, Course_ID, Enrollment_Date) VALUES
(3, 1, '2024-01-15'),
(4, 2, '2024-02-20'),
(5, 3, '2024-03-10'),
(6, 4, '2024-04-05'),
(7, 5, '2024-05-01');

INSERT INTO Students (Student_ID, Student_Number) VALUES
(3, 'S2024-001'),
(4, 'S2024-002'),
(5, 'S2024-003'),
(6, 'S2024-004'),
(7, 'S2024-005');

INSERT INTO Attendance (Student_ID, Session_ID, Status) VALUES
(3, 1, 'Present'),
(4, 2, 'Absent'),
(5, 3, 'Late'),
(6, 4, 'Present'),
(7, 5, 'Present');

INSERT INTO Feedback (Student_ID, Module_ID, Comment, Rating, Feedback_Date) VALUES
(3, 1, 'Great module for beginners!', 5, '2024-12-11'),
(4, 2, 'Well-paced and thorough.', 4, '2024-12-12'),
(5, 3, 'Too fast for me.', 3, '2024-12-13'),
(6, 4, 'Very practical and insightful.', 5, '2024-12-14'),
(7, 5, 'Enjoyable creative projects.', 5, '2024-12-15');

INSERT INTO Progress (Student_ID, Module_ID, Completion_Percentage, Last_Updated) VALUES
(3, 1, 75.00, '2024-12-15'),
(4, 2, 50.00, '2024-12-16'),
(5, 3, 90.00, '2024-12-17'),
(6, 4, 85.00, '2024-12-18'),
(7, 5, 100.00, '2024-12-19');

INSERT INTO Grades (Student_ID, Module_ID, Grade, Assessment_Date) VALUES
(3, 1, 85.50, '2024-12-20'),
(4, 2, 70.00, '2024-12-21'),
(5, 3, 92.00, '2024-12-22'),
(6, 4, 88.00, '2024-12-23'),
(7, 5, 95.00, '2024-12-24');
