import json 
import csv 
import re

# PART ONE: CREATE CLASSES
class Person():
    """
    Represents a person.

    Attributes:
        name (str): The name of the person.
        age (int): The age of the person.
        _email (str): The email address of the person.

    Methods:
        introduce(): Prints a greeting with the person's name and age.
    """
    def __init__(self, name, age, _email):
        """
        Initializes a Person instance.

        Args:
            name (str): The name of the person.
            age (int): The age of the person (must be greater than 0).
            _email (str): The email address of the person.

        Raises:
            AssertionError: If name is not a string or age is not a positive integer.
            ValueError: If email is not in the correct format.
        """
        assert isinstance(name, str), "Name must be a string."
        assert isinstance(age, int), "Age must be an integer."
        assert age>0, "Age must be greater than 0."

        #defining regex patters for emails
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, _email):
            raise ValueError("Email must be in the format localpart@domain.extension")
        
        self.name = name
        self.age = age
        self._email = _email
    def introduce(self):
        """Prints a greeting including the person's name and age."""
        print(f"Hello! My name is {self.name} and I'm {self.age} years old. ")

class Student(Person):
    """
    Represents a student, inheriting from Person.

    Attributes:
        student_id (int): The unique identifier for the student.
        registered_courses (list): A list of courses the student is registered for.

    Methods:
        register_course(course): Adds a course to the student's registered courses.
    """
    def __init__(self, name, age, _email, student_id, registered_courses):
        """
        Initializes a Student instance.

        Args:
            name (str): The name of the student.
            age (int): The age of the student (must be greater than 0).
            _email (str): The email address of the student.
            student_id (int): The unique identifier for the student.
            registered_courses (list): A list of courses the student is registered for.

        Raises:
            AssertionError: If student_id is not an integer or registered_courses is not a list.
        """
        assert isinstance(student_id,int), "student_id must be an integer."
        assert isinstance(registered_courses,list), "registered_courses must be a list."
        super().__init__(name, age, _email)
        self.student_id = student_id
        self.registered_courses = registered_courses
    def register_course(self,course):
        """Adds a course to the list of registered courses."""
        self.registered_courses.append(course)

class Instructor(Person):
    """
    Represents an instructor, inheriting from Person.

    Attributes:
        instructor_id (int): The unique identifier for the instructor.
        assigned_courses (list): A list of courses assigned to the instructor.

    Methods:
        assign_course(course): Adds a course to the instructor's assigned courses.
    """
    def __init__(self, name, age, _email, instructor_id, assigned_courses):
        """
        Initializes an Instructor instance.

        Args:
            name (str): The name of the instructor.
            age (int): The age of the instructor (must be greater than 0).
            _email (str): The email address of the instructor.
            instructor_id (int): The unique identifier for the instructor.
            assigned_courses (list): A list of courses assigned to the instructor.

        Raises:
            AssertionError: If instructor_id is not an integer or assigned_courses is not a list.
        """
        assert isinstance(instructor_id,int), "instructor_id must be an int."
        assert isinstance(assigned_courses,list), "assigned_courses must be a list."
        super().__init__(name,age,_email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses
    def assign_course(self,course):
        self.assigned_courses.append(course)

class Course():
    """
    Represents a course.

    Attributes:
        course_id (int): The unique identifier for the course.
        course_name (str): The name of the course.
        instructor (Instructor): The instructor teaching the course.
        enrolled_students (list): A list of students enrolled in the course.

    Methods:
        add_student(student): Adds a student to the list of enrolled students.
    """
    def __init__(self,course_id, course_name, instructor, enrolled_students):
        """
        Initializes a Course instance.

        Args:
            course_id (int): The unique identifier for the course.
            course_name (str): The name of the course.
            instructor (Instructor): The instructor teaching the course.
            enrolled_students (list): A list of students enrolled in the course.

        Raises:
            AssertionError: If course_id is not an integer, course_name is not a string,
                            instructor is not of type Instructor, or enrolled_students is not a list.
        """
        assert isinstance(course_id,int), "course_id must be an integer."
        assert isinstance(course_name,str), "course_name must be a str."
        assert isinstance(instructor,Instructor), "instructor must be of type Instructor."
        assert isinstance(enrolled_students, list), "enrolled_students must be a list."
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students

    def add_student(self, student):
        """Adds a student to the list of enrolled students."""
        self.enrolled_students.append(student)

#STEP 2:READ FROM FILE (JSON OR CSV)
def read_from_file(file_path):
    """
    Reads data from a specified file.

    This function supports reading from both JSON and CSV file formats.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list or dict: The data read from the file, parsed as a dictionary (for JSON) 
                       or a list of dictionaries (for CSV).

    Raises:
        ValueError: If the file format is unsupported (not .json or .csv).
    """
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    elif file_path.endswith('.csv'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return list(csv.DictReader(file))     
    else:
        raise ValueError("Unsupported file format. Please provide a .json or .csv file.")

# print( read_from_file("fileToReadFrom.csv") )

