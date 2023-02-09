import certifi
from pymongo import MongoClient
import sys
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


ca = certifi.where()
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.oj62xnf.mongodb.net/?retryWrites=true&w=majority')
# client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.gofestival


# 이건잘 돌아감


@app.route('/modify')
def modify():
    return render_template('modify.html')


@app.route('/crud')
def crud():
    return render_template('CRUD.html')

# 디테일 댓글 등록


@app.route("/comentsave", methods=["POST"])
def coment_post():
    coment_receive = request.form["coment_give"]
    param_receive = request.form["param_give"]
    count = list(db.coment.find({}, {'_id': False}))
    num = len(count) + 1
    # if findparam = param_receive:
    doc = {
        'num': num,
        'contentid': param_receive,
        'coment': coment_receive,
    }
    db.coment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})

# 댓글 데이터 불러오기


@app.route("/coment", methods=["POST"])
def coment_get():
    contentid = request.form['contentid']
    print(contentid, file=sys.stderr)

    coment_list = list(db.coment.find(
        {'contentid': contentid}, {'_id': False}))
    return jsonify({'coments': coment_list})

# 삭재버튼


@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    deletenum_receive = request.form["deletenum_give"]
    db.bucket.delete_one({'num': int(deletenum_receive)})
    return jsonify({'msg': '삭재완료!'})


# 수정페이지에 db로수정값 보내주기
@app.route("/bucket/modify", methods=["POST"])
def bucket_modify():
    num_receive = request.form["bucketnum_give"]
    modify_receive = request.form["modify_give"]
    db.bucket.update_one({'num': int(num_receive)}, {
                         '$set': {'bucket': modify_receive}})
    return jsonify({'msg': '수정 완료!'})


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/index')
# def index():
#     return render_template('index.html')


@app.route("/showdata", methods=["GET"])
def festival_get():
    festival_list = list(db.detail.find({}, {'_id': False}))
    return jsonify({'festivals': json.dumps(festival_list)})


# lsit
@app.route("/list", methods=["GET"])
def get_list():
    list_data = list(db.detail.find({}, {'_id': False}))
    return jsonify({'list': list_data})


@app.route('/login', methods=["POST"])
def login():
    id = request.form['id']
    pw = request.form['pw']
    doc = {
        'id': id,
        'pw': pw,
    }
    db.users.insert_one(doc)
    return jsonify({'msg': '로그인 성공'})

# open api 저장


@app.route('/savedata', methods=["POST"])
def data_post():
    data = request.form.getlist('data')
    parsedata = json.loads(data[0])

    # print("@@", parsedata, file=sys.stderr)
    # print("@@", data[0], file=sys.stderr)

    for i in parsedata:
        if i['firstimage'] != "":
            # print("!!!!!", parsedata[i], file=sys.stderr)

            contentid = i['contentid']
            addr1 = i['addr1']
            addr2 = i['addr2']
            eventstartdate = i['eventstartdate']
            eventenddate = i['eventenddate']
            firstimage = i['firstimage']
            firstimage2 = i['firstimage2']
            mapx = i['mapx']
            mapy = i['mapy']
            modifiedtime = i['modifiedtime']
            tel = i['tel']
            title = i['title']

            doc = {
                'contentid': contentid,
                'addr1': addr1,
                'addr2': addr2,
                'eventstartdate': eventstartdate,
                'eventenddate': eventenddate,
                'firstimage': firstimage,
                'firstimage2': firstimage2,
                'mapx': mapx,
                'mapy': mapy,
                'modifiedtime': modifiedtime,
                'tel': tel,
                'title': title,
            }

            db.detail.insert_one(doc)

    return jsonify({'msg': '!!'})


@app.route("/detail/<param>")
def detail(param):
    # print(param,file=sys.stderr)
    return render_template("detail.html", param=param)


@app.route("/detail/<param>", methods=["POST"])
def get_data(param):
    contentid = param
    print(contentid, file=sys.stderr)
    detail_data = db.detail.find_one({'contentid': contentid}, {'_id': False})
    return jsonify({'data': detail_data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)
