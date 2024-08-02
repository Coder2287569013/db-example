import sqlite3

db = sqlite3.connect("univer.db")
db.execute('''
CREATE TABLE IF NOT EXISTS students(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(255),
           age INTEGER,
           major VARCHAR(255)
);
''')
db.execute('''
CREATE TABLE IF NOT EXISTS courses(
           course_id INTEGER PRIMARY KEY AUTOINCREMENT,
           course_name VARCHAR(255),
           instructor VARCHAR(255)
);
''')
db.execute('''
CREATE TABLE IF NOT EXISTS student_course(
           student_id INTEGER REFERENCES students(id),
           course_id INTEGER REFERENCES courses(course_id),
           PRIMARY KEY (student_id, course_id)
);
''')

def add_student():
    name = input("Name: ")
    age = int(input("Age: "))
    major = input("Major: ")
    db.execute('''INSERT INTO students(name, age, major) VALUES (?, ?, ?);''', 
               (name, age, major))
    db.commit()

def add_course():
    course_name = input("Course name: ")
    instructor = input("Instructor: ")
    db.execute('''INSERT INTO courses(course_name, instructor) VALUES (?, ?);''', 
               (course_name, instructor))
    db.commit()

def show_students():
    db_students = db.execute('''SELECT * FROM students;''')
    for student in db_students:
        print(student)

def show_courses():
    db_courses = db.execute('''SELECT * FROM courses;''')
    for course in db_courses:
        print(course)

def register_student():
    student_id = int(input("Student: "))
    course_id = int(input("Course: "))

    student_check = db.execute('''SELECT 1 FROM students WHERE id = ?;''', (student_id, )).fetchone()
    course_check = db.execute('''SELECT 1 FROM courses WHERE course_id = ?;''', (course_id, )).fetchone()

    if not student_check and course_check:
        raise ValueError(f"Student or course doesn't exist")
    else:
        db.execute('''
            INSERT INTO student_course(student_id, course_id) VALUES (?, ?);
        ''', (student_id, course_id))
        db.commit()

def show_student_course():
    course_id = int(input("Course: "))
    info = db.execute('''SELECT name, age 
                      FROM students 
                      JOIN student_course ON student_course.student_id == students.id 
                      WHERE student_course.course_id == ?''', (course_id, ))
    for i in info:
        print(i)
        
def update_student_info():
    id = int(input("Student id: "))
    name = input("Name: ")
    age = int(input("Age: "))
    major = input("Major: ")
    db.execute('''
        UPDATE students SET name = ?, age = ?, major = ? WHERE id = ?;
    ''', (name, age, major, id))
    db.commit()

while True:
    print("\n1. Add a new student")
    print("2. Add a new course")
    print("3. Show the list of students")
    print("4. Show the list of courses")
    print("5. Register a student for a course")
    print("6. Show the list of students enrolled in a specific course")
    print("7. Update the information about a student")
    print("8. Close")

    choice = input("Choose an option (1-8): ")

    match choice:
        case "1":
            add_student()
        case "2":
            add_course()
        case "3":
            show_students()
        case "4":
            show_courses()
        case "5":
            register_student()
        case "6":
            show_student_course()
        case "7":
            update_student_info()
        case "8":
            break
