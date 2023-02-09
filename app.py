import sys, json
from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.qkuxaox.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
  return render_template('list.html')

@app.route("/showdata", methods=["GET"])
def festival_get():
    festival_list = list(db.list.find({}, {'_id':False}))
    return jsonify({'festivals': dumps(festival_list)})

@app.route('/savedata', methods=["POST"])
def data_post():
  data = request.form.getlist('data')
  parsedata = json.loads(data[0])

  for i in parsedata:
    if i['firstimage'] != "":
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
  
      db.list.insert_one(doc)
  
  return jsonify({'msg': '완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)