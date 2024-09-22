from marshmallow import Schema, fields, validate
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Define a relationship table between students and courses
student_course = Table('student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class StudentTable(Base):
    """
    Represents a student in the database.

    Attributes:
        id (int): The primary key for the student.
        name (str): The name of the student.
        age (int): The age of the student.
        email (str): The email of the student.
        student_id (str): A unique identifier for the student.
        courses (relationship): The courses associated with the student.
    """
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=False)
    student_id = Column(String, nullable=False, unique=True)
    courses = relationship('CourseTable', secondary=student_course, back_populates='students')

class InstructorTable(Base):
    """
    Represents an instructor in the database.

    Attributes:
        id (int): The primary key for the instructor.
        name (str): The name of the instructor.
        age (int): The age of the instructor.
        email (str): The email of the instructor.
        instructor_id (str): A unique identifier for the instructor.
        courses (relationship): The courses taught by the instructor.
    """
    __tablename__ = 'instructors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    instructor_id = Column(String, nullable=False, unique=True)
    courses = relationship('CourseTable', back_populates='instructor')

class CourseTable(Base):
    """
    Represents a course in the database.

    Attributes:
        id (int): The primary key for the course.
        course_name (str): The name of the course.
        course_id (str): A unique identifier for the course.
        instructor_id (int): The ID of the instructor teaching the course.
        instructor (relationship): The instructor associated with the course.
        students (relationship): The students enrolled in the course.
    """
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    course_id = Column(String, nullable=False, unique=True)
    instructor_id = Column(Integer, ForeignKey('instructors.id'))
    instructor = relationship('InstructorTable', back_populates='courses')
    students = relationship('StudentTable', secondary=student_course, back_populates='courses')

# Database setup
engine = create_engine('sqlite:///student_management.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class StudentSchema(Schema):
    """
    Schema for validating student data.

    Fields:
        name (str): The name of the student (required).
        age (int): The age of the student (required, must be > 0).
        email (str): The email of the student (required, must be a valid email).
        student_id (int): The unique identifier for the student (required).
        courses (list): A list of courses associated with the student (optional).
    """
    name = fields.String(required=True, validate=validate.Length(min=1))
    age = fields.Integer(required=True, validate=lambda n: n > 0)
    email = fields.Email(required=True)
    student_id = fields.Integer(required=True)
    courses = fields.List(fields.String())  # Assuming you're passing course names or IDs

class InstructorSchema(Schema):
    """
    Schema for validating instructor data.

    Fields:
        name (str): The name of the instructor (required).
        age (int): The age of the instructor (required, must be > 0).
        email (str): The email of the instructor (required, must be a valid email).
        instructor_id (int): The unique identifier for the instructor (required).
        courses (list): A list of courses taught by the instructor (optional).
    """
    name = fields.String(required=True, validate=validate.Length(min=1))
    age = fields.Integer(required=True, validate=lambda n: n > 0)
    email = fields.Email(required=True)
    instructor_id = fields.Integer(required=True)
    courses = fields.List(fields.String())  # Assuming you're passing course names or IDs

class CourseSchema(Schema):
    """
    Schema for validating course data.

    Fields:
        course_name (str): The name of the course (required).
        course_id (int): The unique identifier for the course (required).
        instructor_id (int): The ID of the instructor teaching the course (required).
    """
    course_name = fields.String(required=True, validate=validate.Length(min=1))
    course_id = fields.Integer(required=True)
    instructor_id = fields.Integer(required=True)

# Create schema instances
student_schema = StudentSchema()
instructor_schema = InstructorSchema()
course_schema = CourseSchema()
