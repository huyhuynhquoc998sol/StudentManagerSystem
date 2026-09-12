class UserAccount:
    def __init__(self, uid, user, role):
        self.user_id = uid; self.username = user; self.role = role

class Admin:
    def __init__(self, uid, name, email, phone):
        self.user_id = uid; self.full_name = name; self.email = email; self.phone = phone

class Lecturer:
    def __init__(self, uid, lid, name, pos, email, phone):
        self.user_id = uid; self.lecturer_id = lid; self.full_name = name; self.position = pos; self.email = email; self.phone = phone

class Student:
    def __init__(self, sid, name, gender, cid, phone, email):
        self.student_id = sid; self.full_name = name; self.gender = gender; self.class_id = cid; self.phone = phone; self.email = email

class ClassEntity:
    def __init__(self, cid, cname, faculty, total):
        self.class_id = cid; self.class_name = cname; self.faculty = faculty; self.total_students = total

class CourseClass:
    def __init__(self, ccid, cid, lid, subj, sem):
        self.course_class_id = ccid; self.class_id = cid; self.lecturer_id = lid; self.subject_name = subj; self.semester = sem

class Grade:
    def __init__(self, gid, sid, ccid, att, mid, final, total):
        self.grade_id = gid; self.student_id = sid; self.course_class_id = ccid
        self.attendance = att; self.midterm = mid; self.final = final; self.total = total