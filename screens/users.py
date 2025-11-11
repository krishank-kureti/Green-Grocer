# screens/users.py
import customtkinter as ctk
from tkinter import ttk, simpledialog, messagebox
from db import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class UsersScreen(ctk.CTkFrame):
    def __init__(self, master, role="viewer"):
        super().__init__(master)

        # only admin can view this screen
        if role != "admin":
            ctk.CTkLabel(self, text="Access Denied", font=("Arial", 18), text_color="red").pack(pady=50)
            return

        ctk.CTkLabel(self, text="User Management", font=("Arial", 18)).pack(pady=12)

        cols = ("User_ID", "Username", "Role")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for CRUD
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=8)

        ctk.CTkButton(btn_frame, text="Add User", command=self.add_user).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Edit Selected", command=self.edit_user).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_user).pack(side="left", padx=6)

        self.load_users()

    def load_users(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT User_ID, Username, Role FROM Users")
            rows = cur.fetchall()

            self.tree.delete(*self.tree.get_children())

            for r in rows:
                self.tree.insert("", "end", values=r)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            try: conn.close()
            except: pass

    def add_user(self):
        AddUserWindow(self, self.load_users)

    def edit_user(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a user to edit")
            return

        item = self.tree.item(sel[0])["values"]  # (User_ID, Username, Role)
        EditUserWindow(self, item, self.load_users)

    def delete_user(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a user to delete")
            return

        item = self.tree.item(sel[0])["values"]
        user_id = item[0]

        if messagebox.askyesno("Confirm Delete", f"Delete user ID {user_id}?"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM Users WHERE User_ID=%s", (user_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User deleted")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", str(e))

class AddUserWindow(ctk.CTkToplevel):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)
        self.title("Add User")
        self.geometry("350x300")
        self.refresh = refresh_callback

        ctk.CTkLabel(self, text="Create New User", font=("Arial", 16)).pack(pady=12)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.role_box = ctk.CTkComboBox(self, values=["admin", "viewer"])

        self.username.pack(pady=6, padx=20, fill="x")
        self.password.pack(pady=6, padx=20, fill="x")
        self.role_box.pack(pady=6, padx=20, fill="x")

        ctk.CTkButton(self, text="Create User", command=self.create_user).pack(pady=12)

    def create_user(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        role = self.role_box.get()

        if not uname or not pwd:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                (uname, hash_password(pwd), role)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "User created")
            self.refresh()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

class EditUserWindow(ctk.CTkToplevel):
    def __init__(self, parent, user_data, refresh_callback):
        super().__init__(parent)
        self.title("Edit User")
        self.geometry("350x320")
        self.refresh = refresh_callback

        user_id, username, role = user_data
        self.user_id = user_id

        ctk.CTkLabel(self, text="Edit User", font=("Arial", 16)).pack(pady=12)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.insert(0, username)

        self.role_box = ctk.CTkComboBox(self, values=["admin", "viewer"])
        self.role_box.set(role)

        self.username.pack(pady=6, padx=20, fill="x")
        self.role_box.pack(pady=6, padx=20)

        ctk.CTkButton(self, text="Reset Password", command=self.reset_password).pack(pady=6)
        ctk.CTkButton(self, text="Save Changes", command=self.save_changes).pack(pady=6)

    def reset_password(self):
        new_pwd = simpledialog.askstring("Reset Password", "Enter new password:", parent=self, show="*")
        if not new_pwd:
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE Users SET Password=%s WHERE User_ID=%s",
                (hash_password(new_pwd), self.user_id)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Password updated")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_changes(self):
        new_username = self.username.get().strip()
        new_role = self.role_box.get()

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE Users SET Username=%s, Role=%s WHERE User_ID=%s",
                (new_username, new_role, self.user_id)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "User updated")
            self.refresh()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
