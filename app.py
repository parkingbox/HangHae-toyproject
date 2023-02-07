from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.gofestival


@app.route('/')
def home():
  return render_template('detail.html')

@app.route('/savedata', methods=["POST"])
def data_post():
  data = request.form
  print(data)
  for i in data:
    contentid = i['contentid']
    add1 = i['add1']
    add2 = i['add2']
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
      contentid,
      add1,
      add2,
      eventstartdate,
      eventenddate,
      firstimage,
      firstimage2,
      mapx,
      mapy,
      modifiedtime,
      tel,
      title,
    }

    db.detail.insert_one(doc)
  
  return jsonify({'msg': '!!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)