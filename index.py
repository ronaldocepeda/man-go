from flask import Flask, render_template, session 
from flask import request, redirect, url_for


from flask_mysqldb import MySQL

from flask_wtf import CsrfProtect
from flask import make_response
from flask import flash
import time 
import json

from configs import DevelomentConfig

import yaml
import forms

from werkzeug.security import generate_password_hash, check_password_hash

# import bcrypt


app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CsrfProtect()

# config db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
# semilla = bcrypt.gensalt()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/')
def Welcome():
    return render_template ('ManGO.html', titulo = "Welcome To ManGO!")

@app.route('/home')
def Home():
    return render_template ('home.html', titulo = "MenGO! Home")

@app.route('/services')
def services():
    return render_template ('services.html', titulo = "Servicios")

@app.route('/about')
def about():
    return render_template ('about.html', titulo = "Nosostros")



@app.route('/register' ,methods = ['POST', 'GET'])
def register():
    login_form = forms.LoginForm(request.form)
    if request.method == 'GET':
        if 'username' in session:
            flash('ya estas registrado')
            return redirect('/singup')
        else:
           titulo = "Inicio sesión"
           return render_template ('registerGO.html', titulo = titulo, form = login_form) 

    else:
        username = login_form.username.data
        apellido = login_form.apellido.data
        usuario  = login_form.usuario.data
        email    = login_form.email.data
        password = login_form.password.data
        hashed_value = generate_password_hash(password)
        stored_password = hashed_value
        # password_encode = password.encode("utf-8")
        # password_encriptado = bcrypt.hashpw(password_encode, semilla)
        cur = mysql.connection.cursor()
        sQuery = "INSERT INTO registro(username, apellido, usuario, email, password) VALUES(%s, %s, %s, %s, %s)"
        cur.execute(sQuery,(username,apellido,usuario,email,hashed_value))
        mysql.connection.commit()
        session['username'] = login_form.username.data
        session['usuario']  = login_form.usuario.data
        session['email']    = login_form.email.data

        flash('te has registrado corretamente')
        return redirect('/singup')


    titulo = "Registrate GO!"
    return render_template ('registerGO.html', titulo = titulo, form = login_form)


@app.route('/login',methods = ['POST', 'GET'])
def login():
    
    
    login_form = forms.LoginForm(request.form)
    error = None

    if request.method == 'GET':
        if 'username' in session:
            flash('ya estas en inicio')
            return redirect('/singup')
    else:
        username   = login_form.username.data
        email      = login_form.email.data
        password   = login_form.password.data
        # password_encode = password.encode("utf-8")
        
        # session['username'] = login_form.username.data

        cur = mysql.connection.cursor()

        sQuery = "SELECT username, apellido, usuario, email, password FROM registro WHERE email = %s"

        cur.execute(sQuery,[email])

        usuario = cur.fetchone()

        cur.close()

        if (usuario !=None):
            password_password = usuario[4]
            print("password     :", password)
            print("Password_password :",password_password)
            if check_password_hash(password_password, password):

                session['username'] = usuario

                flash('has iniciado en el sitio web')
                return redirect(url_for('singup'))
            else:
                error ='contraseña incorrecta'
        else:
            error = 'en usuario y password. por favor intente de nuevo!'
    titulo = "Inicio sesión"
    return render_template ('loginGO.html', titulo = titulo, form = login_form, error = error)


@app.route('/singup')
def singup():

    if 'username' in session:

        username = session['username']
    else:
        return redirect(url_for('login'))

    titulo = "Inicio GO!"
    return render_template ('singup.html', titulo = titulo)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))




@app.route('/cookie')
def cookie():
    response = make_response( render_template ('cookie.html') )
    response.set_cookie('custome_cookie', 'mango')
    return response


# @app.route('/ajax-login', methods= ['POST'])
# def ajax_login():
#  print (request.form)
#  username = request.form['username']
#  response = { 'status': 200, 'username': username, 'id': 1 }
#  return json.dumps(response)



if __name__ =='__main__':
    csrf.init_app(app)
    

app.run(port=8000)










