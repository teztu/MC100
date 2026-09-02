from flask import Flask, jsonify, request, g
from werkzeug.utils import secure_filename
from pathlib import Path
from flask_httpauth import HTTPBasicAuth
import hashlib
import sqlite3
import uuid


app = Flask(__name__)
auth = HTTPBasicAuth()


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} #Better than blacklisting, because it is hard to list all of them
DATABASE = 'user_database.db' #Connect to an SQLite database (creates the database if it doesn't exist)


app.config["UPLOAD_FOLDER"] = Path(app.root_path) / "uploads"#Creates folder in root called "uploads"
app.config["UPLOAD_FOLDER"].mkdir(exist_ok=True)#Checks if folder exists


# Hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
#SQLite database setup
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    #database for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            token TEXT
        )
    ''')
    #database for files
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            filename TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
# Create a new user
def create_user(username, password):
    hashed_password = hash_password(password)
    token = str(uuid.uuid4())
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, token) VALUES (?, ?, ?)', (username, hashed_password, token))
    conn.commit()
    conn.close()

# Authenticate a user
@auth.verify_password
def verify_password(username, password): #authenticator
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user[2] == hash_password(password):
        g.user = user
        return True
    return False

# API route to get user information
@app.route('/api/userinfo')
@auth.login_required
def get_user_info():
    user = g.user
    return jsonify({'id': user[0], 'username': user[1]})

# API route for user registration
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if data and 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']
        create_user(username, password)
        return jsonify({"message": "User registered successfully"}), 201
    return jsonify({"message": "Invalid data"}), 400

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API route to upload a file
@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files: #Checks that file was included

        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '': #Empty
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):#Validates

        filename = secure_filename(file.filename)

        if not filename:
            return jsonify({"message": "Invalid filename"}), 400


        file_path = app.config["UPLOAD_FOLDER"] / filename
        file.save(file_path)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO files (owner_id, filename) VALUES (?, ?)',(g.user[0], filename) )
        conn.commit()
        conn.close()

        return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
    else:
        return jsonify({"message": "Invalid file type"}), 400

@app.route('/api/files/<int:file_id>', methods=['GET'])
@auth.login_required
def get_file(file_id): #authorization

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, owner_id, filename FROM files WHERE id=?',
        (file_id,)
    ) #tuple with id, owner_id and filename

    stored_file = cursor.fetchone()
    conn.close()

    if stored_file is None:
        return jsonify({"message": "File not found"}), 404

    #AUTHORIZATION
    if stored_file[1] != g.user[0]: #check if owner_id from the SELECT query matches owner_id from g.user
        return jsonify({"message": "Not authorized"}), 403

    return jsonify({
        "id": stored_file[0],
        "filename": stored_file[2]
    }), 200


if __name__ == '__main__':
    app.run(debug=True)