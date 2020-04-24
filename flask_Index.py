from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '349eb206fa81e05f09ef955193bb062d'

posts = [
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings II two towers',
        'content': '312 pages',
        'data_published': 'June 18, 1975'
    },
    {
        'author': 'Tolkien',
        'title': 'Lords of the Rings',
        'content': '450 pages',
        'data_published': 'April 10, 1970'
    }

]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
     return render_template('about.html', title = 'about')

@app.route('/register', methods=['GET', 'POST'])
def register():
     form = RegistrationForm()
     if form.validate_on_submit():
         flash(f'Account created for { form.username.data }!', 'success')
         return redirect(url_for('home'))
     return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
         if form.email.data == 'admin@admin.com' and form.password.data == 'pass':
             flash(f"Login successful", 'success')
             return redirect(url_for('home'))
         else:
             flash(f'Login Unsuccessful. Please check your email and passoword', 'danger')
     return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)

