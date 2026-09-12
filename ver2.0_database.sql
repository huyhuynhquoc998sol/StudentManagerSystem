-- ==============================================================================
-- 1. TẠO CƠ SỞ DỮ LIỆU
-- ==============================================================================
CREATE DATABASE StudentManagementSystem;
GO

USE StudentManagementSystem;
GO

-- ==============================================================================
-- 2. TẠO 7 BẢNG THEO ĐÚNG DATA MODEL & CLASS DIAGRAM
-- ==============================================================================

-- 1. Bảng USER_ACCOUNT (Tài khoản người dùng)
CREATE TABLE USER_ACCOUNT (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BIT DEFAULT 1
);

-- 2. Bảng ADMIN (Quản trị viên)
CREATE TABLE ADMIN (
    user_id VARCHAR(36) PRIMARY KEY FOREIGN KEY REFERENCES USER_ACCOUNT(user_id) ON DELETE CASCADE,
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- 3. Bảng CLASS (Lớp sinh hoạt / danh nghĩa)
CREATE TABLE CLASS (
    class_id VARCHAR(20) PRIMARY KEY,
    class_name VARCHAR(50),
    faculty VARCHAR(100),
    total_students INT
);

-- 4. Bảng LECTURER (Giảng viên)
CREATE TABLE LECTURER (
    user_id VARCHAR(36) PRIMARY KEY FOREIGN KEY REFERENCES USER_ACCOUNT(user_id) ON DELETE CASCADE,
    lecturer_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    position VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- 5. Bảng STUDENT (Sinh viên)
CREATE TABLE STUDENT (
    user_id VARCHAR(36) PRIMARY KEY FOREIGN KEY REFERENCES USER_ACCOUNT(user_id) ON DELETE CASCADE,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    gender VARCHAR(10),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    class_id VARCHAR(20) FOREIGN KEY REFERENCES CLASS(class_id)
);

-- 6. Bảng COURSE_CLASS (Lớp học phần)
CREATE TABLE COURSE_CLASS (
    course_class_id VARCHAR(60) PRIMARY KEY,
    class_id VARCHAR(20) FOREIGN KEY REFERENCES CLASS(class_id),
    lecturer_id VARCHAR(20) FOREIGN KEY REFERENCES LECTURER(lecturer_id),
    subject_name VARCHAR(150),
    semester VARCHAR(20)
);

-- 7. Bảng GRADE (Điểm học phần)
CREATE TABLE GRADE (
    grade_id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(20) FOREIGN KEY REFERENCES STUDENT(student_id),
    course_class_id VARCHAR(60) FOREIGN KEY REFERENCES COURSE_CLASS(course_class_id),
    attendance_grade FLOAT,
    midterm_grade FLOAT,
    final_grade FLOAT,
    total_grade FLOAT
);
GO

-- ==============================================================================
-- 3. INSERT DỮ LIỆU MẪU (MẬT KHẨU MẶC ĐỊNH: 123456)
-- Chuỗi SHA-256: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
-- ==============================================================================

-- A. Dữ liệu Quản trị viên (2 Admin)
INSERT INTO USER_ACCOUNT (user_id, username, password_hash, role, is_active) VALUES 
('A1', 'admin1', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Admin', 1),
('A2', 'admin2', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Admin', 1);

INSERT INTO ADMIN (user_id, full_name, email, phone) VALUES 
('A1', 'Tran Quan Tri', 'quantri@ut.edu.vn', '090111222'),
('A2', 'Le He Thong', 'hethong@ut.edu.vn', '090333444');

-- B. Dữ liệu Giảng viên (5 Giảng viên)
INSERT INTO USER_ACCOUNT (user_id, username, password_hash, role, is_active) VALUES 
('L1', 'gv1', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Lecturer', 1),
('L2', 'gv2', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Lecturer', 1),
('L3', 'gv3', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Lecturer', 1),
('L4', 'gv4', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Lecturer', 1),
('L5', 'gv5', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Lecturer', 1);

INSERT INTO LECTURER (user_id, lecturer_id, full_name, position, email, phone) VALUES 
('L1', 'GV01', 'Nguyen Van An', 'PhD', 'gv1@ut.edu.vn', '0988001'),
('L2', 'GV02', 'Pham Thi Son', 'PhD', 'gv2@ut.edu.vn', '0988002'),
('L3', 'GV03', 'Le Minh Tri', 'PhD', 'gv3@ut.edu.vn', '0988003'),
('L4', 'GV04', 'Tran Duc Dat', 'PhD', 'gv4@ut.edu.vn', '0988004'),
('L5', 'GV05', 'Vu Hoang Yen', 'PhD', 'gv5@ut.edu.vn', '0988005');

-- C. Dữ liệu Lớp danh nghĩa & Lớp học phần
INSERT INTO CLASS (class_id, class_name, faculty, total_students) VALUES 
('CNTT-01', 'Information Tech 1', 'IT', 20),
('LOG-01', 'Logistics 1', 'Transport', 0);

INSERT INTO COURSE_CLASS (course_class_id, class_id, lecturer_id, subject_name, semester) VALUES 
('CS101', 'CNTT-01', 'GV01', 'Discrete Structures', 'HK1'),
('CS102', 'CNTT-01', 'GV02', 'OOP in C++', 'HK1');

-- D. Dữ liệu Tài khoản Sinh viên (20 Sinh viên)
INSERT INTO USER_ACCOUNT (user_id, username, password_hash, role, is_active) VALUES 
('S1', 'sv1', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S2', 'sv2', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S3', 'sv3', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S4', 'sv4', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S5', 'sv5', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S6', 'sv6', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S7', 'sv7', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S8', 'sv8', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S9', 'sv9', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S10', 'sv10', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S11', 'sv11', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S12', 'sv12', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S13', 'sv13', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S14', 'sv14', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S15', 'sv15', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S16', 'sv16', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S17', 'sv17', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S18', 'sv18', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S19', 'sv19', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1),
('S20', 'sv20', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Student', 1);

-- E. Dữ liệu Hồ sơ chi tiết Sinh viên (20 Sinh viên)
INSERT INTO STUDENT (user_id, student_id, full_name, gender, email, phone, address, class_id) VALUES 
('S1', 'SV26001', 'Nguyen Van Anh', 'Male', 'sv1@ut.edu.vn', '0912001', 'HCM', 'CNTT-01'),
('S2', 'SV26002', 'Tran Thi Binh', 'Female', 'sv2@ut.edu.vn', '0912002', 'HCM', 'CNTT-01'),
('S3', 'SV26003', 'Le Khanh Cuong', 'Male', 'sv3@ut.edu.vn', '0912003', 'HCM', 'CNTT-01'),
('S4', 'SV26004', 'Pham Thuy Dung', 'Female', 'sv4@ut.edu.vn', '0912004', 'HCM', 'CNTT-01'),
('S5', 'SV26005', 'Hoang Trong An', 'Male', 'sv5@ut.edu.vn', '0912005', 'HCM', 'CNTT-01'),
('S6', 'SV26006', 'Vu Thi Cuc', 'Female', 'sv6@ut.edu.vn', '0912006', 'HCM', 'CNTT-01'),
('S7', 'SV26007', 'Bui Van Dat', 'Male', 'sv7@ut.edu.vn', '0912007', 'HCM', 'CNTT-01'),
('S8', 'SV26008', 'Dang Thi Hoa', 'Female', 'sv8@ut.edu.vn', '0912008', 'HCM', 'CNTT-01'),
('S9', 'SV26009', 'Doan Khac Hung', 'Male', 'sv9@ut.edu.vn', '0912009', 'HCM', 'CNTT-01'),
('S10', 'SV26010', 'Ngo Thuy Linh', 'Female', 'sv10@ut.edu.vn', '0912010', 'HCM', 'CNTT-01'),
('S11', 'SV26011', 'Ly Hoang Nam', 'Male', 'sv11@ut.edu.vn', '0912011', 'HCM', 'CNTT-01'),
('S12', 'SV26012', 'Vuong Thi Nga', 'Female', 'sv12@ut.edu.vn', '0912012', 'HCM', 'CNTT-01'),
('S13', 'SV26013', 'Phan Thanh Phat', 'Male', 'sv13@ut.edu.vn', '0912013', 'HCM', 'CNTT-01'),
('S14', 'SV26014', 'Trinh Quoc Quan', 'Female', 'sv14@ut.edu.vn', '0912014', 'HCM', 'CNTT-01'),
('S15', 'SV26015', 'Dao Thi Quynh', 'Male', 'sv15@ut.edu.vn', '0912015', 'HCM', 'CNTT-01'),
('S16', 'SV26016', 'Duong Ngoc Sang', 'Female', 'sv16@ut.edu.vn', '0912016', 'HCM', 'CNTT-01'),
('S17', 'SV26017', 'Mai Thanh Thao', 'Male', 'sv17@ut.edu.vn', '0912017', 'HCM', 'CNTT-01'),
('S18', 'SV26018', 'Dinh Van Tuan', 'Female', 'sv18@ut.edu.vn', '0912018', 'HCM', 'CNTT-01'),
('S19', 'SV26019', 'Chau Nhu Uyen', 'Male', 'sv19@ut.edu.vn', '0912019', 'HCM', 'CNTT-01'),
('S20', 'SV26020', 'Lai Quoc Viet', 'Female', 'sv20@ut.edu.vn', '0912020', 'HCM', 'CNTT-01');

-- F. Dữ liệu Điểm học phần (Môn CS101 và CS102)
INSERT INTO GRADE (grade_id, student_id, course_class_id, attendance_grade, midterm_grade, final_grade, total_grade) VALUES 
('G1', 'SV26001', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G2', 'SV26002', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G3', 'SV26003', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G4', 'SV26004', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G5', 'SV26005', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G6', 'SV26006', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G7', 'SV26007', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G8', 'SV26008', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G9', 'SV26009', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G10', 'SV26010', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G11', 'SV26011', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G12', 'SV26012', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G13', 'SV26013', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G14', 'SV26014', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G15', 'SV26015', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G16', 'SV26016', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G17', 'SV26017', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G18', 'SV26018', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G19', 'SV26019', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G20', 'SV26020', 'CS101', 9.0, 8.0, 7.5, 7.9),
('G21', 'SV26001', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G22', 'SV26002', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G23', 'SV26003', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G24', 'SV26004', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G25', 'SV26005', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G26', 'SV26006', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G27', 'SV26007', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G28', 'SV26008', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G29', 'SV26009', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G30', 'SV26010', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G31', 'SV26011', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G32', 'SV26012', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G33', 'SV26013', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G34', 'SV26014', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G35', 'SV26015', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G36', 'SV26016', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G37', 'SV26017', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G38', 'SV26018', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G39', 'SV26019', 'CS102', 9.0, 8.0, 7.5, 7.9),
('G40', 'SV26020', 'CS102', 9.0, 8.0, 7.5, 7.9);
GO