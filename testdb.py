from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# RDS database credentials
host = 'mydb.c70qoekoig83.ap-south-1.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'admin123'
database = 'rdsdb'

# Function to establish database connection
def connect_to_database():
    return pymysql.connect(host=host, port=port, user=user, password=password, database=database)

# Create student table if it doesn't exist
def create_student_table():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS student (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT, gender VARCHAR(10), email VARCHAR(255))")
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error creating student table: {e}")

# Check if student table exists, if not create it
create_student_table()

# Home page - List all students
@app.route('/')
def home():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()
        connection.close()
        return render_template('index.html', students=students)
    except Exception as e:
        return f"Error: {e}"

# Add new student page
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO student (name, age, gender, email) VALUES (%s, %s, %s, %s)", (name, age, gender, email))
            connection.commit()
            connection.close()
            return redirect(url_for('home'))
        except Exception as e:
            return f"Error adding student: {e}"
    return render_template('add.html')

# Edit student page
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("UPDATE student SET name=%s, age=%s, gender=%s, email=%s WHERE id=%s", (name, age, gender, email, id))
            connection.commit()
            connection.close()
            return redirect(url_for('home'))
        except Exception as e:
            return f"Error editing student: {e}"
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id=%s", (id,))
        student = cursor.fetchone()
        connection.close()
        return render_template('edit.html', student=student)
    except Exception as e:
        return f"Error fetching student: {e}"

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM student WHERE id=%s", (id,))
        connection.commit()
        connection.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error deleting student: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
