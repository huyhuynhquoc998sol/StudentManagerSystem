CREATE DATABASE StudentManagementSystem;
GO
USE StudentManagementSystem;
GO

-- Bảng phân quyền đăng nhập dùng chung[cite: 4]
CREATE TABLE USER_ACCOUNT (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- Bảo mật SHA-256[cite: 4]
    role VARCHAR(20) NOT NULL,
    is_active BIT DEFAULT 1
);

-- Phân hệ Admin[cite: 4]
CREATE TABLE ADMIN (
    user_id VARCHAR(36) PRIMARY KEY FOREIGN KEY REFERENCES USER_ACCOUNT(user_id),
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- Danh mục Lớp danh nghĩa[cite: 4]
CREATE TABLE CLASS (
    class_id VARCHAR(20) PRIMARY KEY,
    class_name VARCHAR(50),
    faculty VARCHAR(100),
    total_students INT DEFAULT 0
);

-- Phân hệ Giảng viên[cite: 4]
CREATE TABLE LECTURER (
    user_id VARCHAR(36) PRIMARY KEY FOREIGN KEY REFERENCES USER_ACCOUNT(user_id),
    lecturer_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    position VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- Phân hệ Sinh viên[cite: 4]
CREATE TABLE STUDENT (
    user_id VARCHAR(36) PRIMARY KEY FOREIGN KEY REFERENCES USER_ACCOUNT(user_id),
    student_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    gender VARCHAR(10),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    class_id VARCHAR(20) FOREIGN KEY REFERENCES CLASS(class_id)
);

-- Danh mục Lớp học phần[cite: 4]
CREATE TABLE COURSE_CLASS (
    course_class_id VARCHAR(60) PRIMARY KEY,
    class_id VARCHAR(20) FOREIGN KEY REFERENCES CLASS(class_id),
    lecturer_id VARCHAR(20) FOREIGN KEY REFERENCES LECTURER(lecturer_id),
    subject_name VARCHAR(150),
    semester VARCHAR(20)
);

-- Bảng Điểm thành phần[cite: 4]
CREATE TABLE GRADE (
    grade_id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(20) FOREIGN KEY REFERENCES STUDENT(student_id),
    course_class_id VARCHAR(60) FOREIGN KEY REFERENCES COURSE_CLASS(course_class_id),
    attendance_grade FLOAT,
    midterm_grade FLOAT,
    final_grade FLOAT,
    total_grade FLOAT
);

-- ==========================================
-- DỮ LIỆU MẪU MÔ PHỎNG HỆ THỐNG THỰC TẾ
-- ==========================================
INSERT INTO USER_ACCOUNT VALUES 
('A1', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Admin', 1),
('L1', 'gv_an', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Lecturer', 1),
('S1', 'sv_yen', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Student', 1),
('S2', 'sv_binh', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Student', 1),
('S3', 'sv_cuc', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Student', 1),
('S4', 'sv_huy', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Student', 1);

INSERT INTO ADMIN VALUES ('A1', 'System Admin', 'admin@ut.edu.vn', '0900111222');

INSERT INTO CLASS VALUES 
('MIS-01', 'Management Information Systems 01', 'Information Technology', 45),
('MIS-02', 'Management Information Systems 02', 'Information Technology', 50),
('LOG-01', 'Logistics 01', 'Transport and Logistics', 60);

INSERT INTO LECTURER VALUES ('L1', 'GV-MIS01', 'TS. Nguyen Van An', 'Senior Lecturer', 'an.nguyen@ut.edu.vn', '0901234567');

INSERT INTO STUDENT VALUES 
('S1', '456236789543', 'Lieu Nhu Yen', 'Female', 'yen.nhu@ut.edu.vn', '0912000001', 'District 1, HCM', 'MIS-01'),
('S2', '20000001', 'Le Van Binh', 'Male', 'binh.le@ut.edu.vn', '0912000002', 'District 3, HCM', 'MIS-01'),
('S3', '20000002', 'Tran Thi Cuc', 'Female', 'cuc.tran@ut.edu.vn', '0912000003', 'District 7, HCM', 'MIS-01'),
('S4', '20000003', 'Vo Quang Huy', 'Male', 'huy.vo@ut.edu.vn', '0912000004', 'Thu Duc, HCM', 'MIS-02');

INSERT INTO COURSE_CLASS VALUES 
('INT1002_01', 'MIS-01', 'GV-MIS01', 'Discrete Structures', 'HK1 2026-2027'),
('CS201_01', 'MIS-01', 'GV-MIS01', 'Object-Oriented Programming (C++)', 'HK1 2026-2027'),
('CS301_01', 'MIS-02', 'GV-MIS01', 'Data Structures and Algorithms', 'HK2 2026-2027');

INSERT INTO GRADE VALUES 
('G1', '456236789543', 'INT1002_01', 9.0, 8.5, 8.0, 8.3),
('G2', '20000001', 'INT1002_01', 10.0, 7.5, 8.0, 8.1),
('G3', '20000002', 'INT1002_01', 8.0, 9.0, 7.5, 8.0);