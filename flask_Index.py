from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def hello():
    name = request.args.get("name", "Home Page")
    return f'<h1>This is, {escape(name)}</h1>'

@app.route('/about')
def about():
    name = request.args.get("name", "About Page")
    return f'<h1>This is, {escape(name)}</h1>'

if __name__ == '__main__':
    app.run(debug=True)

