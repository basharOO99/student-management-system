import tkinter as tk
from tkinter import messagebox
from registration_form import RegistrationForm
from student_listing import StudentListing
from database_handler import DatabaseHandler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.state('zoomed')
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        
        tk.Label(
            self, text="Welcome to the Student Management System",
            font=("Helvetica", 24, "bold"),
            bg='white'
        ).pack(side='top', fill='x', pady=20)

       
        self.registration_form = RegistrationForm(self, self.refresh_listing)
        self.registration_form.pack(fill='x', padx=20, pady=10)

       
        self.student_listing = StudentListing(self)
        self.student_listing.pack(fill='both', expand=True, padx=20, pady=10)

        
        self.visualize_button = tk.Button(
            self,
            text="Visualize Gender Distribution",
            bg='#2196F3',
            fg='white',
            font=("Helvetica", 12, "bold"),
            command=self.visualize_gender_distribution
        )
        self.visualize_button.pack(fill='x', padx=20, pady=10)

    def refresh_listing(self):
        
        self.student_listing.load_students()

    def visualize_gender_distribution(self):
        
        try:
            gender_counts = DatabaseHandler.get_gender_count()
            male_count = gender_counts.get('male', 0)
            female_count = gender_counts.get('female', 0)

            if male_count == 0 and female_count == 0:
                messagebox.showinfo("No Data", "No students registered yet to visualize.")
                return

            labels = ['Male', 'Female']
            sizes = [male_count, female_count]
            colors = ['skyblue', 'lightpink']

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.set_title("Gender Distribution", fontsize=14)

           
            chart_window = tk.Toplevel(self)
            chart_window.title("Gender Distribution")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while visualizing:\n{e}")


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
