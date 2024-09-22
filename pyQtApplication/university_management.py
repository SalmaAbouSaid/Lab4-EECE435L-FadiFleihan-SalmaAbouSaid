import sys
import json 
import csv
import os 
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFormLayout, QLineEdit, QPushButton, QComboBox, QTableWidget, QLabel, QMessageBox, QTabWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from classes import Student, Instructor, Course
from models import student_schema, StudentTable, instructor_schema, InstructorTable, course_schema, course_schema, CourseTable, session

class SchoolManagementSystem(QMainWindow):
    """This class is made for the interface of managing university courses, their instructors, and the student records. This class inherits from QMainWindow which 
    defined in the PyQt library. 

    Raises:
        ValueError: if instructor not found 
        ValueError: if student not found 
    """
    students = []
    instructors =[]
    courses = []
    def __init__(self):
        """
        Initialize the main window of the School Management System.

        This method sets up the main window with the title, dimensions, and a tabbed 
        interface using QTabWidget. The tabbed interface contains three sections:
        Students, Instructors, and Courses. Each tab is created and populated by 
        separate methods.

        :Attributes:
            - **tabs** (:class:`QTabWidget`): The widget managing multiple sections (tabs) for Students, Instructors, and Courses.
            - **student_tab** (:class:`QWidget`): The tab dedicated to managing student information.
            - **instructor_tab** (:class:`QWidget`): The tab dedicated to managing instructor information.
            - **course_tab** (:class:`QWidget`): The tab dedicated to managing course information.

        :Methods:
            - :meth:`create_student_tab`: Populates the Students tab with relevant fields and data.
            - :meth:`create_instructor_tab`: Populates the Instructors tab with relevant fields and data.
            - :meth:`create_course_tab`: Populates the Courses tab with relevant fields and data.
        
        :Raises:
            None
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
                
        # Create the QTabWidget
        self.tabs = QTabWidget()

        # Create individual pages for each section
        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()

        # Add the pages to the QTabWidget
        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.instructor_tab, "Instructors")
        self.tabs.addTab(self.course_tab, "Courses")

        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()

        # Set the QTabWidget as the central widget of the main window
        self.setCentralWidget(self.tabs)

    def create_student_tab(self):
        """creates a student tab GUI. """
        layout = QFormLayout()

        # Add forms for Students
        layout = QFormLayout()
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()
        self.student_registered_courses = QComboBox()
        self.student_registered_courses.addItems([self.courses[i].course_name for i in range(len(self.courses))])
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)

        layout.addRow("Name:", self.student_name)
        layout.addRow("Age:", self.student_age)
        layout.addRow("Email:", self.student_email)
        layout.addRow("Student ID:", self.student_id)
        layout.addRow("Registered courses:", self.student_registered_courses)

        layout.addRow(add_student_button)

        # Add Section Label for Records
        student_record_label = QLabel("Student Record")
        student_record_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(student_record_label)

        # Create Table to display records
        self.student_record_table = QTableWidget()
        self.student_record_table.setColumnCount(4)  
        self.student_record_table.setHorizontalHeaderLabels(["Name", "ID", "Age", "Email", "Registered Courses"])
        self.update_student_table()
        layout.addWidget(self.student_record_table)

        # # Search field
        # self.student_search_field = QLineEdit()
        # self.student_search_field.setPlaceholderText("Search by Name, ID, or Course")
        # self.student_search_field.textChanged.connect(self.student_search_records)
        # layout.addWidget(self.student_search_field)

        self.student_tab.setLayout(layout)

        # Save, Load, and export buttons
        self.save_button = QPushButton("Save Data")
        self.load_button = QPushButton("Load Data")
        self.export_button = QPushButton("Export to CSV")

        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data_students)
        self.export_button.clicked.connect(self.export_to_csv)

        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.export_button)
    
    def create_instructor_tab(self):
        """creates instructor tab GUI."""
        layout = QFormLayout()

        # Add forms for instructors 
        layout = QFormLayout()
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()
        self.instructor_assigned_courses = QComboBox()
        self.instructor_assigned_courses.addItems([self.courses[i].course_name for i in range(len(self.courses))])
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)

        layout.addRow("Name:", self.instructor_name)
        layout.addRow("Age:", self.instructor_age)
        layout.addRow("Email:", self.instructor_email)
        layout.addRow("Instructor ID:", self.instructor_id)
        layout.addRow("Assigned Courses:", self.instructor_assigned_courses)

        layout.addRow(add_instructor_button)

        # Add Section Label for Records
        instructor_record_label = QLabel("Instruction Record")
        instructor_record_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(instructor_record_label)

        # Create Table to display records
        self.instructor_table_record = QTableWidget()
        self.instructor_table_record.setColumnCount(5) 
        self.instructor_table_record.setHorizontalHeaderLabels(["Name", "ID", "Age", "Email", "Assigned Courses"])
        self.update_instructor_table()
        layout.addWidget(self.instructor_table_record)

        # # Search field
        # self.instructor_search_field = QLineEdit()
        # self.instructor_search_field.setPlaceholderText("Search by Name, ID, or Course")
        # self.instructor_search_field.textChanged.connect(self.instructor_search_records)
        # layout.addWidget(self.instructor_search_field)

        self.instructor_tab.setLayout(layout)

        # Save, Load, and export buttons
        self.save_button = QPushButton("Save Data")
        self.load_button = QPushButton("Load Data")
        self.export_button = QPushButton("Export to CSV")

        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data_instructors)
        self.export_button.clicked.connect(self.export_to_csv)
        
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.export_button)
    
    def create_course_tab(self):
        """creates course tab GUI"""
        layout = QFormLayout()
        
        #add form for courses
        layout = QFormLayout()
        self.course_name = QLineEdit()
        self.course_id = QLineEdit()
        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.addItems([self.instructors[i].name for i in range(len(self.instructors))])
        self.student_dropdown = QComboBox()
        self.student_dropdown.addItems([self.students[i].name for i in range(len(self.students))])
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)

        layout.addRow("Course Name:", self.course_name)
        layout.addRow("Course ID:", self.course_id)
        layout.addRow("Assign Instructor:", self.instructor_dropdown)
        layout.addRow("Enrolled Student:", self.student_dropdown)
        layout.addRow(add_course_button)

        # Add Section Label for Records
        course_record_label = QLabel("Course Record")
        course_record_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(course_record_label)

        # Create Table to display records
        self.course_record_table = QTableWidget()
        self.course_record_table.setColumnCount(3) 
        self.course_record_table.setHorizontalHeaderLabels(["Name", "ID", "Instructor"])
        self.update_course_table()
        layout.addWidget(self.course_record_table)

        self.course_tab.setLayout(layout)

        # Save, Load, and export buttons
        self.save_button = QPushButton("Save Data")
        self.load_button = QPushButton("Load Data")
        self.export_button = QPushButton("Export to CSV")

        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data_courses)
        self.export_button.clicked.connect(self.export_to_csv)
        
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.export_button)
        
    def add_student(self):
        """
        Adds a new student to the system.

        This method retrieves student details from the form, validates the input,
        and creates a `Student` object. If the validation is successful, the new
        student is added to the database and the UI is updated.

        Raises:
            ValueError: If age or student ID is not a valid integer.
            ValidationError: If the student data fails schema validation.
            Exception: For any other errors encountered during the process.

        Updates:
            - Adds the new student to the `students` list.
            - Updates the student table in the UI.

        Displays:
            - A message box indicating success or failure of the operation.

        Returns:
            None
        """
        # Logic to add student to system
        name = self.student_name.text()
        age = self.student_age.text()
        email = self.student_email.text()
        student_id = self.student_id.text()
        registered_course = [self.student_registered_courses.currentText()]

        # Validation and student object creation here
        try:
            age = int(age)
            student_id = int(student_id)
            student = Student(name, age, email, student_id, registered_course)
    
            validated_student = student_schema.load(
            {
               "name": student.name,
                "age": student.age,
                "email": student._email,
                "student_id": student.student_id,
                "courses": student.registered_courses
            }
            )

            # Add new student to the database
            new_student = StudentTable(
                name=validated_student["name"],
                age=validated_student["age"],
                email=validated_student["email"],
                student_id=validated_student["student_id"]
            )
            session.add(new_student)
            session.commit()

            self.students.append(student)
            self.update_student_table()
            QMessageBox.information(self, "Success", "Student added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            session.rollback()


    def add_instructor(self):
        """
        Adds a new instructor to the system.

        This method retrieves instructor details from the form, validates the input,
        and creates an `Instructor` object. If the validation is successful, the new
        instructor is added to the database and the UI is updated.

        Raises:
            ValueError: If age or instructor ID is not a valid integer.
            ValidationError: If the instructor data fails schema validation.
            Exception: For any other errors encountered during the process.

        Updates:
            - Adds the new instructor to the dropdown for instructor selection.
            - Updates the instructor table in the UI.

        Displays:
            - A message box indicating success or failure of the operation.

        Returns:
            None
        """
        # Logic to add instructor to system
        name = self.instructor_name.text()
        age = self.instructor_age.text()
        email = self.instructor_email.text()
        instructor_id = self.instructor_id.text()
        assigned_courses = [self.instructor_assigned_courses.currentText()]

        # Validation and instructor object creation here
        try:
            age = int(age)
            instructor_id = int(instructor_id)
            instructor = Instructor(name, age, email, instructor_id,assigned_courses)
            # Add instructor to dropdown or data structure
            self.instructor_dropdown.addItem(name)  # Simplified for demo

            validated_instructor = instructor_schema.load(
                {
                    "name": instructor.name,
                    "age": instructor.age,
                    "email": instructor._email,
                    "instructor_id": instructor.instructor_id
                }
            )

            # Add new instructor to the database
            new_instructor = InstructorTable(
                name=validated_instructor["name"],
                age=validated_instructor["age"],
                email=validated_instructor["email"],
                instructor_id=validated_instructor["instructor_id"]
            )
            session.add(new_instructor)
            session.commit()

            self.students.append(instructor)
            self.update_instructor_table()
            QMessageBox.information(self, "Success", "Instructor added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            session.rollback()

    def add_course(self):
        """
        Adds a new course to the system.

        This method retrieves course details from the form, validates the input,
        and creates a `Course` object. If the validation is successful, the new
        course is added to the database and the UI is updated.

        Raises:
            ValueError: If the course ID is not a valid integer or if the
                        specified instructor or student is not found.
            ValidationError: If the course data fails schema validation.
            Exception: For any other errors encountered during the process.

        Updates:
            - Adds the new course to the list of courses.
            - Updates dropdowns for registered courses and assigned courses.
            - Updates the course table in the UI.

        Displays:
            - A message box indicating success or failure of the operation.

        Returns:
            None
        """
        # Logic to add course to system
        course_name = self.course_name.text()
        course_id = self.course_id.text()
        instructor_name = self.instructor_dropdown.currentText()
        student_name = self.student_dropdown.currentText()

        # Validation and course object creation here
        try:
            course_id = int(course_id)

            # Find the instructor object from the list of instructors
            instructor = next((inst for inst in self.instructors if inst.name == instructor_name), None)
            if instructor is None:
                raise ValueError("Instructor not found.")

            student = next((std for std in self.students if std.name == student_name), None)
            if student is None:
                raise ValueError("Student not found.")

            # Create the course object
            course = Course(course_id, course_name, instructor, [student])
            self.courses.append(course)
            self.student_registered_courses.addItem(course.course_name)
            self.instructor_assigned_courses.addItem(course.course_name)
            
            validated_course = course_schema.load(
                {
                    "course_name": course.course_name,
                    "course_id": course.course_id,
                    "instructor_id": course.instructor.instructor_id
                }
            )

            # Add new instructor to the database
            new_course = CourseTable(
                course_name=validated_course["course_name"],
                course_id =validated_course["course_id"],
                instructor_id=validated_course["instructor_id"]
            )
            session.add(new_course)
            session.commit()
            
            self.update_course_table()
            
            QMessageBox.information(self, "Success", "Course added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            session.rollback()


    def update_student_table(self):
        """Update student table based on the students list."""
        self.student_record_table.setRowCount(len(self.students))

        for row, student in enumerate(self.students):
            self.student_record_table.setItem(row, 0, QTableWidgetItem(student.name))
            self.student_record_table.setItem(row, 1, QTableWidgetItem(str(student.student_id)))
            self.student_record_table.setItem(row, 2, QTableWidgetItem(str(student.age)))
            self.student_record_table.setItem(row, 3, QTableWidgetItem(student._email))
            registered_courses = ", ".join(str(student.registered_courses))
            self.student_record_table.setItem(row, 4, QTableWidgetItem(registered_courses))

    def update_instructor_table(self):
        """Update instructor table based on the instructors list."""
        self.instructor_table_record.setRowCount(len(self.instructors))

        for row, instructor in enumerate(self.instructors):
            self.instructor_table_record.setItem(row, 0, QTableWidgetItem(instructor.name))
            self.instructor_table_record.setItem(row, 1, QTableWidgetItem(str(instructor.instructor_id)))
            self.instructor_table_record.setItem(row, 2, QTableWidgetItem(str(instructor.age)))
            self.instructor_table_record.setItem(row, 3, QTableWidgetItem(instructor._email))
            assigned_courses = ", ".join(instructor.assigned_courses)
            self.instructor_table_record.setItem(row, 4, QTableWidgetItem(assigned_courses))

    def update_course_table(self):
        """Update course table based on the courses list."""
        self.course_record_table.setRowCount(len(self.courses))

        for row, course in enumerate(self.courses):
            self.course_record_table.setItem(row, 0, QTableWidgetItem(course.course_name))
            self.course_record_table.setItem(row, 1, QTableWidgetItem(str(course.course_id)))
            self.course_record_table.setItem(row, 2, QTableWidgetItem(course.instructor.name))


    def load_data_students(self, data):
        """Load student data from the given JSON data."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)
                for student_data in data.get('students', []):
                    # Find or create a student by student_id
                    student = next((s for s in self.students if s.student_id == student_data['student_id']), None)
                    if student:
                        student.name = student_data['name']
                        student.age = student_data['age']
                        student._email = student_data['_email']
                        student.registered_courses = student_data['registered_courses']
                    else:
                        # Create a new student if not found
                        new_student = Student(
                            student_data['name'],
                            student_data['age'],
                            student_data['_email'],
                            student_data['student_id'],
                            student_data['registered_courses']
                        )
                        self.students.append(new_student)
                self.update_student_table()
        
        #update dropdowns
        self.student_dropdown.addItems([self.students[i].name for i in range(len(self.students))])



    def load_data_courses(self, data):
        """Load course data from the given JSON data."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")

        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)
                
                for course_data in data.get('courses', []):
                    # Find or create a course by course_id
                    course = next((c for c in self.courses if c.course_id == course_data['course_id']), None)
                    if course:
                        course.course_name = course_data['course_name']
                        course.instructor = next((i for i in self.instructors if i.instructor_id == course_data['instructor_id']), None)
                        
                        # Match students by student_id (instead of student_name) from JSON data
                        course.enrolled_students = [
                            next((s for s in self.students if int(s.student_id) == int(student_id)), None)
                            for student_id in course_data['enrolled_students']
                        ]
                    else:
                        instructor = next((i for i in self.instructors if i.instructor_id == course_data['instructor_id']), None)
                        
                        if instructor is None:
                            print(f"Error: No instructor found with ID {course_data['instructor_id']}, or instructors have not been loaded yet.")
                        print(type(instructor))
                        # Create a new course if not found
                        new_course = Course(
                            course_data['course_id'],
                            course_data['course_name'],
                            instructor, 
                            [next((s for s in self.students if s.student_id == student_id), None)
                            for student_id in course_data['enrolled_students']]
                        )
                        self.courses.append(new_course)
                
                self.update_course_table()
        #update dropdown
        self.student_registered_courses.addItems([self.courses[i].course_name for i in range(len(self.courses))])
        self.instructor_assigned_courses.addItems([self.courses[i].course_name for i in range(len(self.courses))])


    def load_data_instructors(self, data):
        """Load instructor data from the given JSON data."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)
                for instructor_data in data.get('instructors', []):
                    # Find or create an instructor by instructor_id
                    instructor = next((i for i in self.instructors if i.instructor_id == instructor_data['instructor_id']), None)
                    if instructor:
                        instructor.name = instructor_data['name']
                        instructor.age = instructor_data['age']
                        instructor._email = instructor_data['_email']
                        instructor.assigned_courses = instructor_data['assigned_courses']
                    else:
                        # Create a new instructor if not found
                        new_instructor = Instructor(
                            instructor_data['name'],
                            instructor_data['age'],
                            instructor_data['_email'],
                            instructor_data['instructor_id'],
                            instructor_data['assigned_courses']
                        )
                        self.instructors.append(new_instructor)
                self.update_instructor_table()
        #update dropdowns
        self.instructor_dropdown.addItems([self.instructors[i].name for i in range(len(self.instructors))])

            
    def update_json_data_students(self):
        """
        Update the JSON file with current student data.

        This method collects data from all students in the system and
        writes it to a JSON file named 'data.json'. Each student's
        details, including name, age, email, student ID, and registered
        courses, are stored in a structured format.

        Raises:
            IOError: If the file cannot be opened for writing.
            Exception: For any other errors encountered during the process.

        Returns:
            None
        """
        file_name="data.json"
        data = {
            'students': [
                {
                    'name': student.name,
                    'age': student.age,
                    '_email': student._email,
                    'student_id': student.student_id,
                    'registered_courses': student.registered_courses
                } for student in self.students
            ]
        }
        with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)

    def update_json_data_instructors(self):
        """
        Update the JSON file with current instructor data.

        This method collects data from all instructors in the system and
        writes it to a JSON file named 'data.json'. Each instructor's
        details, including name, age, email, instructor ID, and assigned
        courses, are stored in a structured format.

        Raises:
            IOError: If the file cannot be opened for writing.
            Exception: For any other errors encountered during the process.

        Returns:
            None
        """
        file_name="data.json"
        data = {
             'instructors': [
                {
                    'name': instructor.name,
                    'age': instructor.age,
                    '_email': instructor._email,
                    'instructor_id': instructor.instructor_id,
                    'assigned_courses': instructor.assigned_courses
                } for instructor in self.instructors
            ]
        }
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    
    def update_json_data_courses(self):
        """
        Update the JSON file with current course data.

        This method collects data from all courses in the system and
        writes it to a JSON file named 'data.json'. Each course's
        details, including course_name, id, instructor, and students are stored in a structured format.

        Raises:
            IOError: If the file cannot be opened for writing.
            Exception: For any other errors encountered during the process.

        Returns:
            None
        """
        file_name="data.json"
        data = {
            'courses': [
                {
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'instructor_id': course.instructor.instructor_id,
                    'enrolled_students': [student.student_id for student in course.enrolled_students]
                } for course in self.courses
            ]
        }

        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def save_data(self):
        """
        updates all json data.

        Returns:
            None
        """
        self.update_json_data_students()
        self.update_json_data_instructors()
        self.update_json_data_courses()
    
    def export_to_csv(self):
        """
        Export current student, instructor, and course data to a CSV file.

        This method loads data from existing JSON files for students, instructors,
        and courses, and writes the consolidated data into a CSV file named
        'exported_csv.csv' in the current working directory. The CSV file is organized
        into three sections: Students, Instructors, and Courses, each with a header row.

        Raises:
            IOError: If any of the JSON files cannot be opened or read.
            Exception: For any other errors encountered during the CSV writing process.

        Returns:
            None
        """
        file_name = os.path.join(os.getcwd(), 'exported_csv.csv')
        
        if not file_name:
            return  # If no file is selected, return
        
        # Load data from JSON files
        with open('student_data.json', 'r') as file:
            student_data = json.load(file)
        
        with open('instructor_data.json', 'r') as file:
            instructor_data = json.load(file)
        
        with open('courses_data.json', 'r') as file:
            courses_data = json.load(file)
        
        # Open the CSV file and write the data
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write header for Students
            writer.writerow(["Students Data"])
            writer.writerow(["Name", "ID", "Age", "Email", "Registered Courses"])
            for student in student_data.get('students', []):
                writer.writerow([
                    student['name'],
                    student['student_id'],
                    student['age'],
                    student['_email'],
                    ", ".join(map(str, student['registered_courses']))
                ])
            
            # Add a blank row to separate sections
            writer.writerow([])
            
            # Write header for Instructors
            writer.writerow(["Instructors Data"])
            writer.writerow(["Name", "ID", "Age", "Email", "Assigned Courses"])
            for instructor in instructor_data.get('instructors', []):
                writer.writerow([
                    instructor['name'],
                    instructor['instructor_id'],
                    instructor['age'],
                    instructor['_email'],
                    ", ".join(map(str, instructor['assigned_courses']))
                ])
            
            # Add a blank row to separate sections
            writer.writerow([])
            
            # Write header for Courses
            writer.writerow(["Courses Data"])
            writer.writerow(["Course ID", "Course Name", "Instructor ID", "Enrolled Students"])
            for course in courses_data.get('courses', []):
                writer.writerow([
                    course['course_id'],
                    course['course_name'],
                    course['instructor_id'],
                    ", ".join(map(str, course['enrolled_students']))
                ])
        
        print("All data exported successfully to CSV.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())

