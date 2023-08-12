from config import db
import datetime


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column('id', db.Integer(), primary_key=True)
    symbol = db.Column('symbol', db.String(100))
    tokens = db.Column('tokens', db.Integer())
    expiry= db.Column('expiry' , db.String(100))