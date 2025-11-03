
import tkinter as tk
from tkinter import messagebox
from database_handler import DatabaseHandler  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RegistrationForm(tk.Frame):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent,padx=10,pady=10)
        self.refresh_callback = refresh_callback
        
        tk.Label(self, text="Full name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(fill='x')

        tk.Label(self, text='Email').pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(fill='x')

        tk.Label(self, text='Age').pack()
        self.age_spinbox = tk.Spinbox(self, from_=1, to=90)
        self.age_spinbox.pack(fill='x')
            
        tk.Label(self, text='Gender').pack(pady=5)

     
        self.gender_var = tk.StringVar()
        self.gender_var.set("") 

       
        tk.Radiobutton(self, text='Male', variable=self.gender_var, value='male').pack(anchor='w')
        tk.Radiobutton(self, text='Female', variable=self.gender_var, value='female').pack(anchor='w')

       
        self.submit_button = tk.Button(self, text='Submit', command=self.submit_form)
        self.submit_button.pack(fill='x')

    def submit_form(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        age_text = self.age_spinbox.get().strip()
        gender = self.gender_var.get().strip()

       
        if not (name and email and age_text and gender):
            messagebox.showwarning("Validation", "Please fill all fields.")
            return

   
        try:
            age = int(age_text)
        except ValueError:
            messagebox.showerror("Validation", "Age must be a number.")
            return

        
        try:
            DatabaseHandler.insert_student(name, email, age, gender)
            self.refresh_callback()  
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save student:\n{e}")
            return

        messagebox.showinfo("Success", "Registration Successful!")
        self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        
        self.age_spinbox.delete(0, tk.END)
        self.age_spinbox.insert(0, "1")
        self.gender_var.set("")
