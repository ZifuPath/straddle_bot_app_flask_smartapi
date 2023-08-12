from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
DB_NAME = "tokens.db"
from turbo_flask import Turbo

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Database! Created')


app = Flask(__name__)
turbo = Turbo(app)

app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=False
db = SQLAlchemy(app)
create_database(app)