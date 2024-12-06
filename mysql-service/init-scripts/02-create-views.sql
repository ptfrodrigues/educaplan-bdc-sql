CREATE OR REPLACE VIEW Users_View AS
SELECT 
    u.User_ID,
    u.Name,
    u.Email,
    r.Name AS Role_Name,
    u.last_login
FROM Users u
LEFT JOIN Roles r ON u.Role_ID = r.Role_ID;

CREATE OR REPLACE VIEW Roles_View AS
SELECT * FROM Roles;

CREATE OR REPLACE VIEW Courses_View AS
SELECT 
    c.Course_ID,
    c.Name,
    c.Description,
    e.Name AS Entity_Name
FROM Courses c
LEFT JOIN Entities e ON c.Entity_ID = e.Entity_ID;

CREATE OR REPLACE VIEW Modules_View AS
SELECT 
    m.Module_ID,
    m.Name,
    m.Description,
    c.Name AS Course_Name
FROM Modules m
LEFT JOIN Courses c ON m.Course_ID = c.Course_ID;

CREATE OR REPLACE VIEW Topics_View AS
SELECT 
    t.Topic_ID,
    t.Name,
    t.Description,
    m.Name AS Module_Name
FROM Topics t
LEFT JOIN Modules m ON t.Module_ID = m.Module_ID;

CREATE OR REPLACE VIEW Materials_View AS
SELECT 
    m.Material_ID,
    m.Name,
    m.Type,
    m.URL,
    t.Name AS Topic_Name
FROM Materials m
LEFT JOIN Topics t ON m.Topic_ID = t.Topic_ID;

CREATE OR REPLACE VIEW Students_View AS
SELECT 
    s.Student_ID,
    s.Student_Number,
    u.Name,
    u.Email
FROM Students s
LEFT JOIN Users u ON s.Student_ID = u.User_ID;

CREATE OR REPLACE VIEW Attendance_View AS
SELECT 
    a.Attendance_ID,
    u.Name AS Student_Name,
    ses.Date_Time AS Session_DateTime,
    m.Name AS Module_Name,
    a.Status
FROM Attendance a
LEFT JOIN Students st ON a.Student_ID = st.Student_ID
LEFT JOIN Users u ON st.Student_ID = u.User_ID
LEFT JOIN Sessions ses ON a.Session_ID = ses.Session_ID
LEFT JOIN Modules m ON ses.Module_ID = m.Module_ID;

CREATE OR REPLACE VIEW Feedback_View AS
SELECT 
    f.Feedback_ID,
    u.Name AS Student_Name,
    m.Name AS Module_Name,
    f.Comment,
    f.Rating,
    f.Feedback_Date
FROM Feedback f
LEFT JOIN Students st ON f.Student_ID = st.Student_ID
LEFT JOIN Users u ON st.Student_ID = u.User_ID
LEFT JOIN Modules m ON f.Module_ID = m.Module_ID;

CREATE OR REPLACE VIEW Progress_View AS
SELECT 
    p.Progress_ID,
    u.Name AS Student_Name,
    m.Name AS Module_Name,
    p.Completion_Percentage,
    p.Last_Updated
FROM Progress p
LEFT JOIN Students st ON p.Student_ID = st.Student_ID
LEFT JOIN Users u ON st.Student_ID = u.User_ID
LEFT JOIN Modules m ON p.Module_ID = m.Module_ID;

CREATE OR REPLACE VIEW Grades_View AS
SELECT 
    g.Grade_ID,
    u.Name AS Student_Name,
    m.Name AS Module_Name,
    g.Grade,
    g.Assessment_Date
FROM Grades g
LEFT JOIN Students st ON g.Student_ID = st.Student_ID
LEFT JOIN Users u ON st.Student_ID = u.User_ID
LEFT JOIN Modules m ON g.Module_ID = m.Module_ID;

CREATE OR REPLACE VIEW My_Courses_View AS
SELECT 
    c.Course_ID,
    c.Name AS Course_Name,
    c.Description,
    uc.Enrollment_Date
FROM Users_Courses uc
LEFT JOIN Courses c ON uc.Course_ID = c.Course_ID;

CREATE OR REPLACE VIEW Sessions_View AS
SELECT 
    s.Session_ID,
    s.Date_Time,
    s.Duration,
    m.Name AS Module_Name
FROM Sessions s
LEFT JOIN Modules m ON s.Module_ID = m.Module_ID;

CREATE OR REPLACE VIEW Recent_User_Activity AS
SELECT 
    u.User_ID,
    u.Name,
    u.Email,
    r.Name AS Role_Name,
    u.last_login,
    CASE 
        WHEN u.last_login > DATE_SUB(NOW(), INTERVAL 1 DAY) THEN 'Active'
        WHEN u.last_login > DATE_SUB(NOW(), INTERVAL 3 DAY) THEN 'Semi-Active'
        ELSE 'Inactive'
    END AS Activity_Status
FROM Users u
LEFT JOIN Roles r ON u.Role_ID = r.Role_ID
ORDER BY u.last_login DESC;