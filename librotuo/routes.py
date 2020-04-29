from flask import render_template, url_for, flash, redirect
from librotuo import app, db, bcrypt
from librotuo.forms import RegistrationForm, LoginForm
from librotuo.models import User, Book


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!, '
              'You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'pass':
            flash(f"Login successful", 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your email and passoword',
                  'danger')
    return render_template('login.html', title='Login', form=form)
