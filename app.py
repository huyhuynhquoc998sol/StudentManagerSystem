import tkinter as tk
from tkinter import ttk, messagebox
from services import SystemService

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x750")
        self.srv = SystemService()
        self.user = None
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        f = tk.Frame(self, padx=40, pady=40)
        f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="System Authentication", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(f, text="Username").pack(anchor="w", pady=(10, 0))
        self.u = tk.Entry(f, font=("Arial", 12), width=35)
        self.u.pack()
        tk.Label(f, text="Password").pack(anchor="w", pady=(10, 0))
        self.p = tk.Entry(f, font=("Arial", 12), width=35, show="*")
        self.p.pack()
        tk.Button(f, text="Log in", bg="#2563eb", fg="white", font=("Arial", 12, "bold"), command=self.do_login).pack(fill="x", pady=20)

    def do_login(self):
        user = self.srv.auth(self.u.get(), self.p.get())
        if user:
            self.user = user
            if user.role == 'Admin':
                self.show_admin_students()
            elif user.role == 'Lecturer':
                self.show_lecturer_assigned_classes()
            elif user.role == 'Student':
                self.show_student_transcript()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def build_sidebar(self, role):
        sb = tk.Frame(self, bg="#0f172a", width=220)
        sb.pack(side="left", fill="y")
        tk.Label(sb, text=f"{role} Portal", fg="white", bg="#0f172a", font=("Arial", 14, "bold")).pack(pady=20)
        if role == 'Admin':
            tk.Button(sb, text="Student Management", bg="#1e293b", fg="white", bd=0, command=self.show_admin_students).pack(fill="x", ipady=10)
            tk.Button(sb, text="Class Management", bg="#0f172a", fg="white", bd=0, command=self.show_admin_classes).pack(fill="x", ipady=10)
            tk.Button(sb, text="Course Class", bg="#1e293b", fg="white", bd=0, command=self.show_admin_courses).pack(fill="x", ipady=10)
            tk.Button(sb, text="Grade Management", bg="#0f172a", fg="white", bd=0, command=self.show_admin_grades).pack(fill="x", ipady=10)
        elif role == 'Lecturer':
            tk.Button(sb, text="My Assigned Classes", bg="#1e293b", fg="white", bd=0, command=self.show_lecturer_assigned_classes).pack(fill="x", ipady=10)
            tk.Button(sb, text="Grade Management", bg="#0f172a", fg="white", bd=0, command=self.show_lecturer_grades).pack(fill="x", ipady=10)
            tk.Button(sb, text="Profile Management", bg="#1e293b", fg="white", bd=0, command=self.show_lecturer_profile).pack(fill="x", ipady=10)
        elif role == 'Student':
            tk.Button(sb, text="Academic Transcript", bg="#1e293b", fg="white", bd=0, command=self.show_student_transcript).pack(fill="x", ipady=10)
            tk.Button(sb, text="Profile Management", bg="#0f172a", fg="white", bd=0, command=self.show_student_profile).pack(fill="x", ipady=10)
        tk.Button(sb, text="Log out", bg="#ef4444", fg="white", bd=0, command=self.show_login).pack(side="bottom", fill="x", pady=20, ipady=10)

    # ============================== ADMIN MODULES ==============================
    def show_admin_classes(self):
        self.clear()
        self.build_sidebar('Admin')
        main = tk.Frame(self, padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)

        sf = tk.Frame(main)
        sf.pack(fill="x", pady=5)
        tk.Label(sf, text="Search Class:").pack(side="left")
        self.ent_search_cls = tk.Entry(sf, width=40)
        self.ent_search_cls.pack(side="left", padx=5)
        tk.Button(sf, text="Search", command=self.load_classes).pack(side="left", padx=5)

        self.tree_cls = ttk.Treeview(main, columns=("id", "name", "fac", "tot"), show="headings")
        for c, t in zip(self.tree_cls["columns"], ["Class ID", "Class Name", "Faculty", "Total Students"]):
            self.tree_cls.heading(c, text=t)
        self.tree_cls.pack(fill="both", expand=True, pady=10)
        self.tree_cls.bind("<<TreeviewSelect>>", lambda e: self.on_select(self.tree_cls, [self.cls_id, self.cls_name, self.cls_fac]))

        df = tk.LabelFrame(main, text="Detailed Information", padx=10, pady=10)
        df.pack(fill="x")
        tk.Label(df, text="Class ID:").grid(row=0, column=0, sticky="w")
        self.cls_id = tk.Entry(df)
        self.cls_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(df, text="Class Name:").grid(row=0, column=2, sticky="w")
        self.cls_name = tk.Entry(df)
        self.cls_name.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(df, text="Faculty:").grid(row=1, column=0, sticky="w")
        self.cls_fac = tk.Entry(df)
        self.cls_fac.grid(row=1, column=1, padx=5, pady=5)

        af = tk.Frame(main)
        af.pack(fill="x", pady=10)
        tk.Button(af, text="Add", bg="#16a34a", fg="white", command=self.add_cls).pack(side="left", padx=5)
        tk.Button(af, text="Update", bg="#ca8a04", fg="white", command=self.upd_cls).pack(side="left", padx=5)
        tk.Button(af, text="Delete", bg="#dc2626", fg="white", command=self.del_cls).pack(side="left", padx=5)
        self.load_classes()

    def add_cls(self):
        res = self.srv.add_class(self.cls_id.get(), self.cls_name.get(), self.cls_fac.get())
        if res == "OK":
            self.load_classes()
            messagebox.showinfo("Success", "Class added successfully!")
        else:
            messagebox.showerror("Error", res)

    def upd_cls(self):
        res = self.srv.update_class(self.cls_id.get(), self.cls_name.get(), self.cls_fac.get())
        if res == "OK":
            self.load_classes()
            messagebox.showinfo("Success", "Class updated successfully!")
        else:
            messagebox.showerror("Error", res)

    def del_cls(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this class?"):
            res = self.srv.delete_class(self.cls_id.get())
            if res == "OK":
                self.load_classes()
            else:
                messagebox.showerror("Error", res)

    def load_classes(self):
        for r in self.tree_cls.get_children():
            self.tree_cls.delete(r)
        for c in self.srv.get_all_classes(self.ent_search_cls.get()):
            self.tree_cls.insert("", tk.END, values=(c.class_id, c.class_name, c.faculty, c.total_students))

    def show_admin_courses(self):
        self.clear()
        self.build_sidebar('Admin')
        main = tk.Frame(self, padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)

        sf = tk.Frame(main)
        sf.pack(fill="x", pady=5)
        tk.Label(sf, text="Search Course:").pack(side="left")
        self.ent_search_cc = tk.Entry(sf, width=40)
        self.ent_search_cc.pack(side="left", padx=5)
        tk.Button(sf, text="Search", command=self.load_courses).pack(side="left", padx=5)

        self.tree_cc = ttk.Treeview(main, columns=("ccid", "cid", "lid", "subj", "sem"), show="headings")
        for c, t in zip(self.tree_cc["columns"], ["Course Class ID", "Class ID", "Lecturer ID", "Subject Name", "Semester"]):
            self.tree_cc.heading(c, text=t)
        self.tree_cc.pack(fill="both", expand=True, pady=10)
        self.tree_cc.bind("<<TreeviewSelect>>", lambda e: self.on_select(self.tree_cc, [self.cc_id, self.cc_cid, self.cc_lid, self.cc_subj, self.cc_sem]))

        df = tk.LabelFrame(main, text="Detailed Information", padx=10, pady=10)
        df.pack(fill="x")
        tk.Label(df, text="Course Class ID:").grid(row=0, column=0, sticky="w")
        self.cc_id = tk.Entry(df)
        self.cc_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(df, text="Class ID:").grid(row=0, column=2, sticky="w")
        self.cc_cid = tk.Entry(df)
        self.cc_cid.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(df, text="Lecturer ID:").grid(row=1, column=0, sticky="w")
        self.cc_lid = tk.Entry(df)
        self.cc_lid.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(df, text="Subject Name:").grid(row=1, column=2, sticky="w")
        self.cc_subj = tk.Entry(df)
        self.cc_subj.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(df, text="Semester:").grid(row=2, column=0, sticky="w")
        self.cc_sem = tk.Entry(df)
        self.cc_sem.grid(row=2, column=1, padx=5, pady=5)

        af = tk.Frame(main)
        af.pack(fill="x", pady=10)
        tk.Button(af, text="Add", bg="#16a34a", fg="white", command=self.add_cc).pack(side="left", padx=5)
        tk.Button(af, text="Update", bg="#ca8a04", fg="white", command=self.upd_cc).pack(side="left", padx=5)
        tk.Button(af, text="Delete", bg="#dc2626", fg="white", command=self.del_cc).pack(side="left", padx=5)
        self.load_courses()

    def add_cc(self):
        res = self.srv.add_course_class(self.cc_id.get(), self.cc_cid.get(), self.cc_lid.get(), self.cc_subj.get(), self.cc_sem.get())
        if res == "OK":
            self.load_courses()
            messagebox.showinfo("Success", "Course class added successfully!")
        else:
            messagebox.showerror("Error", res)

    def upd_cc(self):
        res = self.srv.update_course_class(self.cc_id.get(), self.cc_cid.get(), self.cc_lid.get(), self.cc_subj.get(), self.cc_sem.get())
        if res == "OK":
            self.load_courses()
            messagebox.showinfo("Success", "Course class updated successfully!")
        else:
            messagebox.showerror("Error", res)

    def del_cc(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this course class?"):
            res = self.srv.delete_course_class(self.cc_id.get())
            if res == "OK":
                self.load_courses()
            else:
                messagebox.showerror("Error", res)

    def load_courses(self):
        for r in self.tree_cc.get_children():
            self.tree_cc.delete(r)
        for c in self.srv.get_all_course_classes(self.ent_search_cc.get()):
            self.tree_cc.insert("", tk.END, values=(c.course_class_id, c.class_id, c.lecturer_id, c.subject_name, c.semester))

    def show_admin_students(self):
        self.clear()
        self.build_sidebar('Admin')
        main = tk.Frame(self, padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)

        sf = tk.Frame(main)
        sf.pack(fill="x", pady=5)
        tk.Label(sf, text="Search:").pack(side="left")
        self.ent_search = tk.Entry(sf, width=40)
        self.ent_search.pack(side="left", padx=5)
        tk.Button(sf, text="Search", command=self.load_students).pack(side="left", padx=5)

        self.tree_stu = ttk.Treeview(main, columns=("id", "name", "gen", "cid", "ph", "em"), show="headings")
        for c, t in zip(self.tree_stu["columns"], ["Student ID", "Full Name", "Gender", "Class ID", "Phone", "Email"]):
            self.tree_stu.heading(c, text=t)
        self.tree_stu.pack(fill="both", expand=True, pady=10)
        self.tree_stu.bind("<<TreeviewSelect>>", lambda e: self.on_select(self.tree_stu, [self.sv_id, self.sv_name, self.sv_gen, self.sv_cid, self.sv_ph, self.sv_em]))

        df = tk.LabelFrame(main, text="Detailed Information", padx=10, pady=10)
        df.pack(fill="x")
        tk.Label(df, text="Student ID:").grid(row=0, column=0, sticky="w")
        self.sv_id = tk.Entry(df)
        self.sv_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(df, text="Full Name:").grid(row=0, column=2, sticky="w")
        self.sv_name = tk.Entry(df)
        self.sv_name.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(df, text="Gender:").grid(row=1, column=0, sticky="w")
        self.sv_gen = tk.Entry(df)
        self.sv_gen.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(df, text="Class ID:").grid(row=1, column=2, sticky="w")
        self.sv_cid = tk.Entry(df)
        self.sv_cid.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(df, text="Phone:").grid(row=2, column=0, sticky="w")
        self.sv_ph = tk.Entry(df)
        self.sv_ph.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(df, text="Email:").grid(row=2, column=2, sticky="w")
        self.sv_em = tk.Entry(df)
        self.sv_em.grid(row=2, column=3, padx=5, pady=5)

        af = tk.Frame(main)
        af.pack(fill="x", pady=10)
        tk.Button(af, text="Add", bg="#16a34a", fg="white", command=self.add_stu).pack(side="left", padx=5)
        tk.Button(af, text="Update", bg="#ca8a04", fg="white", command=self.upd_stu).pack(side="left", padx=5)
        tk.Button(af, text="Delete", bg="#dc2626", fg="white", command=self.del_stu).pack(side="left", padx=5)
        self.load_students()

    def add_stu(self):
        res = self.srv.add_student(self.sv_id.get(), self.sv_name.get(), self.sv_gen.get(), self.sv_cid.get(), self.sv_ph.get(), self.sv_em.get())
        if res == "OK":
            self.load_students()
            messagebox.showinfo("Success", "Student added successfully!")
        else:
            messagebox.showerror("Error", res)

    def upd_stu(self):
        res = self.srv.update_student(self.sv_id.get(), self.sv_name.get(), self.sv_gen.get(), self.sv_cid.get(), self.sv_ph.get(), self.sv_em.get())
        if res == "OK":
            self.load_students()
            messagebox.showinfo("Success", "Student updated successfully!")
        else:
            messagebox.showerror("Error", res)

    def del_stu(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this student?"):
            res = self.srv.delete_student(self.sv_id.get())
            if res == "OK":
                self.load_students()
            else:
                messagebox.showerror("Error", res)

    def load_students(self):
        for r in self.tree_stu.get_children():
            self.tree_stu.delete(r)
        for s in self.srv.get_all_students(self.ent_search.get()):
            self.tree_stu.insert("", tk.END, values=(s.student_id, s.full_name, s.gender, s.class_id, s.phone, s.email))

    def show_admin_grades(self):
        self.clear()
        self.build_sidebar('Admin')
        main = tk.Frame(self, padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)

        sf = tk.Frame(main)
        sf.pack(fill="x", pady=5)
        tk.Label(sf, text="Search by Course Class ID:").pack(side="left")
        self.ent_search_ad_gr = tk.Entry(sf, width=40)
        self.ent_search_ad_gr.pack(side="left", padx=5)
        tk.Button(sf, text="Load Class List", command=self.load_admin_grades).pack(side="left", padx=5)

        self.tree_ad_gr = ttk.Treeview(main, columns=("sid", "name", "att", "mid", "fin", "tot", "ccid"), show="headings")
        for c, t in zip(self.tree_ad_gr["columns"], ["Student ID", "Full Name", "Attendance", "Midterm", "Final", "Total", "Course Class ID"]):
            self.tree_ad_gr.heading(c, text=t)
        self.tree_ad_gr.pack(fill="both", expand=True, pady=10)
        self.tree_ad_gr.bind("<<TreeviewSelect>>", lambda e: self.on_select(self.tree_ad_gr, [self.ad_gr_sid, self.ad_gr_name, self.ad_gr_att, self.ad_gr_mid, self.ad_gr_fin]))

        df = tk.LabelFrame(main, text="Enter / Update Student Grades", padx=10, pady=10)
        df.pack(fill="x")
        tk.Label(df, text="Student ID:").grid(row=0, column=0, sticky="w")
        self.ad_gr_sid = tk.Entry(df, state="readonly")
        self.ad_gr_sid.grid(row=0, column=1, padx=5, pady=5)
        self.ad_gr_name = tk.Entry(df)
        tk.Label(df, text="Attendance:").grid(row=1, column=0, sticky="w")
        self.ad_gr_att = tk.Entry(df)
        self.ad_gr_att.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(df, text="Midterm:").grid(row=1, column=2, sticky="w")
        self.ad_gr_mid = tk.Entry(df)
        self.ad_gr_mid.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(df, text="Final:").grid(row=1, column=4, sticky="w")
        self.ad_gr_fin = tk.Entry(df)
        self.ad_gr_fin.grid(row=1, column=5, padx=5, pady=5)
        tk.Button(df, text="Save Grade", bg="#16a34a", fg="white", command=self.upd_admin_grade).grid(row=2, column=5, pady=10)

    def load_admin_grades(self):
        for r in self.tree_ad_gr.get_children():
            self.tree_ad_gr.delete(r)
        ccid = self.ent_search_ad_gr.get()
        if not ccid:
            return
        for g in self.srv.get_grades_by_course(ccid):
            self.tree_ad_gr.insert("", tk.END, values=(g['sid'], g['name'], g['att'], g['mid'], g['fin'], g['tot'], g['ccid']))

    def upd_admin_grade(self):
        ccid = self.ent_search_ad_gr.get()
        if ccid and self.ad_gr_sid.get():
            res = self.srv.update_grade(self.ad_gr_sid.get(), ccid, self.ad_gr_att.get(), self.ad_gr_mid.get(), self.ad_gr_fin.get())
            if res == "OK":
                self.load_admin_grades()
                messagebox.showinfo("Success", "Grades saved successfully!")
            else:
                messagebox.showerror("Error", res)

    def on_select(self, tree, entry_list):
        sel = tree.focus()
        if sel:
            for ent, val in zip(entry_list, tree.item(sel, 'values')):
                ent.config(state="normal")
                ent.delete(0, tk.END)
                ent.insert(0, val)

    

    # ============================== STUDENT MODULES ==============================
    def show_student_transcript(self):
        self.clear()
        self.build_sidebar('Student')
        main = tk.Frame(self, padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)
        tk.Label(main, text="Academic Transcript (Read-Only)", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        tree = ttk.Treeview(main, columns=("sub", "sem", "att", "mid", "fin", "tot"), show="headings")
        for c, t in zip(tree["columns"], ["Subject", "Semester", "Attendance", "Midterm", "Final", "Total Grade"]):
            tree.heading(c, text=t)
        tree.pack(fill="both", expand=True, pady=10)
        for t in self.srv.get_student_transcript(self.user.user_id):
            tree.insert("", tk.END, values=(t['sub'], t['sem'], t['att'], t['mid'], t['fin'], t['tot']))

    def show_student_profile(self):
        self.clear()
        self.build_sidebar('Student')
        prof = self.srv.get_student_profile(self.user.user_id)
        main = tk.Frame(self, padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)
        tk.Label(main, text="Personal Profile Management", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        df = tk.LabelFrame(main, text="Your Information", padx=20, pady=20)
        df.pack(fill="x")
        tk.Label(df, text="Full Name:").grid(row=0, column=0, sticky="w")
        self.sp_name = tk.Entry(df, width=35)
        self.sp_name.insert(0, prof.full_name)
        self.sp_name.grid(row=0, column=1, pady=10)
        tk.Label(df, text="Phone Number:").grid(row=1, column=0, sticky="w")
        self.sp_phone = tk.Entry(df, width=35)
        self.sp_phone.insert(0, prof.phone)
        self.sp_phone.grid(row=1, column=1, pady=10)
        tk.Label(df, text="Email:").grid(row=2, column=0, sticky="w")
        self.sp_email = tk.Entry(df, width=35)
        self.sp_email.insert(0, prof.email)
        self.sp_email.grid(row=2, column=1, pady=10)
        tk.Label(df, text="Contact Address:").grid(row=3, column=0, sticky="w")
        self.sp_address = tk.Entry(df, width=35)
        self.sp_address.insert(0, prof.address if prof.address else "")
        self.sp_address.grid(row=3, column=1, pady=10)
        tk.Button(df, text="Update", bg="#16a34a", fg="white", command=self.upd_student_profile).grid(row=4, column=1, sticky="e", pady=20)

    def upd_student_profile(self):
        res = self.srv.update_student_profile(self.user.user_id, self.sp_name.get(), self.sp_phone.get(), self.sp_email.get(), self.sp_address.get())
        if res == "OK":
            messagebox.showinfo("Success", "Profile updated successfully!")
        else:
            messagebox.showerror("Error", res)

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()