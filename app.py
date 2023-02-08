import sys, json
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.gofestival


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
  id = request.form['id']
  pw = request.form['pw']
  doc ={
    'id': id,
    'pw': pw,
  }
  db.users.insert_one(doc)
  return jsonify({'msg':'로그인 성공'})

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
      firstimage= i['firstimage']
      firstimage2= i['firstimage2']
      mapx = i['mapx']
      mapy = i['mapy']
      modifiedtime= i['modifiedtime']
      tel= i['tel']
      title= i['title']
    
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
    print(contentid,file=sys.stderr)
    detail_data = db.detail.find_one({'contentid': contentid},{'_id':False})
    return jsonify({'data': detail_data})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)