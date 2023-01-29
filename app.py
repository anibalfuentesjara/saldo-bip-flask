from flask import (
    Flask, 
    abort,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from markupsafe import escape
import secrets

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Index page!</p>"

#@app.get('/hello')
#@app.post('/hello')
#@app.route("/hello", methods=['GET', 'POST']) use with request.method=='POST'
@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route("/user/<string:username>")
def user(username):
    return f'<p>Hello user {escape(username)}</p>'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

#request object
def valid_login(username, password):
    return username=='admin' and password=='admin'

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        #searchword = request.args.get('key', '') TO ACCESS QUERY PARAMS
        if valid_login(request.form['username'],
                       request.form['password']):
            return redirect(url_for('user', username=request.form['username']))
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

#debug
with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello'))
    print(url_for('user', username='Anibal fuentes'))
    print(url_for('show_post', post_id=10))
    print(url_for('static', filename='zelda.jpg'))

#for unit test
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

""" Upload files
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")
    ...
"""

#Cookies
@app.route('/get-cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f"<p>cookie username: {username}</p>"

@app.route('/set-cookie/<string:username>')
def set_cookie(username=None):
    resp = make_response(render_template('hello.html', username=username))
    resp.set_cookie('username', username)
    return resp

#redirect and errors
@app.route('/redirect')
def redirect_view():
    return redirect(url_for('error'))

@app.route('/error')
def error():
    abort(401)

#404 not found customization
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

class User:
    def __init__(self, username, theme, image='zelda.jpg'):
        self.username = username
        self.theme = theme
        self.image = image


#APIs with json
def get_current_user():
    return User(username="anibal", theme="dark theme")

@app.route("/me")
def me_api():
    user=get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("static", filename=user.image)
    }

#Sessions
app.secret_key = secrets.token_hex()

@app.route('/session-index')
def session_index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/session-login', methods=['GET', 'POST'])
def session_login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('session_index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('session_index'))
