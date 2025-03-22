from flask import Flask, request, jsonify, render_template, make_response
# from flask_cors import CORS
import mysql.connector
import os
import asyncio
from model import main_fun
from verify import verify
import cv2
import numpy as np
from modeladd import main_fun2
import time
from gender import verify_gender
# from flask_session import Session
# import uuid

app = Flask(__name__)
# CORS(app, origins='*')  # Allowing requests from all origins


app = Flask(__name__, static_url_path='/static')

totalTime = 0

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="c"
)


cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Persons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        nicknames VARCHAR(255),
        idMark VARCHAR(255),
        dob VARCHAR(10),
        birthplace VARCHAR(255),
        suspect INT DEFAULT 0,
        explanation TEXT
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    department VARCHAR(255),
    post VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20)
)
""")



@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.form
    name = data['name']
    nicknames = data.get('nicknames', None)
    idMark = data.get('idMark', None)
    dob = data.get('dob', None)
    birthplace = data.get('birthplace', None)
    suspect = data.get('suspect', 0)
    explanation = data.get('explanation', None)

    sql = """
        INSERT INTO Persons (name, nicknames, idMark, dob, birthplace, suspect, explanation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (name, nicknames, idMark, dob, birthplace, suspect, explanation)
    cursor.execute(sql, values)
    db.commit()

    file = request.files['image']
    filename = str(cursor.lastrowid) + os.path.splitext(file.filename)[1]
    file.save(os.path.join('static/uploads', filename))

    response = jsonify({"message": "Person added successfully"})

    return response, 201


@app.route('/clear_image', methods=['POST'])
def clear_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    try:
        image_file = request.files['image']
        asyncio.run(main_fun(image_file))
        return jsonify({"totalLastOperation": totalTime, "imageName": asyncio.run(verify("./results/res/input.jpg"))})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/verify_image', methods=['POST'])
def verify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    try:
        image_file = request.files['image']
        nparr = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_path = "static/data/input.jpg"
        cv2.imwrite(img_path, image)
        return jsonify({"imageName": asyncio.run(verify(img_path))})
    
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/clear_add', methods=['POST'])
def clearadd_image():
    data = request.form
    name = data['name']
    nicknames = data.get('nicknames', None)
    idMark = data.get('idMark', None)
    dob = data.get('dob', None)
    birthplace = data.get('birthplace', None)
    suspect = data.get('suspect', 0)
    explanation = data.get('explanation', None)

    sql = """
        INSERT INTO Persons (name, nicknames, idMark, dob, birthplace, suspect, explanation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (name, nicknames, idMark, dob, birthplace, suspect, explanation)
    cursor.execute(sql, values)
    db.commit()

    file = request.files['file']
    asyncio.run(main_fun2(file, os.path.join("./static/uploads/", str(cursor.lastrowid) + ".jpg")))
    response = jsonify({"message": "Person added successfully"})
    return response, 201


@app.route('/clear_image_only', methods=['POST'])
def clear_image_only():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    try:
        image_file = request.files['image']
        asyncio.run(main_fun(image_file))
        return jsonify({"blurRemoved": "true", "gender": asyncio.run(verify_gender())})
    
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/')
def index():
    username = request.cookies.get('username')
    print(username)
    cursor.execute("SELECT COUNT(*) AS total_records FROM Persons")
    result = cursor.fetchone()
    total_records = result[0]
    return render_template('index.html', records=int(total_records))


@app.route('/match/<num>')
def match(num):
    print(num)
    id=int(os.path.splitext(num)[0])
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Persons WHERE id = %s", (id,))
    person = cursor.fetchone()
    cursor.close()
    img_name = "uploads/"+str(num)
    return render_template('match.html', data = person, iname=img_name, match="Matched")


@app.route('/edit_record', methods=['POST'])
def edit_records():
    try:
        data = request.json
        id = int(data['id'])
        name = data['name']
        nicknames = data['nicknames']
        idMark = data['idMark']
        dob = data['dob']
        birthplace = data['birthplace']
        suspect = data['suspect']
        explanation = data['explaination']

        print(data)

        update_query = "UPDATE Persons SET name = %s, nicknames = %s, idMark = %s, dob = %s, birthplace = %s, suspect = %s, explanation = %s WHERE id = %s"
        cursor.execute(update_query, (name, nicknames, idMark, dob, birthplace, suspect, explanation, id))
        db.commit()
        response = jsonify({"message": "Record updated successfully"})
        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/confirm_delete/<num>')
def confirm_delete(num):
    return render_template('confirmDelete.html', deleteID=num)


@app.route('/search/<query>', methods=['GET'])
def search_records(query):
        search_query = "SELECT * FROM Persons WHERE name LIKE %s"
        cursor.execute(search_query, ('%' + query + '%',))

        records = cursor.fetchall()

        results = []
        for record in records:
            result = {
                'id': record[0],
                'name': record[1],
                'nicknames': record[2],
                'idMark': record[3],
                'dob': record[4],
                'birthplace': record[5],
                'suspect': record[6],
                'explanation': record[7]
            }
            results.append(result)

        return render_template('searchq.html', persons=results)


@app.route('/delete_record', methods=['DELETE'])
def delete_record():
    try:
        data = request.get_json(force=True)
        if data:

            id = data['id']

            delete_query = "DELETE FROM Persons WHERE id = %s"
            cursor.execute(delete_query, (id,))
            db.commit()

            file_path = os.path.join("./static/uploads/", id, ".jpg")
            file_path2 = os.path.join("./static/uploads/", id, ".jpeg")

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' deleted successfully.")
            elif os.path.exists(file_path2):
                os.remove(file_path2)
                print(f"File '{file_path}' deleted successfully.")
            else:
                print(f"File '{file_path}' does not exist.")

            return jsonify({'message': 'Record deleted successfully'})
        else:
            return jsonify({'error': 'No data received'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/editr/<num>')
def editr(num):
    id=int(num)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Persons WHERE id = %s", (id,))
    person = cursor.fetchone()
    cursor.close()
    return render_template('editr.html', person = person)


@app.route('/clearonly/<gender>')
def clearonly(gender):
    gender = int(gender)
    gGender = "Female" if gender == 1 else ("Male" if gender==0 else "Not detected")
    return render_template('clearonly.html', gender=gGender)



@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/search')
def search():
    cursor.execute("SELECT id, name, explanation FROM Persons")
    persons = cursor.fetchall()
    return render_template('search.html', persons=persons)

@app.route('/edit')
def edit():
    cursor.execute("SELECT id, name, explanation FROM Persons")
    persons = cursor.fetchall()
    return render_template('edit.html', persons=persons)

@app.route('/clear')
def clear():
    return render_template('clear.html')

@app.route('/clearadd')
def clearadd():
    return render_template('clearadd.html')

@app.route('/delete')
def delete():
    cursor.execute("SELECT id, name, explanation FROM Persons")
    persons = cursor.fetchall()
    return render_template('delete.html', persons=persons)

@app.route('/admin/settings')
def admin_settings():
    return render_template('admin_settings.html')

@app.route('/admin/users')
def admin_users():
    cursor.execute("SELECT name, email FROM user")
    person = cursor.fetchall()
    return render_template('admin_users.html', persons=person)

@app.route('/admin/about')

def admin_contact():
    return render_template('admin_about.html')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        if data:
            name = data.get('name')
            department = data.get('department')
            post = data.get('post')
            email = data.get('email')
            password = data.get('password')
            phone_number = data.get('phone_number')

            if not (name and email and password):
                return jsonify({'error': 'Name, email, and password are required'}), 400

            insert_query = "INSERT INTO user (name, department, post, email, password, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (name, department, post, email, password, phone_number))
            db.commit()

            return jsonify({'message': 'User signed up successfully'})
        else:
            return jsonify({'error': 'No data received'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
        data = request.json
        if data:
            email = data.get('email')
            password = data.get('password')

            cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            print(user)
            if user:
                username = request.cookies.get('username')
                print(username)
                print(user[0])
                return jsonify({'message': user[4]})
            else:
                return jsonify({'error': 'Invalid email or password'}), 401
        else:
            return jsonify({'error': 'No data received'}), 400

@app.route('/home')
def home():
    return render_template('home/index.html')

@app.route("/fromvideo", methods=['POST'])
def fromVideo():
    print(request.files['image'])
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    try:
        image_file = request.files['image']
        asyncio.run(main_fun(image_file))
        return jsonify({"blurRemoved": "true", "gender": asyncio.run(verify_gender())})
    
    except Exception as e:
        return jsonify({'error': str(e)})
    


@app.route("/fromvid")
def fromVid():
    return render_template("fromv.html")

if __name__ == '__main__':
    app.run(debug=True)
