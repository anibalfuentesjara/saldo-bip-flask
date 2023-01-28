from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Index page!</p>"


@app.route("/hello")
def hello():
    return "<p>Hello world!</p>"

@app.route("/user/<string:username>")
def user(username):
    return f'<p>Hello user {escape(username)}</p>'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'