import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
connection = sqlite3.connect("student.db")

# Create a cursor object
cursor = connection.cursor()

# Table creation
table_info = """
CREATE TABLE IF NOT EXISTS student(
    name VARCHAR(20), 
    class VARCHAR(20), 
    section VARCHAR(25), 
    marks INT
)
"""
cursor.execute(table_info)

# Data to insert (as list of tuples)
students_data = [
    ('John', 'Data Science', 'B', 100),
    ('Mukesh', 'Data Science', 'A', 90),
    ('Jacob', 'DEVOPS', 'B', 80),
    ('Dipesh', 'Big Data', 'B', 75),
    ('Raj', 'MLE', 'A', 55),
    ('Alice', 'Cyber Security', 'A', 85),
    ('Bob', 'Software Engineering', 'C', 70),
    ('Charlie', 'AI & ML', 'B', 95),
    ('David', 'Cloud Computing', 'A', 88),
    ('Eve', 'Computer Networks', 'B', 78),
    ('Frank', 'Data Science', 'C', 65),
    ('Grace', 'Big Data', 'A', 92),
    ('Hannah', 'AI & ML', 'B', 89),
    ('Ian', 'Software Engineering', 'C', 73),
    ('Jack', 'Cloud Computing', 'B', 81),
    ('Karen', 'Cyber Security', 'A', 90),
    ('Leo', 'Computer Networks', 'C', 60),
    ('Mia', 'Big Data', 'B', 85),
    ('Nathan', 'DEVOPS', 'A', 79),
    ('Olivia', 'MLE', 'B', 76),
    ('Peter', 'Data Science', 'A', 94)
]

# Insert multiple records using executemany
cursor.executemany("INSERT INTO student (name, class, section, marks) VALUES (?, ?, ?, ?)", students_data)

print("Data inserted successfully.")

# Fetch & display records
print("Fetching data from student table:")
data = cursor.execute("SELECT * FROM student")
for row in data:
    print(row)

# Commit changes
connection.commit()

# Close connection
connection.close()
