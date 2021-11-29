from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from py.models import users
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():

  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    found_user = users.query.filter_by(username = username).first()

    if found_user:
      if found_user.password == password:
        login_user(found_user, remember = True)
        return redirect(url_for('views.empty_cart'))
      else: flash('Wrong password.', category='bad')
    else: flash('Wrong username.', category='bad')

  return render_template('login.html', user = current_user)

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("auth.login"))
