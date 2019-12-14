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

@app.route('/accounts', methods = ['GET'])
def accounts():
    email    = request.form.get('email')
    token    = request.form.get('token')

    user = users.find_one({'email' : email})

    if user['token'] == token:
        return user['accounts']
    else:
        return 'da-te in mortii ma-tii'

@app.route('/account', methods = ['POST'])
def account():
    email     = request.form.get('email')
    token     = request.form.get('token')
    accountID = request.form.get('accountID')
    currency  = request.form.get('currency')

    user = users.find_one({'email' : email})

    if user['token'] == token:
        users.update({'email' : email},
                      {'$push' : {'accountID' : accountID,
                                  'currency'  : currency,
                      }})
    else:
        return 'da-te in mortii ma-tii'

if __name__ == '__main__':
    app.run(port = 8080,
            host = '0.0.0.0',
            )
