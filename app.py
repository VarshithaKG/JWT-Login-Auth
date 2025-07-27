from flask import Flask, render_template, request, redirect, make_response
import jwt
import datetime

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # used for encoding/decoding JWT

# Dummy username and password
USERNAME = 'admin'
PASSWORD = 'password'

# Home route (login page)
@app.route('/')
def home():
    return render_template('login.html')

# Login route (form submission)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        # create JWT token
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }, app.secret_key)

        resp = make_response(redirect('/welcome'))
        resp.set_cookie('token', token)
        return resp
    else:
        return 'Invalid credentials. Try again.'

# Welcome page (after login)
@app.route('/welcome')
def welcome():
    token = request.cookies.get('token')
    if not token:
        return redirect('/')

    try:
        decoded = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        username = decoded['user']
        return render_template('welcome.html', username=username)
    except jwt.ExpiredSignatureError:
        return 'Token expired. Login again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Login again.'

if __name__ == '__main__':
    app.run(debug=True)
