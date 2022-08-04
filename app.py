from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
from time import sleep

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


import subprocess
import sys

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.exc import NoResultFound

import random

subprocess.Popen(["python.exe", "D:/python projects/stealled site/app_copy.py"])


app = Flask('stealled site')
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

class Comments(db.Model):
    
    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    name_href = db.Column(db.Text, nullable=False)
    text_post = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Comments %r>' % self.number

class Article(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(15), nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Article %r>' % self.number
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(17), nullable=False, unique = True)
    password = db.Column(db.String(64), nullable=False)

    promocode50 = db.Column(db.Text, unique = True)
    promocode100 = db.Column(db.Text, unique = True)
    promocode_all = db.Column(db.Integer)
    promocode_date = db.Column(db.DateTime, default=datetime.now())

    
    def __repr__(self):
        return '<User %r>' % self.id

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.id == 1 #or else

admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Article, db.session))

def dating(Article):

    hr = datetime.now()
    meme = Article.date.date()

    popo = hr - meme

    return(popo)


@app.route("/")
def main():
    now = datetime.now()
    articles = Article.query.order_by(Article.number.desc())

    logged = current_user

    def time_checker(article):
        return article.date > datetime.now() + timedelta(hours=-24)
    
    return render_template('index.html', articles=articles, time_checker=time_checker, logged=logged)

@app.route("/comments")
def contacts():
    comments = Comments.query.order_by(Comments.number.desc()).all()
    
    return render_template('comments.html', comments=comments)

@app.route("/make_post", methods=['POST', 'GET'])
@login_required
def dbase():
    if current_user.id == 1:
        if request.method == 'POST':
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']
            tag = request.form['tag']
            img_url = request.form['img_url']

            if title == "" or intro == "" or text == "" or tag == "" or img_url == "":
                return "Не все поля заполнены! Вернись на предыдущую страничку."
            article = Article(title=title, intro=intro, text=text, tag=tag, img_url=img_url)

            try:
                db.session.add(article)
                db.session.commit()
                return redirect('/posts')
            except:
                return "!Eroor!"
        else:
            return render_template('make_post.html')
    else:
        return redirect("/")

@app.route("/posts")
def posts():
    now = datetime.now()
    articles = Article.query.order_by(Article.number.desc()).all()

    def time_checker(article):
        return article.date > datetime.now() + timedelta(hours=-24)


    return render_template('posts.html', articles=articles, time_checker=time_checker)

@app.route("/posts/<int:number>")
def def_post(number):

    article = Article.query.get(number)
    return render_template('def_post.html', article=article)

@app.route("/posts/<int:number>/delete")
@login_required
def def_post_delete(number):
    if current_user.id == 1:
        article = Article.query.get_or_404(number)

        try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return '!ERrOr!'
    else:
        return redirect("/")

@app.route("/posts/<int:number>/edit", methods=['POST', 'GET'])
@login_required
def def_post_edit(number):
    if current_user.id == 1:
        article = Article.query.get_or_404(number)
        if request.method == "POST":
            article.title = request.form['title']
            article.intro = request.form['intro']
            article.text = request.form['text']
            article.tag = request.form['tag']
            article.img_url = request.form['img_url']

            try:
                db.session.commit()
                return redirect('/posts')
            except:
                return "!Eroor!"
        else:
            return render_template('edit_post.html', article=article)
    else:
        return redirect("/")

@app.route("/game", methods=['POST', 'GET'])
@login_required
def game():

    if current_user.promocode50 == None or current_user.promocode100 == None or current_user.promocode_date < datetime.now() + timedelta(hours=0):
        code50 = '50'
        for x in range(12):
            code50 = code50 + random.choice(list('23456789qwertyuipasdfghjklzxcvbnmQWERTYUIPASDFGHJKLZXCVBNM'))
        code100 = '100'
        for x in range(12):
            code100 = code100 + random.choice(list('23456789qwertyuipasdfghjklzxcvbnmQWERTYUIPASDFGHJKLZXCVBNM'))


        if request.method == "POST":
            if request.form['rock-paper-scissors'].startswith("0"):
                current_user.promocode50 = "нет"
                current_user.promocode100 = "нет"
                current_user.promocode_all += 1
                current_user.promocode_date = datetime.now()
            elif request.form['rock-paper-scissors'].startswith("100"):
                current_user.promocode50 = "нет"
                current_user.promocode100 = request.form['rock-paper-scissors']
                current_user.promocode_all += 1
                current_user.promocode_date = datetime.now()
            elif request.form['rock-paper-scissors'].startswith("50"):
                current_user.promocode50 = request.form['rock-paper-scissors']
                current_user.promocode100 = "нет"
                current_user.promocode_all += 1
                current_user.promocode_date = datetime.now()

            try:
                db.session.commit()
                return redirect('/account')
            except:
                return "!Eroor!"
        else:
            pass
    else:
        return render_template("game_return.html")

    return render_template('game.html', code50=code50, code100=code100)

@app.route("/board")
def board():
    
    users = User.query.order_by(User.promocode_all.desc()).limit(10).all()
    return render_template('board.html', users=users)

#регистрация
@manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    #если уже залогинен:
    if current_user.is_authenticated:
	    return redirect(url_for('account'))
    
    #ожидаем поля login and password
    login = request.form.get("login")
    password = request.form.get("password")

    #авторизация (если полей login and password нет ):
    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if request.method == 'POST':
                flash('Отлично!')
        else: #если логин или пароль не совпадают 
            if request.method == 'POST':
                flash('Неверный логин или пароль')
    else:
        if request.method == 'POST':
            flash('Пожалуйста, заполните все поля')
    
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    #если уже залогинен:
    if current_user.is_authenticated:
	    return redirect(url_for('account'))

    login = request.form.get("login")
    password = request.form.get("password")
    promocode_all = 0

    if request.method == 'POST':
        if not (login or password):
            flash('Пожалуйста, заполните все поля')
        
        else:
            if 17 >= len(request.form['login']) >= 3 and len(request.form['password']) >= 8:
                hash_p = generate_password_hash(password)
                new_user = User(login=login, password=hash_p, promocode_all=promocode_all)
                #проверка на уникальность логина
                try:
                    new_user = User.query.filter_by(login=new_user.login).one()
                except NoResultFound:
                    #логин уникален
                    flash('Учётная запись успешно создана!')
                else:
                    #логин занят
                    flash('Никнейм уже занят );')
                db.session.add(new_user)
                db.session.commit()
            elif len(request.form['login']) < 3:
                flash('Длина логина > 3 символов.')
            elif len(request.form['login']) > 17:
                flash('Длина логина не больше 17 символов.')
            elif len(request.form['password']) < 8:
                flash('Длина пароля > 8 символов.')

    return render_template('register.html')

@app.route("/account")
@login_required
def account():

    return render_template('account.html')

#phone style
@app.route("/ph_posts")
def ph_posts():
    now = datetime.now()
    articles = Article.query.order_by(Article.number.desc()).all()

    def time_checker(article):
        return article.date > datetime.now() + timedelta(hours=-24)


    return render_template('phone_posts.html', articles=articles, time_checker=time_checker)

@app.route("/phone")
def phone():

    return render_template("phone_index.html")

@app.route("/ph_login", methods=["GET", "POST"])
def ph_login():
    #если уже залогинен:
    if current_user.is_authenticated:
	    return redirect(url_for('ph_account'))
    
    #ожидаем поля login and password
    login = request.form.get("login")
    password = request.form.get("password")

    #авторизация (если полей login and password нет ):
    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if request.method == 'POST':
                flash('Отлично!')
        else: #если логин или пароль не совпадают 
            if request.method == 'POST':
                flash('Неверный логин или пароль')
    else:
        if request.method == 'POST':
            flash('Пожалуйста, заполните все поля')
    
    return render_template("phone_login.html")

@app.route("/ph_register", methods=["GET", "POST"])
def ph_register():
    #если уже залогинен:
    if current_user.is_authenticated:
	    return redirect(url_for('ph_account'))

    login = request.form.get("login")
    password = request.form.get("password")
    promocode_all = 0

    if request.method == 'POST':
        if not (login or password):
            flash('Пожалуйста, заполните все поля')
        
        else:
            if 17 >= len(request.form['login']) >= 3 and len(request.form['password']) >= 8:
                hash_p = generate_password_hash(password)
                new_user = User(login=login, password=hash_p, promocode_all=promocode_all)
                #проверка на уникальность логина
                try:
                    new_user = User.query.filter_by(login=new_user.login).one()
                except NoResultFound:
                    #логин уникален
                    flash('Учётная запись успешно создана!')
                    return redirect(url_for('ph_login'))
                else:
                    #логин занят
                    flash('Никнейм уже занят ;(')
                db.session.add(new_user)
                db.session.commit()
            elif len(request.form['login']) < 3:
                flash('Длина логина > 3 символов.')
            elif len(request.form['login']) > 17:
                flash('Длина логина не больше 17 символов.')
            elif len(request.form['password']) < 8:
                flash('Длина пароля > 8 символов.')

    return render_template("phone_register.html")

@app.route("/ph_account")
def ph_account():
    if current_user.is_authenticated:
        return render_template("phone_account.html")
    else:
        return redirect(url_for('ph_login'))
#phone style

@app.route("/account/<int:id>")
def def_account(id):

    user = User.query.get(id)
    return render_template('def_account.html', user=user)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for("login_page"))
    return response
#

if __name__=="__main__":
    app.run(debug=True)