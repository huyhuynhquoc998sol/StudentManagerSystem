import hashlib
import uuid
import pyodbc
from database import DatabaseConnection
from models import UserAccount, Student, ClassEntity, CourseClass, Lecturer

class SystemService:
    def __init__(self):
        self.db = DatabaseConnection()

    def auth(self, username, password):
        conn = self.db.connect()
        if not conn: return None
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, role FROM USER_ACCOUNT WHERE username=? AND password_hash=?", (username, pwd_hash))
        row = cur.fetchone()
        conn.close()
        if row: return UserAccount(row[0], row[1], row[2])
        return None

    def sync_class_totals(self, cursor):
        cursor.execute("UPDATE CLASS SET total_students = (SELECT COUNT(*) FROM STUDENT WHERE STUDENT.class_id = CLASS.class_id)")

    # --- ADMIN: STUDENT SERVICES ---
    def get_all_students(self, keyword=""):
        conn = self.db.connect()
        data = []
        if conn:
            cur = conn.cursor()
            query = "SELECT student_id, full_name, gender, class_id, phone, email, address FROM STUDENT"
            if keyword: query += f" WHERE full_name LIKE '%{keyword}%' OR student_id LIKE '%{keyword}%'"
            cur.execute(query)
            for r in cur.fetchall(): data.append(Student(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
            conn.close()
        return data

    def add_student(self, sid, name, gender, cid, phone, email):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                uid = str(uuid.uuid4())
                cur.execute("INSERT INTO USER_ACCOUNT VALUES (?, ?, ?, 'Student', 1)", (uid, sid, hashlib.sha256('123456'.encode()).hexdigest()))
                cur.execute("INSERT INTO STUDENT (user_id, student_id, full_name, gender, class_id, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)", (uid, sid, name, gender, cid, phone, email))
                self.sync_class_totals(cur)
                conn.commit()
                return "OK"
            except pyodbc.IntegrityError: return "Mã lớp bạn nhập không tồn tại ! Vui lòng kiểm tra lại"
            except Exception as e: return str(e)
            finally: conn.close()

    def update_student(self, sid, name, gender, cid, phone, email):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE STUDENT SET full_name=?, gender=?, class_id=?, phone=?, email=? WHERE student_id=?", (name, gender, cid, phone, email, sid))
                self.sync_class_totals(cur)
                conn.commit()
                return "OK"
            except pyodbc.IntegrityError: return "Mã lớp bạn nhập không tồn tại ! Vui lòng kiểm tra lại"
            except Exception as e: return str(e)
            finally: conn.close()

    def delete_student(self, sid):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT user_id FROM STUDENT WHERE student_id=?", (sid,))
                row = cur.fetchone()
                if row:
                    cur.execute("DELETE FROM USER_ACCOUNT WHERE user_id=?", (row[0],))
                    self.sync_class_totals(cur)
                    conn.commit()
                return "OK"
            except Exception as e: return "Không thể xóa do ràng buộc dữ liệu!"
            finally: conn.close()

    # --- ADMIN: CLASS SERVICES ---
    def get_all_classes(self, keyword=""):
        conn = self.db.connect()
        data = []
        if conn:
            cur = conn.cursor()
            query = "SELECT class_id, class_name, faculty, total_students FROM CLASS"
            if keyword: query += f" WHERE class_name LIKE '%{keyword}%' OR class_id LIKE '%{keyword}%'"
            cur.execute(query)
            for r in cur.fetchall(): data.append(ClassEntity(r[0], r[1], r[2], r[3]))
            conn.close()
        return data

    def add_class(self, cid, name, faculty):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO CLASS VALUES (?, ?, ?, 0)", (cid, name, faculty))
                conn.commit()
                return "OK"
            except Exception as e: return str(e)
            finally: conn.close()

    def update_class(self, cid, name, faculty):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE CLASS SET class_name=?, faculty=? WHERE class_id=?", (name, faculty, cid))
                conn.commit()
                return "OK"
            except Exception as e: return str(e)
            finally: conn.close()

    def delete_class(self, cid):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM CLASS WHERE class_id=?", (cid,))
                conn.commit()
                return "OK"
            except pyodbc.IntegrityError: return "Không thể xóa lớp này vì đang có sinh viên hoặc dữ liệu liên kết!"
            finally: conn.close()

    # --- ADMIN: COURSE CLASS SERVICES ---
    def get_all_course_classes(self, keyword=""):
        conn = self.db.connect()
        data = []
        if conn:
            cur = conn.cursor()
            query = "SELECT course_class_id, class_id, lecturer_id, subject_name, semester FROM COURSE_CLASS"
            if keyword: query += f" WHERE subject_name LIKE '%{keyword}%' OR course_class_id LIKE '%{keyword}%'"
            cur.execute(query)
            for r in cur.fetchall(): data.append(CourseClass(r[0], r[1], r[2], r[3], r[4]))
            conn.close()
        return data

    def add_course_class(self, ccid, cid, lid, subj, sem):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO COURSE_CLASS VALUES (?, ?, ?, ?, ?)", (ccid, cid, lid, subj, sem))
                conn.commit()
                return "OK"
            except pyodbc.IntegrityError: return "Mã lớp bạn nhập không tồn tại ! Vui lòng kiểm tra lại"
            except Exception as e: return str(e)
            finally: conn.close()

    def update_course_class(self, ccid, cid, lid, subj, sem):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE COURSE_CLASS SET class_id=?, lecturer_id=?, subject_name=?, semester=? WHERE course_class_id=?", (cid, lid, subj, sem, ccid))
                conn.commit()
                return "OK"
            except pyodbc.IntegrityError: return "Mã lớp hoặc mã giảng viên không tồn tại!"
            except Exception as e: return str(e)
            finally: conn.close()

    def delete_course_class(self, ccid):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM COURSE_CLASS WHERE course_class_id=?", (ccid,))
                conn.commit()
                return "OK"
            except pyodbc.IntegrityError: return "Không thể xóa vì đã có điểm của sinh viên liên kết với lớp học phần này!"
            finally: conn.close()

    

    # --- GRADE SERVICES ---
    def get_grades_by_course(self, course_id, keyword=""):
        conn = self.db.connect()
        data = []
        if conn:
            cur = conn.cursor()
            query = """
                SELECT s.student_id, s.full_name, g.attendance_grade, g.midterm_grade, g.final_grade, g.total_grade, g.course_class_id
                FROM GRADE g JOIN STUDENT s ON g.student_id = s.student_id WHERE g.course_class_id=?
            """
            if keyword: query += f" AND (s.student_id LIKE '%{keyword}%' OR s.full_name LIKE '%{keyword}%')"
            cur.execute(query, (course_id,))
            data = [{"sid": r[0], "name": r[1], "att": r[2], "mid": r[3], "fin": r[4], "tot": r[5], "ccid": r[6]} for r in cur.fetchall()]
            conn.close()
        return data

    def update_grade(self, sid, ccid, att, mid, fin):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                att, mid, fin = float(att), float(mid), float(fin)
                tot = round((att * 0.1) + (mid * 0.3) + (fin * 0.6), 2)
                cur.execute("UPDATE GRADE SET attendance_grade=?, midterm_grade=?, final_grade=?, total_grade=? WHERE student_id=? AND course_class_id=?", (att, mid, fin, tot, sid, ccid))
                conn.commit()
                return "OK"
            except Exception as e: return str(e)
            finally: conn.close()

    # --- STUDENT SUBSYSTEM SERVICES ---
    def get_student_transcript(self, user_id):
        conn = self.db.connect()
        data = []
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.subject_name, c.semester, g.attendance_grade, g.midterm_grade, g.final_grade, g.total_grade
                FROM GRADE g JOIN COURSE_CLASS c ON g.course_class_id = c.course_class_id
                JOIN STUDENT s ON g.student_id = s.student_id WHERE s.user_id = ?
            """, (user_id,))
            data = [{"sub": r[0], "sem": r[1], "att": r[2], "mid": r[3], "fin": r[4], "tot": r[5]} for r in cur.fetchall()]
            conn.close()
        return data

    def get_student_profile(self, user_id):
        conn = self.db.connect()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT student_id, full_name, gender, class_id, phone, email, address FROM STUDENT WHERE user_id=?", (user_id,))
            r = cur.fetchone()
            conn.close()
            if r: return Student(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        return None

    def update_student_profile(self, user_id, name, phone, email, address):
        conn = self.db.connect()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE STUDENT SET full_name=?, phone=?, email=?, address=? WHERE user_id=?", (name, phone, email, address, user_id))
                conn.commit()
                return "OK"
            except Exception as e: return str(e)
            finally: conn.close()