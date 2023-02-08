from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oj62xnf.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta




@app.route('/')
def home():
   return render_template('index.html')

# 이건잘 돌아감
@app.route('/modify')
def modify():
   return render_template('modify.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]

    count = list(db.bucket.find({},{'_id':False}))
    num = len(count) + 1

    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg':'등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

#삭재버튼
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
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'bucket': modify_receive}})
    return jsonify({'msg': '수정 완료!'})




if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)