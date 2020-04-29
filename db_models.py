from index import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # books = db.relationship('Book', backref='addedby', lazy=True)

    def __repr__(self):
        return "User({username}, {email}, {image_file})".format(username=self.username,
                                                                email=self.email,
                                                                image_file=self.image_file)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=True)
    authors = db.Column(db.String(300), nullable=True)
    published_date = db.Column(db.String(12), nullable=True)
    ISBN_number = db.Column(db.String(300), nullable=True)
    page_number = db.Column(db.Integer, nullable=True)
    cover_url = db.Column(db.String(120), nullable=True)
    publication_language = db.Column(db.String(20), nullable=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return "Book({title}, {authors}, {page_number}, " \
               "{cover_url})".format(title=self.title, authors=self.authors,
                                     page_number=self.page_number,
                                     cover_url=self.cover_url)
