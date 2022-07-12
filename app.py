from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.nv3ij.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/as", methods=["POST"])
def web_as_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y년%m월%d일%H시%M분%S초')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title':title_receive,
        'content':content_receive,
        'file':f'{filename}.{extension}'
    }

    db.as.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route("/as", methods=["GET"])
def web_as_get():
    order_list = list(db.mars.find({}, {'_id': False}))
    return jsonify({'orders':order_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
