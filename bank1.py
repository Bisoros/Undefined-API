from flask import Flask, request, Response, jsonify, redirect, render_template, session
import bcrypt
from secrets import token_urlsafe

from pymongo import MongoClient

import requests, json

client = MongoClient('localhost', 27017)
db = client.bank1
users = db.users

ports = {
    'B1' : 8081,
    'B2' : 8082,
    'B3' : 8083,
}

app = Flask(__name__)

@app.route('/balance', methods = ['GET'])
def balance():
    accountID = request.form.get('accountID')

    print(accountID)

    accounts = users.find_one({'id' : accountID[2:4]})['accounts']

    for account in accounts:
        if account['accountID'] == accountID[4:6]:
            return jsonify({
                'balance'  : account['balance'],
                'currency' : account['currency'], 
                })

@app.route('/add', methods = ['POST'])
def add():
    accountID = request.form.get('accountID')
    ammount   = request.form.get('ammount')


    accounts = users.find_one({'id' : accountID[2:4]})['accounts']

    for account in accounts:
        if account['accountID'] == accountID[4:6]:
            account['balance'] += int(ammount)
            users.find_one_and_update({'id': accountID[2:4]}, 
                                 {'$set': {'accounts': accounts}})
            return 'ok'

@app.route('/transaction', methods = ['POST'])
def transaction():
    accountID     = request.form.get('accountID')
    accountIDdest = request.form.get('accountIDdest')
    ammount       = int(request.form.get('ammount'))

    print('heeeeeeeeeeeeeeeeeeeeeeeeelp')
    print(accountID, ammount, accountIDdest)

    accounts = users.find_one({'id' : accountID[2:4]})['accounts']
    print(accounts)

    for account in accounts:
        print(account)
        if account['accountID'] == accountID[4:6]:
            if ammount <= account['balance']:
                account['balance'] -= ammount
                users.find_one_and_update({'id': accountID[2:4]}, 
                                    {'$set': {'accounts': accounts}})

                r = requests.post('http://34.89.193.58:' + str(ports[accountIDdest[:2]]) + '/add',
                data = {'accountID' : accountIDdest,
                        'ammount'   : ammount,
                       })

                return 'ok'
            else:
                return 'no money'
    


if __name__ == '__main__':
    app.run(port = 8081,
            host = '0.0.0.0',
            )
