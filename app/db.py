from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__) # We define the flask application on main

app.config['SECRET_KEY'] = 'c1155c6a351e49eba15c00ce577b259e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.db' # Declares the database path

db = SQLAlchemy(app) # Uses SQLAlchemy as ORM

socketio = SocketIO(app, async_mode="gevent", engineio_logger=False, cors_allowed_origins=['https://amplet.fr', 'http://amplet.fr', 'http://127.0.0.1:5000']) # Uses SocketIO as WS
