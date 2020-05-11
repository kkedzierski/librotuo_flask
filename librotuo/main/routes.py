from flask import render_template
from flask import request
from librotuo.models import Book
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=6)
    return render_template('home.html', books=books)


@main.route('/about')
def about():
    return render_template('about.html', title='about')
