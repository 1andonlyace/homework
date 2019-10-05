from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

#어떤 페이지로?
@app.route('/')
def home():
  return render_template('nhrspm.html')

#포스팅
@app.route('/order', methods=['POST'])
def POST():
  name = request.form['name_give']
  count = request.form['count_give']
  address = request.form['address_give']
  phone = request.form['phone_give']
  item = request.form['item_give']

  doc = {
      'name':name,
      'count':count,
      'address':address,
      'phone': phone,
      'item': item
  }
  db.orderlists.insert_one(doc)
  return jsonify({'result':'success'})

#리스팅
@app.route('/order', methods=['GET'])
def listing():
    cstmr_info = request.args.get('item_give')
    result = list(db.orderlists.find({'item': cstmr_info}, {'_id': 0}))

    return jsonify({'result': 'success', 'orders': result})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)



