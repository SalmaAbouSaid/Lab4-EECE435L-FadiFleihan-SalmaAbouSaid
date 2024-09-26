import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import shutil

# Connect to SQLite database
conn = sqlite3.connect("school_management.db")
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS students (
             id INTEGER PRIMARY KEY, 
             name TEXT, 
             age INTEGER, 
             student_id TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS instructors (
             id INTEGER PRIMARY KEY, 
             name TEXT, 
             instructor_id TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS courses (
             id INTEGER PRIMARY KEY, 
             course_name TEXT, 
             course_id TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS student_course (
             student_id TEXT, 
             course_id TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS instructor_course (
             instructor_id TEXT, 
             course_id TEXT)''')
conn.commit()

root = tk.Tk()
root.title("School Management System")
root.geometry("900x600")

def get_all_students():
    """
    Fetch all student records from the students table.
    
    Returns:
        List of tuples: Each tuple contains information about a student.
    """
    c.execute("SELECT * FROM students")
    return c.fetchall()

def get_all_instructors():
    """
    Fetch all instructor records from the instructors table.
    
    Returns:
        List of tuples: Each tuple contains information about an instructor.
    """
    c.execute("SELECT * FROM instructors")
    return c.fetchall()

def get_all_courses():
    """
    Fetch all course records from the courses table.
    
    Returns:
        List of tuples: Each tuple contains information about a course.
    """
    c.execute("SELECT * FROM courses")
    return c.fetchall()

def add_student():
    """
    Add a student to the students table in the SQLite database.
    The student's name, age, and ID are taken from the entry fields.
    """
    name = name_entry.get()
    age = age_entry.get()
    student_id = student_id_entry.get()
    try:
        c.execute("INSERT INTO students (name, age, student_id) VALUES (?, ?, ?)", 
                  (name, age, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        student_id_entry.delete(0, tk.END)
        refresh_tree()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID must be unique!")

def add_instructor():
    """
    Add an instructor to the instructors table in the SQLite database.
    The instructor's name and ID are taken from the entry fields.
    """
    instructor_name = instructor_name_entry.get()
    instructor_id = instructor_id_entry.get()
    try:
        c.execute("INSERT INTO instructors (name, instructor_id) VALUES (?, ?)", 
                  (instructor_name, instructor_id))
        conn.commit()
        messagebox.showinfo("Success", "Instructor added successfully!")
        instructor_name_entry.delete(0, tk.END)
        instructor_id_entry.delete(0, tk.END)
        refresh_tree()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Instructor ID must be unique!")

def add_course():
    """
    Add a course to the courses table in the SQLite database.
    The course's name and ID are taken from the entry fields.
    """
    course_name = course_name_entry.get()
    course_id = course_id_entry.get()
    try:
        c.execute("INSERT INTO courses (course_name, course_id) VALUES (?, ?)", 
                  (course_name, course_id))
        conn.commit()
        messagebox.showinfo("Success", "Course added successfully!")
        course_name_entry.delete(0, tk.END)
        course_id_entry.delete(0, tk.END)
        refresh_tree()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Course ID must be unique!")

def assign_student_to_course():
    """
    Assign a selected student to a selected course.
    Updates the student_course table in the database.
    """
    selected_student = student_combobox.get()
    selected_course = course_combobox.get()
    student_id = next(s[3] for s in get_all_students() if s[1] == selected_student)
    course_id = next(c[2] for c in get_all_courses() if c[1] == selected_course)
    c.execute("INSERT INTO student_course (student_id, course_id) VALUES (?, ?)", 
              (student_id, course_id))
    conn.commit()
    refresh_tree()

def assign_instructor_to_course():
    """
    Assign a selected instructor to a selected course.
    Updates the instructor_course table in the database.
    """
    selected_instructor = instructor_combobox.get()
    selected_course = instructor_course_combobox.get()
    instructor_id = next(i[2] for i in get_all_instructors() if i[1] == selected_instructor)
    course_id = next(c[2] for c in get_all_courses() if c[1] == selected_course)
    c.execute("INSERT INTO instructor_course (instructor_id, course_id) VALUES (?, ?)", 
              (instructor_id, course_id))
    conn.commit()
    refresh_tree()

def refresh_tree():
    """
    Refresh the treeview widget to display the latest data from the database.
    Populates the treeview with both student and instructor assignments.
    """
    for row in tree.get_children():
        tree.delete(row)

    c.execute('''SELECT students.name, courses.course_name 
                 FROM student_course 
                 INNER JOIN students ON student_course.student_id = students.student_id 
                 INNER JOIN courses ON student_course.course_id = courses.course_id''')
    for row in c.fetchall():
        tree.insert("", tk.END, values=("Student", row[0], "", row[1]))

    c.execute('''SELECT instructors.name, courses.course_name 
                 FROM instructor_course 
                 INNER JOIN instructors ON instructor_course.instructor_id = instructors.instructor_id 
                 INNER JOIN courses ON instructor_course.course_id = courses.course_id''')
    for row in c.fetchall():
        tree.insert("", tk.END, values=("Instructor", row[0], "", row[1]))

def delete_record():
    """
    Delete a record (student or instructor assignment) from the treeview and the database.
    """
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No item selected to delete.")
        return
    values = tree.item(selected_item)['values']
    if values[0] == "Student":
        student_id = next(s[3] for s in get_all_students() if s[1] == values[1])
        c.execute("DELETE FROM student_course WHERE student_id = ?", (student_id,))
    else:
        instructor_id = next(i[2] for i in get_all_instructors() if i[1] == values[1])
        c.execute("DELETE FROM instructor_course WHERE instructor_id = ?", (instructor_id,))
    conn.commit()
    refresh_tree()

def search_records():
    """
    Search for records in the treeview based on user input in the search field.
    Filters records by matching student names, instructor names, or course names.
    """
    query = search_entry.get().lower()
    for row in tree.get_children():
        tree.delete(row)

    c.execute('''SELECT students.name, courses.course_name 
                 FROM student_course 
                 INNER JOIN students ON student_course.student_id = students.student_id 
                 INNER JOIN courses ON student_course.course_id = courses.course_id 
                 WHERE students.name LIKE ? OR courses.course_name LIKE ?''', 
              (f"%{query}%", f"%{query}%"))
    for row in c.fetchall():
        tree.insert("", tk.END, values=("Student", row[0], "", row[1]))

    c.execute('''SELECT instructors.name, courses.course_name 
                 FROM instructor_course 
                 INNER JOIN instructors ON instructor_course.instructor_id = instructors.instructor_id 
                 INNER JOIN courses ON instructor_course.course_id = courses.course_id 
                 WHERE instructors.name LIKE ? OR courses.course_name LIKE ?''', 
              (f"%{query}%", f"%{query}%"))
    for row in c.fetchall():
        tree.insert("", tk.END, values=("Instructor", row[0], "", row[1]))

def reset_search():
    """
    Reset the search field and refresh the treeview to display all records again.
    """
    search_entry.delete(0, tk.END)
    refresh_tree()

def backup_database():
    """
    Create a backup of the current database file.
    The backup is stored as 'school_management_backup.db'.
    """
    try:
        shutil.copy("school_management.db", "school_management_backup.db")
        messagebox.showinfo("Success", "Database backup created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create backup: {str(e)}")

def fetch_latest_data():
    """
    Fetch the latest data from the database and refresh the treeview.
    """
    refresh_tree()


notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# GUI components for Add Student, Add Instructor, Add Course, Assignments
student_tab = ttk.Frame(notebook)
notebook.add(student_tab, text="Students")

name_label = tk.Label(student_tab, text="Name:")
name_label.grid(row=1, column=0, padx=10, pady=5)
name_entry = tk.Entry(student_tab)
name_entry.grid(row=1, column=1, padx=10, pady=5)

age_label = tk.Label(student_tab, text="Age:")
age_label.grid(row=2, column=0, padx=10, pady=5)
age_entry = tk.Entry(student_tab)
age_entry.grid(row=2, column=1, padx=10, pady=5)

student_id_label = tk.Label(student_tab, text="Student ID:")
student_id_label.grid(row=3, column=0, padx=10, pady=5)
student_id_entry = tk.Entry(student_tab)
student_id_entry.grid(row=3, column=1, padx=10, pady=5)

add_student_button = tk.Button(student_tab, text="Add Student", command=add_student)
add_student_button.grid(row=4, column=1, padx=10, pady=5)

# Instructor Tab
instructor_tab = ttk.Frame(notebook)
notebook.add(instructor_tab, text="Instructors")

instructor_name_label = tk.Label(instructor_tab, text="Name:")
instructor_name_label.grid(row=1, column=0, padx=10, pady=5)
instructor_name_entry = tk.Entry(instructor_tab)
instructor_name_entry.grid(row=1, column=1, padx=10, pady=5)

instructor_id_label = tk.Label(instructor_tab, text="Instructor ID:")
instructor_id_label.grid(row=2, column=0, padx=10, pady=5)
instructor_id_entry = tk.Entry(instructor_tab)
instructor_id_entry.grid(row=2, column=1, padx=10, pady=5)

add_instructor_button = tk.Button(instructor_tab, text="Add Instructor", command=add_instructor)
add_instructor_button.grid(row=3, column=1, padx=10, pady=5)

# Course Tab
course_tab = ttk.Frame(notebook)
notebook.add(course_tab, text="Courses")

course_name_label = tk.Label(course_tab, text="Course Name:")
course_name_label.grid(row=1, column=0, padx=10, pady=5)
course_name_entry = tk.Entry(course_tab)
course_name_entry.grid(row=1, column=1, padx=10, pady=5)

course_id_label = tk.Label(course_tab, text="Course ID:")
course_id_label.grid(row=2, column=0, padx=10, pady=5)
course_id_entry = tk.Entry(course_tab)
course_id_entry.grid(row=2, column=1, padx=10, pady=5)

add_course_button = tk.Button(course_tab, text="Add Course", command=add_course)
add_course_button.grid(row=3, column=1, padx=10, pady=5)

# Assign Student to Course
assign_tab = ttk.Frame(notebook)
notebook.add(assign_tab, text="Assign Student to Course")

assign_label = tk.Label(assign_tab, text="Assign a Student to a Course")
assign_label.grid(row=0, column=1, padx=10, pady=5)

student_combobox_label = tk.Label(assign_tab, text="Select Student:")
student_combobox_label.grid(row=1, column=0, padx=10, pady=5)

student_combobox = ttk.Combobox(assign_tab, values=[s[1] for s in get_all_students()])
student_combobox.grid(row=1, column=1, padx=10, pady=5)

course_combobox_label = tk.Label(assign_tab, text="Select Course:")
course_combobox_label.grid(row=2, column=0, padx=10, pady=5)

course_combobox = ttk.Combobox(assign_tab, values=[c[1] for c in get_all_courses()])
course_combobox.grid(row=2, column=1, padx=10, pady=5)

assign_button = tk.Button(assign_tab, text="Assign", command=assign_student_to_course)
assign_button.grid(row=3, column=1, padx=10, pady=5)

# Assign Instructor to Course
assign_instructor_tab = ttk.Frame(notebook)
notebook.add(assign_instructor_tab, text="Assign Instructor to Course")

instructor_combobox_label = tk.Label(assign_instructor_tab, text="Select Instructor:")
instructor_combobox_label.grid(row=1, column=0, padx=10, pady=5)

instructor_combobox = ttk.Combobox(assign_instructor_tab, values=[i[1] for i in get_all_instructors()])
instructor_combobox.grid(row=1, column=1, padx=10, pady=5)

instructor_course_combobox_label = tk.Label(assign_instructor_tab, text="Select Course:")
instructor_course_combobox_label.grid(row=2, column=0, padx=10, pady=5)

instructor_course_combobox = ttk.Combobox(assign_instructor_tab, values=[c[1] for c in get_all_courses()])
instructor_course_combobox.grid(row=2, column=1, padx=10, pady=5)

assign_instructor_button = tk.Button(assign_instructor_tab, text="Assign", command=assign_instructor_to_course)
assign_instructor_button.grid(row=3, column=1, padx=10, pady=5)

# View Records Tab with TreeView
record_tab = ttk.Frame(notebook)
notebook.add(record_tab, text="View Records")

columns = ("Role", "Name", "ID", "Course")
tree = ttk.Treeview(record_tab, columns=columns, show="headings")
tree.heading("Role", text="Role")
tree.heading("Name", text="Name")
tree.heading("ID", text="ID")
tree.heading("Course", text="Course")
tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Edit and Delete Buttons
edit_button = tk.Button(record_tab, text="Edit", command=lambda: messagebox.showinfo("Info", "Edit functionality coming soon!"))
edit_button.grid(row=1, column=2, padx=10, pady=5)

delete_button = tk.Button(record_tab, text="Delete", command=delete_record)
delete_button.grid(row=1, column=3, padx=10, pady=5)

# Save and Load Buttons
backup_button = tk.Button(record_tab, text="Backup Database", command=backup_database)
backup_button.grid(row=2, column=2, padx=10, pady=5)

fetch_button = tk.Button(record_tab, text="Fetch Latest Data", command=fetch_latest_data)
fetch_button.grid(row=2, column=3, padx=10, pady=5)

# Search Field and Button
search_label = tk.Label(record_tab, text="Search by Name or Course:")
search_label.grid(row=3, column=0, padx=10, pady=5)

search_entry = tk.Entry(record_tab)
search_entry.grid(row=3, column=1, padx=10, pady=5)

search_button = tk.Button(record_tab, text="Search", command=search_records)
search_button.grid(row=3, column=2, padx=10, pady=5)

reset_button = tk.Button(record_tab, text="Reset", command=reset_search)
reset_button.grid(row=3, column=3, padx=10, pady=5)

root.mainloop()