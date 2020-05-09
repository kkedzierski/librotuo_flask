import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect
from flask import request, abort
from librotuo import app, db, bcrypt
from librotuo.forms import RegistrationForm, LoginForm, UpdateAccountForm
from librotuo.forms import BookForm
from librotuo.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=6)
    return render_template('home.html', books=books)


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have logged in successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and passoword',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='images/' + current_user.image_file)
    return render_template('account.html', title='Your account',
                           image_file=image_file, form=form)


@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        if not form.cover_url.data:
            form.cover_url.data = "https://ibf.org/site_assets/img/placeholder-book-cover-default.png"
        book = Book(title=form.title.data, authors=form.authors.data,
                    published_date=form.published_date.data,
                    ISBN_number=form.ISBN_number.data,
                    page_number=form.page_number.data,
                    cover_url=form.cover_url.data,
                    publication_language=form.publication_language.data,
                    addedby=current_user)
        db.session.add(book)
        db.session.commit()
        flash('You added new book!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', title="Add new book",
                           form=form, legend="New Book")


@app.route('/book/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@app.route('/book/<int:book_id>/update', methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.addedby != current_user:
        abort(403)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.authors = form.authors.data
        book.published_date = str(form.published_date.data)
        book.ISBN_number = form.ISBN_number.data
        book.page_number = form.page_number.data
        book.cover_url = form.cover_url.data
        book.publication_language = form.publication_language.data
        db.session.commit()
        flash('Your book has been updated!', 'success')
        return redirect(url_for('book', book_id=book.id))
    elif request.method == 'GET':
        form.title.data = book.title
        form.authors.data = book.authors
        form.published_date.data = datetime.strptime(book.published_date, "%Y-%m-%d").date()
        form.ISBN_number.data = book.ISBN_number
        form.page_number.data = book.page_number
        form.cover_url.data = book.cover_url
        form.publication_language.data = book.publication_language
    return render_template('add_book.html', title="Update book",
                           form=form, legend="Update Book")


@app.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.addedby != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/search', methods=['POST', 'GET'])
def search_book():
    if request.method == 'POST':
        if request.form.get('title_input'):
            title = request.form.get('title_input').capitalize()
            books = Book.query.filter(Book.title.contains(title)).paginate()
        if request.form.get('authors_input'):
            authors = request.form.get('authors_input').capitalize()
            books = Book.query.filter(Book.authors.contains(authors)).paginate()
        if request.form.get('lang_input'):
            lang = request.form.get('lang_input')
            books = Book.query.filter(Book.publication_language.contains(lang)).paginate()
        if request.form.get('publication_date_input'):
            passed_date = request.form.get('publication_date_input')
            if len(passed_date) == 4:
                passed_date += '-01-01'
            passed_date = datetime.strptime(passed_date, '%Y-%m-%d')
            books = Book.query.filter(Book.published_date >= passed_date).paginate()
        if books.items:
            return render_template('home.html', books=books)
        else:
            flash('Book not found!', 'danger')
            return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_books(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query\
        .filter_by(addedby=user)\
        .paginate(page=page, per_page=6)
    return render_template('user_books.html', books=books, user=user)
