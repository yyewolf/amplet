from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask import render_template
from flask import url_for

# Setup ####################################
setup = False
if not os.path.isfile("data/db.db"):
    os.open("data/db.db", os.O_CREAT)
    setup = True
############################################

from db import *
from models import *
        
db.create_all() # Creates the tables if necessary

# Setup ####################################
if setup:
    admin = users.User(username='admin', email='admin@test.com')
    guest = users.User(username='guest', email='guest@test.com')
    admin.set_password('oof')
    guest.set_password('oof')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
############################################

@app.route("/admin")
def hello_world():
    content = "<p>Hello, World ! Here are my users : </p>"
    content += "<br/>"
    for user in users.User.query.all():
        content += f"{user.id} - {user.username} & {user.email}"
        content += "<br/>"
    return content

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register",methods=['POST'])
def createaccount():    
    username = request.form['username']
    motdepasse = request.form['register']
    mail = request.form['emailAddress']
    return f"{mail},{username},{motdepasse}"
    


if __name__=="__main__":
    app.run(debug=True)