import tkinter as tk
from tkinter import ttk
from database_handler import DatabaseHandler

class StudentListing(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        
        self.tree = ttk.Treeview(
            self,
            columns=('ID', 'Name', 'Email', 'Age', 'Gender'),
            show='headings',
            selectmode='browse',
            height=15
        )

        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Gender', text='Gender')

        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Name', width=150, anchor='w')
        self.tree.column('Email', width=200, anchor='w')
        self.tree.column('Age', width=50, anchor='center')
        self.tree.column('Gender', width=80, anchor='center')

        
        self.tree.pack(side='left', fill='both', expand=True, padx=(0,0), pady=10)

        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y', pady=10)

        
        self.tree.tag_configure('oddrow', background='lightblue')
        self.tree.tag_configure('evenrow', background='white')

    def load_students(self):
        
        for row in self.tree.get_children():
            self.tree.delete(row)

        
        students = DatabaseHandler.get_all_students()
        for index, student in enumerate(students):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert('', tk.END, values=student, tags=(tag,))
