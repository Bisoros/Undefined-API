from flask import Flask, request, Response, jsonify, redirect, render_template, session
import bcrypt
from secrets import token_urlsafe

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.bank1
users = db.users

app = Flask(__name__)

@app.route('/user', methods = ['POST'])
def create_user():
    print(request.form)
    email    = request.form.post('email')
    password = request.form.post('password').encode()
    name     = request.form.post('name')


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




if __name__ == '__main__':
    app.run(port = 8081,
            host = '0.0.0.0',
            )
