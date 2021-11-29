from flask_sqlalchemy.model import Model
from py.init import db
from flask_login import UserMixin

class users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(20))
  password = db.Column(db.String(20))
  admin_status = db.Column(db.Boolean)

  def __init__(self, username, password, admin_status):
    self.username = username
    self.password = password
    self.admin_status = admin_status

class books(db.Model):
  name_of_book = db.Column(db.String(30))
  name_of_author = db.Column(db.String(30))
  isbn13 = db.Column(db.Integer, primary_key = True)
  book_description = db.Column(db.String(300))
  publication_date = db.Column(db.String(10))
  photo_path = db.Column(db.String(100))
  trade_price = db.Column(db.Integer)
  retail_price = db.Column(db.Integer)
  quantity = db.Column(db.Integer)
 
  def __init__(self, name_of_book, name_of_author, isbn13, book_description, publication_date, photo_path, trade_price, retail_price, quantity):
    self.name_of_book =  name_of_book
    self.name_of_author = name_of_author
    self.isbn13 = isbn13
    self.book_description = book_description
    self.publication_date = publication_date
    self.photo_path = photo_path
    self.trade_price = trade_price
    self.retail_price = retail_price
    self.quantity = quantity