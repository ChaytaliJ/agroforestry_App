# from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
# import jwt
# import datetime
# import os
# from functools import wraps
# import mysql.connector
# from werkzeug.utils import secure_filename
# from config import DB_CONFIG, SECRET_KEY

# app = Flask(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.cookies.get('token')
#         if not token:
#             return redirect(url_for('login'))

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#             current_user = data['username']
#             role = data['role']
#         except jwt.ExpiredSignatureError:
#             return redirect(url_for('login'))
#         except jwt.InvalidTokenError:
#             return redirect(url_for('login'))

#         return f(current_user, role, *args, **kwargs)
#     return decorated

# @app.route('/')
# def index():
#     token = request.cookies.get('token')
#     is_logged_in = False

#     if token:
#         try:
#             jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#             is_logged_in = True
#         except jwt.ExpiredSignatureError:
#             pass
#         except jwt.InvalidTokenError:
#             pass

#     return render_template('index.html', is_logged_in=is_logged_in)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if user:
#             token = jwt.encode(
#                 {'username': user['username'], 'role': user['role'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
#                 app.config['SECRET_KEY'],
#                 algorithm="HS256"
#             )
#             response = redirect(url_for('submit'))
#             response.set_cookie('token', token)
#             return response

#         return render_template('login.html', error="Invalid username or password!")
#     return render_template('login.html')

# @app.route('/submit', methods=['GET', 'POST'])
# @token_required
# def submit(current_user, role):
#     if role != 'field_executive':
#         return redirect(url_for('index'))

#     if request.method == 'POST':
#         try:
#             # Fetch form data
#             name = request.form.get('farmerName')
#             contact = request.form.get('contactNumber')
#             plot_location = request.form.get('plotLocation')
#             field_photo = request.files.get('fieldPhoto')  # Get the uploaded file
#             tree_names = request.form.getlist('treeName[]')
#             tree_counts = request.form.getlist('treeCount[]')

#             if not name or not contact or not plot_location or not field_photo:
#                 return render_template('submit.html', username=current_user, success=False, error="Missing required fields!")

#             # Read image data
#             field_photo_blob = field_photo.read()

#             # Insert farmer data into the database
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('''INSERT INTO farmers (name, contact_number, plot_location, field_photo_blob, added_by) VALUES (%s, %s, %s, %s, %s)''', (name, contact, plot_location, field_photo_blob, current_user))
#             conn.commit()

#             # Insert tree species
#             farmer_id = cursor.lastrowid
#             for tree_name, count in zip(tree_names, tree_counts):
#                 cursor.execute('''INSERT INTO tree_species (farmer_id, species_name, quantity) VALUES (%s, %s, %s)''', (farmer_id, tree_name, count))
#             conn.commit()

#             cursor.close()
#             conn.close()

#             return render_template('submit.html', username=current_user, success=True)
#         except Exception as e:
#             print("Error:", str(e))  # Debugging
#             return "An error occurred: " + str(e), 400

#     return render_template('submit.html', username=current_user, success=False)

# @app.route('/dashboard', methods=['GET'])
# @token_required
# def dashboard(current_user, role):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         # Fetch farmer data only visible to the logged-in user (field executive A/B)
#         if role == 'field_executive':
#             cursor.execute("SELECT * FROM farmers WHERE added_by = %s", (current_user,))
#         # Field Manager C/D and Senior Manager E can see all data
#         else:
#             cursor.execute("SELECT * FROM farmers")

#         farmers = cursor.fetchall()

#         # Fetch tree species data
#         cursor.execute('''SELECT tree_species.*, farmers.name AS farmer_name FROM tree_species JOIN farmers ON tree_species.farmer_id = farmers.id''')
#         tree_species = cursor.fetchall()

#         cursor.close()
#         conn.close()

#         return render_template('dashboard.html', farmers=farmers, tree_species=tree_species)
#     except Exception as e:
#         print("Error fetching data:", e)
#         return "Error fetching data", 500

# @app.route('/image/<int:farmer_id>')
# def fetch_image(farmer_id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT field_photo_blob FROM farmers WHERE id = %s", (farmer_id,))
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result and result[0]:
#             return Response(result[0], mimetype='image/jpeg')  # Or other MIME type based on image format
#         else:
#             return "Image not found", 404
#     except Exception as e:
#         print("Error fetching image:", e)
#         return "Error fetching image", 500

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import jwt
import datetime
import os
from functools import wraps
import mysql.connector
from werkzeug.utils import secure_filename
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
            role = data['role']
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))

        return f(current_user, role, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    token = request.cookies.get('token')
    is_logged_in = False
    username = ""

    if token:
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            is_logged_in = True
            username = data['username']
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            pass

    return render_template('index.html', is_logged_in=is_logged_in, username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            token = jwt.encode(
                {'username': user['username'], 'role': user['role'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            response = redirect(url_for('submit'))
            response.set_cookie('token', token)
            return response

        return render_template('login.html', error="Invalid username or password!")
    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
@token_required
def submit(current_user, role):
    if role != 'field_executive':
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            # Fetch form data
            name = request.form.get('farmerName')
            contact = request.form.get('contactNumber')
            plot_location = request.form.get('plotLocation')
            field_photo = request.files.get('fieldPhoto')  # Get the uploaded file
            tree_names = request.form.getlist('treeName[]')
            tree_counts = request.form.getlist('treeCount[]')

            if not name or not contact or not plot_location or not field_photo:
                return render_template('submit.html', username=current_user, success=False, error="Missing required fields!")

            # Read image data
            field_photo_blob = field_photo.read()

            # Insert farmer data into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO farmers (name, contact_number, plot_location, field_photo_blob, added_by) VALUES (%s, %s, %s, %s, %s)''', (name, contact, plot_location, field_photo_blob, current_user))
            conn.commit()

            # Insert tree species
            farmer_id = cursor.lastrowid
            for tree_name, count in zip(tree_names, tree_counts):
                cursor.execute('''INSERT INTO tree_species (farmer_id, species_name, quantity) VALUES (%s, %s, %s)''', (farmer_id, tree_name, count))
            conn.commit()

            cursor.close()
            conn.close()

            return render_template('submit.html', username=current_user, success=True)
        except Exception as e:
            print("Error:", str(e))  # Debugging
            return "An error occurred: " + str(e), 400

    return render_template('submit.html', username=current_user, success=False)

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user, role):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch farmer data only visible to the logged-in user (field executive A/B)
        if role == 'field_executive':
            cursor.execute("SELECT * FROM farmers WHERE added_by = %s", (current_user,))
        elif role == 'field_manager' and current_user == 'manager_d':  # Replace 'manager_d' with the exact username for Manager D
            return render_template('dashboard.html', message="You are not allowed to view the data.")
        # Field Manager C/D and Senior Manager E can see all data
        else:
            cursor.execute("SELECT * FROM farmers")

        farmers = cursor.fetchall()

        # Fetch tree species data
        cursor.execute('''SELECT tree_species.*, farmers.name AS farmer_name FROM tree_species JOIN farmers ON tree_species.farmer_id = farmers.id''')
        tree_species = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('dashboard.html', farmers=farmers, tree_species=tree_species)
    except Exception as e:
        print("Error fetching data:", e)
        return "Error fetching data", 500
    
@app.route('/delete_farmers', methods=['POST'])
@token_required
def delete_farmers(current_user, role):
    if role != 'senior_manager_e':
        return redirect(url_for('index'))

    try:
        farmer_ids = request.form.getlist('farmer_id[]')
        conn = get_db_connection()
        cursor = conn.cursor()

        for farmer_id in farmer_ids:
            cursor.execute('''DELETE FROM farmers WHERE id = %s''', (farmer_id,))
            cursor.execute('''DELETE FROM tree_species WHERE farmer_id = %s''', (farmer_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))
    except Exception as e:
        print("Error deleting data:", e)
        return "Error deleting data", 500


@app.route('/logout')
def logout():
    response = redirect(url_for('index'))
    response.delete_cookie('token')  # Remove the token cookie
    return response

@app.route('/image/<int:farmer_id>')
def fetch_image(farmer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT field_photo_blob FROM farmers WHERE id = %s", (farmer_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and result[0]:
            return Response(result[0], mimetype='image/jpeg')  # Or other MIME type based on image format
        else:
            return "Image not found", 404
    except Exception as e:
        print("Error fetching image:", e)
        return "Error fetching image", 500

if __name__ == '__main__':
    app.run(debug=True)
