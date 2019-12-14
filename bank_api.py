from flask import Flask, request, Response, jsonify, redirect, render_template, session
import bcrypt
from secrets import token_urlsafe

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.mitten
users = db.users

app = Flask(__name__)

@app.route('/user', methods = ['POST'])
def create_user():
    email    = request.form.get('email')
    password = request.form.get('password').encode()
    name     = request.form.get('name')

    salt   = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    token  = token_urlsafe(16) 

    users.insert({
        'email'  : email,
        'hashed' : hashed,
        'name'   : name,
        'salt'   : salt,
        'token'  : token,
    })

    return 'ok'

@app.route('/user', methods = ['GET'])
def get_user():
    email    = request.form.get('email')
    password = request.form.get('password').encode()

    user = users.find_one({'email' : email})

    salt   = user['salt']
    hashed = bcrypt.hashpw(password, salt)

    if user['hashed'] == hashed:
        return user['token']
    else:
        return 'da-te in mortii ma-tii'


if __name__ == '__main__':
    app.run(port = 8081,
            host = '0.0.0.0',
            )
