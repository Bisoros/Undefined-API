from flask import Flask, request, Response, jsonify, redirect, render_template, session
import bcrypt

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.bank1
users = db.users

app = Flask(__name__)

@app.route('/user', methods = ['POST'])
def create_user():
    email    = request.form.get('email')
    password = request.form.get('password').encode()
    name     = request.form.get('name')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    users.insert({
        'email'  : email,
        'hashed' : hashed,
        'name'   : name,
        'salt'   : salt,
    })




if __name__ == '__main__':
    app.run(port = 8081,
            host = '0.0.0.0',
            )
