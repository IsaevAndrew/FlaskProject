from flask import request
from werkzeug.exceptions import abort
from project.data import db_session
from project.data.users import User
from project.data.book import Book
from project.data.avtor import Avtor
from project.data.genre import Genre
from project.data.opinion import Opinion
from project.data.wishlist import Wishlist
from project.forms.register import RegisterForm
from werkzeug.utils import secure_filename
from project.forms.add_opinion import OpinionsForm
from project.forms.add_avtor import AvtorsForm
from project.forms.add_book import BooksForm
from project.forms.login import LoginForm
from flask import Flask, url_for, render_template, redirect
from flask_login import LoginManager, logout_user, login_required
from flask_login import login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    a = []
    b = []
    if current_user.is_authenticated:
        op = db_sess.query(Opinion).filter(
            Opinion.id_user == current_user.id).all()
        wl = db_sess.query(Wishlist).filter(
            Wishlist.id_user == current_user.id).all()
        for i in op:
            a.append(i.id_book)
        for i in wl:
            b.append(i.id_book)
    avtors = db_sess.query(Avtor).all()
    return render_template("board_of_books.html", title='Книжная Полка',
                           avtors=avtors, books=books, a=a, b=b)


@app.route('/account')
def account():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    avtors = db_sess.query(Avtor).all()
    return render_template("account.html", title='Книжная Полка', avtors=avtors,
                           books=books)


@app.route('/Mybooks')
def Mybooks():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    a = []
    if current_user.is_authenticated:
        op = db_sess.query(Opinion).filter(
            Opinion.id_user == current_user.id).all()
        for i in op:
            a.append(i.id_book)
    avtors = db_sess.query(Avtor).all()
    return render_template("Mybooks.html", title='Книжная Полка', avtors=avtors,
                           books=books, a=a)


@app.route('/Mylist')
def Mylist():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    b = []
    if current_user.is_authenticated:
        wl = db_sess.query(Wishlist).filter(
            Wishlist.id_user == current_user.id).all()
        for i in wl:
            b.append(i.id_book)
    avtors = db_sess.query(Avtor).all()
    return render_template("Mylist.html", title='Книжная Полка', avtors=avtors,
                           books=books, b=b)


@app.route('/Myopinions')
def Myopinions():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    a = []
    if current_user.is_authenticated:
        op = db_sess.query(Opinion).filter(
            Opinion.id_user == current_user.id).all()
        for i in op:
            a.append(i.id_book)
    avtors = db_sess.query(Avtor).all()
    print(a)
    return render_template("Myopinions.html", title='Книжная Полка',
                           avtors=avtors, books=books, a=a)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_into_wl/<int:id>', methods=['GET', 'POST'])
@login_required
def add_into_wl(id):
    db_sess = db_session.create_session()
    wl = Wishlist()
    wl.id_user = current_user.id
    wl.id_book = id
    db_sess.merge(wl)
    db_sess.commit()
    return redirect('/')


@app.route('/del_in_wl/<int:id>', methods=['GET', 'POST'])
@login_required
def del_in_wl(id):
    db_sess = db_session.create_session()
    a = db_sess.query(Wishlist).filter(Wishlist.id_book == id,
                                       Wishlist.id_user == current_user.id
                                       ).first()
    db_sess.delete(a)
    db_sess.commit()
    return redirect('/Mylist')


@app.route('/addbook', methods=['GET', 'POST'])
@login_required
def add_books():
    db_sess = db_session.create_session()
    avt = [(x.surname, x.surname) for x in db_sess.query(Avtor).all()]
    g = [(x.title, x.title) for x in db_sess.query(Genre).all()]
    form = BooksForm()
    form.content1.choices = avt
    form.content5.choices = g
    if form.validate_on_submit():
        books = Book()
        a = form.content1.data
        b = db_sess.query(Avtor).filter(Avtor.surname == a).first()
        books.id_avt = b.id
        books.title = form.content2.data
        books.year = form.content3.data
        books.publish = form.content4.data
        a = form.content5.data
        b = db_sess.query(Genre).filter(Genre.title == a).first()
        books.id_genre = b.id
        filename = secure_filename(form.content6.data.filename)
        form.content6.data.save('static/img/' + filename)
        books.name_foto = form.content6.data.filename.split("/")[
            -1] if form.content6.data else ""
        books.book_creater = current_user
        db_sess.merge(books)
        db_sess.commit()
        return redirect('/')
    return render_template('addbook.html', title='Добавление книги',
                           form=form)


@app.route('/addavtor', methods=['GET', 'POST'])
@login_required
def add_avtors():
    db_sess = db_session.create_session()
    form = AvtorsForm()
    if form.validate_on_submit():
        a = form.content1.data
        b = form.content2.data
        db_sess = db_session.create_session()
        q = db_sess.query(Avtor).filter(Avtor.name == a,
                                        Avtor.surname == b
                                        ).first()
        if not q:
            avtors = Avtor()
            avtors.name = form.content1.data
            avtors.surname = form.content2.data
            db_sess.merge(avtors)
            db_sess.commit()
        return redirect('/')
    return render_template('addavtor.html', title='Добавление автора',
                           form=form)


@app.route('/addopinion/<int:id>', methods=['GET', 'POST'])
@login_required
def add_opinions(id):
    db_sess = db_session.create_session()
    form = OpinionsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        op = Opinion()
        op.id_user = current_user.id
        op.opinion = request.form['about']
        op.id_book = id
        db_sess.merge(op)
        db_sess.commit()
        return redirect('/')
    return render_template('addopinion.html', title='Добавление отзыва',
                           form=form, a='')


@app.route('/edit_opinion/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_opinion(id):
    form = OpinionsForm()
    db_sess = db_session.create_session()
    opinion = db_sess.query(Opinion).filter(Opinion.id_book == id,
                                            Opinion.id_user == current_user.id).first()
    a = opinion.opinion
    if form.validate_on_submit():
        opinion.opinion = request.form['about']
        opinion.id_user = opinion.id_user
        opinion.id_book = opinion.id_book
        db_sess.commit()
        return redirect('/')
    return render_template('addopinion.html',
                           title='Редактирование отзыва',
                           form=form, a=a)


@app.route('/opinions/<int:id>', methods=['GET', 'POST'])
def opinions(id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).filter(Book.id == id,
                                      ).first()
    users = db_sess.query(User).all()
    opinions = db_sess.query(Opinion).filter(Opinion.id_book == id).all()
    return render_template("opinions.html", opinions=opinions, name=book.title,
                           users=users)


@app.route('/book_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def book_delete(id):
    db_sess = db_session.create_session()
    a = db_sess.query(Book).filter(Book.id == id,
                                   Book.book_creater == current_user
                                   ).first()
    b = db_sess.query(Opinion).filter(Opinion.id_book == id).all()
    if a:
        for i in b:
            db_sess.delete(i)
        db_sess.delete(a)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/books.db")
    app.run(port=5000, host='127.0.0.1')
