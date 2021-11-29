from typing import ItemsView
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from py.init import db, upload_folder
from .models import users, books
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/home')
@views.route('/')
@login_required
def home():

  allbooks = books.query.all()

  return render_template('home.html', user = current_user, books = allbooks)

@views.route('/cart')
@login_required
def cart():

  incart = []
  index = 0
  total = 0

  if 'cart' in session:
    for item in session['cart']:
      current_book = books.query.filter_by(isbn13 = item['isbn13']).first()

      quantity = item['quantity']
      item_total = current_book.retail_price * quantity
      total += item_total
      index += 1

      incart.append({'name' : current_book.name_of_book, 'photo' : current_book.photo_path, 'price' : current_book.retail_price, 'quantity' : quantity, 'item_total' : item_total, 'index' : index})

  print(incart)

  return render_template('cart.html', user = current_user, cart = incart, total = total)

@views.route('/addtocart/<isbn13>')
@login_required
def addtocart(isbn13):

  if 'cart' not in session:
    session['cart'] = []

  verify = False
  exd = False
  global items_incart
  items_incart = 0

  for item in session['cart']:
    if item['isbn13'] == isbn13:
      verify = True

  if verify == False:
    session['cart'].append({'isbn13' : isbn13, 'quantity' : 1})
  else:

    found_book = books.query.filter_by(isbn13 = isbn13).first()

    for item in session['cart']:
      if item['isbn13'] == isbn13:
        if item['quantity'] < found_book.quantity:
          item['quantity'] += 1
        else: exd = True

  if exd == True:
    flash('Not enough stock.', category='bad')

  for item in session['cart']:
    items_incart += item['quantity']

  print(items_incart)

  return redirect(url_for('views.home'))

@views.route('/delete_from_cart/<index>')
@login_required
def delete_from_cart(index):

  del session['cart'][int(index) - 1]

  return redirect(url_for('views.cart'))

@views.route('/empty_cart')
@login_required
def empty_cart():

  session.clear()

  return redirect(url_for('views.home'))


@views.route('/stock_levels')
@login_required
def stock_levels():

  if current_user.admin_status == True:
    allbooks = books.query.all()
    return render_template('stock_levels.html', user = current_user, books = allbooks)
  else:
    flash('You need to be an admin to access this page.', category='bad')
    return redirect(url_for('views.home'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('add_stock', methods = ['GET', 'POST'])
@login_required
def add_stock():

  if current_user.admin_status == True:

    if request.method == 'POST':

      name_of_book = request.form.get('name_of_book')
      name_of_author = request.form.get('name_of_author')
      isbn13 = request.form.get('isbn13')
      book_description = request.form.get('book_description')
      publication_date = request.form.get('date')
      trade_price = request.form.get('trade_price')
      retail_price = request.form.get('retail_price')
      quantity = request.form.get('quantity')
      file = request.files['file']

      global html_photo_name
      html_photo_name = file.filename

      html_photo_name = html_photo_name.replace(' ', '_')

      photo_path = '../static/uploads/' + html_photo_name

      found_book = books.query.filter_by(isbn13 = isbn13).first()

      if name_of_book == '':
        flash('You forgot the name of the book.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif name_of_author == '':
        flash('You forgot the name of author.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif isbn13 == '':
        flash('You forgot the ISBN13 number.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif book_description == '':
        flash('You forgot the book description.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif publication_date == '':
        flash('You forgot the publication date.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif trade_price == '0':
        flash('You forgot to select the trade price.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif retail_price == '0':
        flash('You forgot to select the retail price.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif quantity == '0':
        flash('You forgot to select the quantity.', category='bad')
        return redirect(url_for("views.add_stock"))
      elif found_book:
        found_book.quantity = str(int(found_book.quantity) + int(quantity))
        db.session.commit()
        flash('Book added to stock.', category='good')
      else:

        book = books(name_of_book, name_of_author, isbn13, book_description, publication_date, photo_path, trade_price, retail_price, quantity)
        db.session.add(book)
        db.session.commit()

        if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(upload_folder, filename))

        flash('Book added to stock.', category='good')

    return render_template('add_stock.html', user = current_user)
  else:
    flash('You need to be an admin to access this page.', category='bad')
    return redirect(url_for('views.home'))

@views.route("/delete/<string:book_name>")
def delete(book_name):
  books.query.filter_by(name_of_book = book_name).delete()
  db.session.commit()
  return f'{book_name} was deleted'

@views.route("/au")
def au():
  u1 = users('customer1', 'p455w0rd', False)
  u2 = users('customer2', 'p455w0rd', False)
  a1 = users('admin', 'p455w0rd', True)
  db.session.add(u1), db.session.add(u2), db.session.add(a1)
  db.session.commit()

