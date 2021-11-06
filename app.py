from flask import Flask, render_template, request, redirect, session
from flask.helpers import url_for
import pymongo
from random import seed
from random import randint
from pymongo import MongoClient, cursor
from dotenv import load_dotenv
import datetime
import os

app = Flask(__name__)

app.permanent_session_lifetime = datetime.timedelta(days=1)
app.secret_key = os.environ.get("secret_key");

client = pymongo.MongoClient(
    "mongodb+srv://rraya:rubenraya@cluster0.w9ojs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client.Escuela
usuarios = db.alumno

@app.route('/')
def index():
    email=""
    if "email" in session:
        email = session["email"]
        return render_template('/index.html', message=email)
    else:
        return render_template('/LoginFull.html')
    

@app.route('/login', methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    session["email"] = email
    session["password"] = password

    return render_template('/index.html')

@app.route('/register', methods=["POST"])
def register():
    seed(1)
    valor = randint(2, 99999)
    _cursor = 0
    _cursor = usuarios.find_one({"matricula": valor})
    print(_cursor)
    if _cursor is None:
        matricula = valor
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        _user = {"matricula": matricula,
                 "nombre": name,
                 "correo": email,
                 "contrasena": password}
        try:
            usuarios.insert_one(_user)
            return render_template("/LoginFull.html")
        except Exception as e:
            return "%s" % e
    else:
        return redirect(url_for("find_users"))



@app.route('/logout')
def logout():
    session.clear()
    return render_template("/LoginFull.html")

@app.route('/find_users', methods=['GET'])
def find_users():
    _cursor = usuarios.find()
    user = []
    for doc in _cursor:
        user.append(doc)
    return render_template("/Retrieve.html", data=user)

@app.route('/update', methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]}
        query = {"$set": {
            "nombre": request.form['nombre'],
            "correo": request.form['correo'],
            "contrasena": request.form['contrasena']}}
        usuarios.update_one(filter, query)
        return redirect(url_for("find_users"))
    except Exception as e:
        return 'Hay un error: %s' % e

    return ""
    

@app.route('/create_form', methods=["GET", "POST"])
def create_form():
    if request.method == "POST":
        _user = { 
            "matricula": request.form["matricula"],
            "nombre": request.form['nombre'],
            "correo": request.form['correo'],
            "contrasena": request.form['contrasena']
        }
        try:
            usuarios.insert_one(_user)
            return redirect(url_for("find_users"))
        except Exception as e:
            return 'Hay un error: %s' % e
    else:
        return render_template("/CreateForm.html")

@app.route('/delete/<matricula>', methods=["GET"])
def delete(matricula):
    try:
        _cursor = usuarios.delete_one({"matricula": matricula})
        if _cursor.deleted_count == 0:
            return 'La matricula %s no existe en DB' % matricula
    except Exception as e:
        return 'Hay un error: %s' % e
    return redirect(url_for("find_users"))


    



    
if __name__ == '__main__':
    app.run(debug=True)

