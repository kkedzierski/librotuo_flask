from flask import render_template, url_for, flash, redirect
from flask import request, abort
from librotuo import db
from librotuo.books.forms import BookForm
from librotuo.models import Book
from flask_login import current_user, login_required
from datetime import datetime

from flask import Blueprint

books = Blueprint('books', __name__)


@books.route('/book/new', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        if not form.cover_url.data:
            form.cover_url.data = "https://ibf.org/site_assets/"\
                                  "img/placeholder-book-cover-default.png"
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
        return redirect(url_for('main.home'))
    return render_template('add_book.html', title="Add new book",
                           form=form, legend="New Book")


@books.route('/book/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@books.route('/book/<int:book_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('books.book', book_id=book.id))
    elif request.method == 'GET':
        form.title.data = book.title
        form.authors.data = book.authors
        form.published_date.data = datetime.strptime(book.published_date,
                                                     "%Y-%m-%d").date()
        form.ISBN_number.data = book.ISBN_number
        form.page_number.data = book.page_number
        form.cover_url.data = book.cover_url
        form.publication_language.data = book.publication_language
    return render_template('add_book.html', title="Update book",
                           form=form, legend="Update Book")


@books.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.addedby != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('main.home'))


@books.route('/search', methods=['POST', 'GET'])
def search_book():
    if request.method == 'POST':
        if request.form.get('title_input'):
            title = request.form.get('title_input').capitalize()
            books = Book.query.filter(Book.title.contains(title)).paginate()
        if request.form.get('authors_input'):
            authors = request.form.get('authors_input').capitalize()
            books = Book.query.filter(Book.authors.contains(authors)
                                      ).paginate()
        if request.form.get('lang_input'):
            lang = request.form.get('lang_input')
            books = Book.query.filter(Book.publication_language.contains(lang)
                                      ).paginate()
        if request.form.get('publication_date_input'):
            passed_date = request.form.get('publication_date_input')
            if len(passed_date) == 4:
                passed_date += '-01-01'
            passed_date = datetime.strptime(passed_date, '%Y-%m-%d')
            books = Book.query.filter(Book.published_date >= passed_date
                                      ).paginate()
        if books.items:
            return render_template('home.html', books=books)
        else:
            flash('Book not found!', 'danger')
            return redirect(url_for('main.home'))
