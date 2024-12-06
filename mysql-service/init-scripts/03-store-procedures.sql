DELIMITER //
CREATE PROCEDURE GetCourseStatistics(IN course_id INT)
BEGIN
    SELECT 
        c.Course_ID,
        c.Name AS Course_Name,
        COUNT(DISTINCT uc.User_ID) AS Enrolled_Students,
        COUNT(DISTINCT m.Module_ID) AS Total_Modules,
        COUNT(DISTINCT t.Topic_ID) AS Total_Topics,
        COUNT(DISTINCT mat.Material_ID) AS Total_Materials,
        AVG(g.Grade) AS Average_Grade
    FROM Courses c
    LEFT JOIN Users_Courses uc ON c.Course_ID = uc.Course_ID
    LEFT JOIN Modules m ON c.Course_ID = m.Course_ID
    LEFT JOIN Topics t ON m.Module_ID = t.Module_ID
    LEFT JOIN Materials mat ON t.Topic_ID = mat.Topic_ID
    LEFT JOIN Grades g ON m.Module_ID = g.Module_ID
    WHERE c.Course_ID = course_id
    GROUP BY c.Course_ID, c.Name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE FindInactiveStudents(IN days_inactive INT)
BEGIN
    SELECT 
        s.Student_ID,
        u.Name,
        u.Email,
        COALESCE(
            MAX(a.Session_ID),
            MAX(f.Feedback_Date),
            MAX(p.Last_Updated),
            MAX(g.Assessment_Date)
        ) AS Last_Activity_Date
    FROM Students s
    JOIN Users u ON s.Student_ID = u.User_ID
    LEFT JOIN Attendance a ON s.Student_ID = a.Student_ID
    LEFT JOIN Feedback f ON s.Student_ID = f.Student_ID
    LEFT JOIN Progress p ON s.Student_ID = p.Student_ID
    LEFT JOIN Grades g ON s.Student_ID = g.Student_ID
    GROUP BY s.Student_ID, u.Name, u.Email
    HAVING Last_Activity_Date < DATE_SUB(CURDATE(), INTERVAL days_inactive DAY)
        OR Last_Activity_Date IS NULL
    ORDER BY Last_Activity_Date;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER LogUserLogin
AFTER UPDATE ON Users
FOR EACH ROW
BEGIN
    IF NEW.last_login != OLD.last_login THEN
        INSERT INTO UserLoginLog (User_ID, Login_Time)
        VALUES (NEW.User_ID, NEW.last_login);
    END IF;
END //
DELIMITER ;

CREATE TABLE IF NOT EXISTS CourseEnrollmentLog (
    Log_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT,
    Course_ID INT,
    Enrollment_Date DATE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID)
);

DELIMITER //
CREATE TRIGGER LogCourseEnrollment
AFTER INSERT ON Users_Courses
FOR EACH ROW
BEGIN
    INSERT INTO CourseEnrollmentLog (User_ID, Course_ID, Enrollment_Date)
    VALUES (NEW.User_ID, NEW.Course_ID, NEW.Enrollment_Date);
END //
DELIMITER ;