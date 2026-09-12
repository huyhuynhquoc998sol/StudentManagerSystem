import tkinter as tk
from tkinter import ttk, messagebox
from services import SystemService

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1100x700")
        self.srv = SystemService()
        self.user = None
        self.show_login()

    def clear(self):
        for w in self.winfo_children(): w.destroy()

    def show_login(self):
        self.clear()
        f = tk.Frame(self, padx=40, pady=40)
        f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="System Authentication", font=("Arial", 20, "bold")).pack(pady=10)
        
        tk.Label(f, text="User name").pack(anchor="w", pady=(10,0))
        self.u = tk.Entry(f, font=("Arial", 12), width=35); self.u.pack()
        tk.Label(f, text="Password").pack(anchor="w", pady=(10,0))
        self.p = tk.Entry(f, font=("Arial", 12), width=35, show="*"); self.p.pack()
        
        tk.Button(f, text="Log in", bg="#2563eb", fg="white", font=("Arial", 12, "bold"), command=self.do_login).pack(fill="x", pady=20)

    def do_login(self):
        user = self.srv.auth(self.u.get(), self.p.get())
        if user:
            self.user = user
            if user.role == 'Admin': self.show_admin_students()
            elif user.role == 'Lecturer': self.show_lecturer_grades()
            elif user.role == 'Student': messagebox.showinfo("Info", "Student Module OK")
        else:
            messagebox.showerror("Error", "Sai tài khoản hoặc mật khẩu")

    def build_sidebar(self, role):
        sb = tk.Frame(self, bg="#0f172a", width=200)
        sb.pack(side="left", fill="y")
        tk.Label(sb, text=f"{role} Portal", fg="white", bg="#0f172a", font=("Arial", 14, "bold")).pack(pady=20)
        if role == 'Admin':
            tk.Button(sb, text="Student Management", bg="#1e293b", fg="white", bd=0, command=self.show_admin_students).pack(fill="x", ipady=10)
            tk.Button(sb, text="Class Management", bg="#0f172a", fg="white", bd=0, command=self.show_admin_classes).pack(fill="x", ipady=10)
            tk.Button(sb, text="Course Class", bg="#1e293b", fg="white", bd=0, command=self.show_admin_courses).pack(fill="x", ipady=10)
        elif role == 'Lecturer':
            tk.Button(sb, text="Grade Management", bg="#1e293b", fg="white", bd=0, command=self.show_lecturer_grades).pack(fill="x", ipady=10)
        tk.Button(sb, text="Log out", bg="#ef4444", fg="white", bd=0, command=self.show_login).pack(side="bottom", fill="x", pady=20, ipady=10)

    # ---------------------------------------------------------
    # MODULE: STUDENT MANAGEMENT (ADMIN) - Chuẩn form nhập liệu
    # ---------------------------------------------------------
    def show_admin_students(self):
        self.clear(); self.build_sidebar('Admin')
        main = tk.Frame(self, padx=20, pady=20); main.pack(side="right", fill="both", expand=True)
        
        # 1. Search Box
        sf = tk.Frame(main); sf.pack(fill="x", pady=5)
        tk.Label(sf, text="Tìm kiếm:").pack(side="left")
        self.ent_search = tk.Entry(sf, width=40); self.ent_search.pack(side="left", padx=5)
        tk.Button(sf, text="Tìm kiếm", command=self.load_students).pack(side="left", padx=5)
        tk.Button(sf, text="Tải lại tất cả", command=lambda: [self.ent_search.delete(0,tk.END), self.load_students()]).pack(side="left")

        # 2. Treeview
        tf = tk.Frame(main); tf.pack(fill="both", expand=True, pady=10)
        self.tree_stu = ttk.Treeview(tf, columns=("id","name","gen","cid","ph","em"), show="headings")
        for c, t in zip(self.tree_stu["columns"], ["Mã SV", "Họ Tên", "Giới Tính", "Mã Lớp", "SĐT", "Email"]):
            self.tree_stu.heading(c, text=t)
        self.tree_stu.pack(fill="both", expand=True)
        self.tree_stu.bind("<<TreeviewSelect>>", self.on_student_select)

        # 3. Details Form
        df = tk.LabelFrame(main, text="Thông tin chi tiết", padx=10, pady=10); df.pack(fill="x")
        tk.Label(df, text="Mã SV:").grid(row=0, column=0, sticky="w")
        self.sv_id = tk.Entry(df); self.sv_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(df, text="Họ Tên:").grid(row=0, column=2, sticky="w")
        self.sv_name = tk.Entry(df); self.sv_name.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(df, text="Giới Tính:").grid(row=1, column=0, sticky="w")
        self.sv_gen = tk.Entry(df); self.sv_gen.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(df, text="Mã Lớp:").grid(row=1, column=2, sticky="w")
        self.sv_cid = tk.Entry(df); self.sv_cid.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(df, text="SĐT:").grid(row=2, column=0, sticky="w")
        self.sv_ph = tk.Entry(df); self.sv_ph.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(df, text="Email:").grid(row=2, column=2, sticky="w")
        self.sv_em = tk.Entry(df); self.sv_em.grid(row=2, column=3, padx=5, pady=5)

        # 4. Action Buttons
        af = tk.Frame(main); af.pack(fill="x", pady=10)
        tk.Button(af, text="Thêm", bg="#16a34a", fg="white", command=self.add_stu).pack(side="left", padx=5)
        tk.Button(af, text="Cập nhật (Sửa)", bg="#ca8a04", fg="white", command=self.upd_stu).pack(side="left", padx=5)
        tk.Button(af, text="Xóa", bg="#dc2626", fg="white", command=self.del_stu).pack(side="left", padx=5)
        
        self.load_students()

    def load_students(self):
        for r in self.tree_stu.get_children(): self.tree_stu.delete(r)
        kw = self.ent_search.get()
        for s in self.srv.get_all_students(kw):
            self.tree_stu.insert("", tk.END, values=(s.student_id, s.full_name, s.gender, s.class_id, s.phone, s.email))

    def on_student_select(self, event):
        sel = self.tree_stu.focus()
        if sel:
            v = self.tree_stu.item(sel, 'values')
            for ent, val in zip([self.sv_id, self.sv_name, self.sv_gen, self.sv_cid, self.sv_ph, self.sv_em], v):
                ent.delete(0, tk.END); ent.insert(0, val)

    def add_stu(self):
        self.srv.add_student(self.sv_id.get(), self.sv_name.get(), self.sv_gen.get(), self.sv_cid.get(), self.sv_ph.get(), self.sv_em.get())
        self.load_students()

    def upd_stu(self):
        self.srv.update_student(self.sv_id.get(), self.sv_name.get(), self.sv_gen.get(), self.sv_cid.get(), self.sv_ph.get(), self.sv_em.get())
        self.load_students()

    def del_stu(self):
        self.srv.delete_student(self.sv_id.get())
        self.load_students()
        
if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()    