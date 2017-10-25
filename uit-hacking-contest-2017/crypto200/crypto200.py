#!/usr/bin/python

#__author__ = qd
from flask import Flask, request, render_template_string
import os
import json
import string
from hashlib import md5
from Crypto.Cipher import AES

key = os.urandom(16)
flag = 'A_real_@dm1n_must_know_how_to_use_crypto_the_right_w@y'
menu = """<html>
<title>Adult Entertainment Service</title>
<body>
<h2>Welcome to our Adult Entertainment Service!</h2>
Don't have an account? <a href="register"><button>Register</button></a><br><br>
Already a member? <a href="login"><button>Login</button></a><br><br>
<!--I'm a 900db01, so I give yo<a href="source"><button>source</button></a><br><br>-->
Remember that, only <b>admin</b> can view <b>flag</b>.
</body>
</html>"""
menu_register = """<html>
<title>Registration Page</title>
<form action="/register" method="post">Username: <input type=text name=username> <input type=submit value=Register></form>
</html>"""
menu_login = """<html>
<title>Login Page</title>
<form action="/login" method="post">Token: <input type=text name=token> <input type=submit value=Login></form>
</html>"""
menu_homepage = """<html>
<title>Welcome</title>
<body>
<h2>Welcome, %s!</h2>
Your token is %s
</body>
</html>
"""
menu_user = """<html>
<title>Homepage</title>
<h2>Welcome back, %s!</h2>
You need to be admin to get flag!
</html>"""
win = """<html>
<title>Admin Panel</title>
<h2>Welcome back, admin!</h2>
Here's your flag: """ + flag + "<br></html>"
error = "<title>Error</title><h2>Invalid credential!<h2>"
class AES_(object):

    def __init__(self, key):
        self.blocksize = 16
        self.key = md5(key.encode("hex")).digest()

    def pad(self, st):
        return st + (self.blocksize - len(st) % self.blocksize) * chr(self.blocksize - len(st) % self.blocksize)

    def unpad(self, st):
        return st[:-ord(st[len(st)-1:])]

    def encrypt(self, msg):
        msg = self.pad(msg)
        iv = os.urandom(16)
        crypt = AES.new(self.key, AES.MODE_CBC, iv)
        return (iv + crypt.encrypt(msg)).encode("base64")

    def decrypt(self, msg):
        msg = msg.decode("base64")
        iv = msg[:self.blocksize]
        crypt = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(crypt.decrypt(msg[self.blocksize:]))

def valid(username):
    if username != "" and u'admin' not in username.lower() and not any(char not in string.printable[:62] for char in list(username)):
        return True
    return False

def generate_token(username):
    aes = AES_(key)
    cred = {}
    cred['user'] = username
    cred_encrypted = aes.encrypt(json.dumps(cred))
    return (username, cred_encrypted)

def check(token):
    aes = AES_(key)
    try:
        login = json.loads(aes.decrypt(token))
    except:
        return error
    if login['user'] == 'admin':
        open('logs.txt', 'a').write(token + " " + str(login))
        return win
    else:
        return menu_user % (login['user'], login['user'])

app = Flask(__name__)
@app.route('/')
def index():
	return render_template_string(menu)

@app.route('/secret_log')
def log():
    src = open("logs.txt").read()
    return render_template_string(src)

@app.route('/source')
def source():
    src = open("src.txt").read()
    return render_template_string(src)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if valid(request.form['username']):
        	send_token = generate_token(request.form['username'])
        	return render_template_string(menu_homepage % send_token)
        else:
            return render_template_string('<title>Hacker Detected!</title><h2>Go away, hackers!<h2>')
    else:
    	return render_template_string(menu_register)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['token']:
            return render_template_string(check(request.form['token']))
    else:
    	return render_template_string(menu_login)

if __name__ == '__main__':
	app.run(host="0.0.0.0")