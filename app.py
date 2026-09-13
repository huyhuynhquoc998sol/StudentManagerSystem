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

    

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()