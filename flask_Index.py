from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

