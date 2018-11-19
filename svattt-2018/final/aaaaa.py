#!/usr/local/bin/python3
from flask import Flask, render_template, request, make_response
from _AES import * 
import json
import os
import base64
import jwt
import sys
import string

key = os.urandom(16)
pubkey = open('public.pem').read()
privkey = open('private.pem').read()

def encryptToken(username):
    aes = AES_(key)
    cred = {}
    cred['user'] = username
    cred_encrypted = aes.encrypt(json.dumps(cred))
    return cred_encrypted

def parseToken(token):
    try:
        payload = json.loads(json.dumps(jwt.decode(token, key=pubkey)))
        token = payload['auth']
        aes = AES_(key)
        auth = json.loads(aes.decrypt(token))
        if auth['user'] == 'admin':
            return FLAG
        else:
            return auth['user']
    except:
        return 'wrong format'

def generateToken(username):
    return jwt.encode({'auth':encryptToken(username)}, key=privkey, algorithm='RS256').decode('utf-8')

app = Flask(__name__)

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    return resp

@app.route('/register', methods = ['POST', 'GET'])
def register():
    resp = make_response(render_template('register.html'))
    if request.method == 'POST':
        name = request.form['name']
        if 'admin' in str(name) or any(char not in string.printable[:62] for char in list(name)):
            return 'not allowed'
        elif not name:
            return 'Use this token to authenticate as <code>guest</code>:\n <pre><code>' + generateToken('guest') + '</code></pre>'
        else:
            return 'Use this token to authenticate as <code>' + name + '</code>:\n <pre><code>' + generateToken(name) + '</code></pre>'
        return resp
    return resp

@app.route('/auth', methods = ['POST', 'GET'])
def auth():
    resp = make_response(render_template('auth.html'))
    if request.method == 'POST':
        token = request.form['auth']
        return parseToken(token)
    return resp

@app.route('/public.pem')
def getKey():
    return '<pre><code>' + pubkey + '</code></pre>'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
