
from pymongo import MongoClient
import sys
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# import certifi
# ca = certifi.where()
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.oj62xnf.mongodb.net/?retryWrites=true&w=majority')
# client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority')
# client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.gofestival


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list')
def home():
    return render_template('list.html')


@app.route("/showdata", methods=["GET"])
def festival_get():
    festival_list = list(db.list.find({}, {'_id': False}))
    return jsonify({'festivals': json.dumps(festival_list)})


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

# 이건잘 돌아감


@app.route('/modify')
def modify():
    return render_template('modify.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]

    count = list(db.bucket.find({}, {'_id': False}))
    num = len(count) + 1

    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

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

# list


@app.route("/list", methods=["GET"])
def get_list():


list_data = list(db.detail.find({}, {'_id': False}))
return jsonify({'list': list_data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)
