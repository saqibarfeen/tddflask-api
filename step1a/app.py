from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os , bson , json

app= Flask(__name__ ,static_url_path='')

app.config['MONGO_DBNAME']='tddapi_flask'
app.config['MONGO_URI']= 'mongodb://saqib:pakistan12@ds159459.mlab.com:59459/tddapi_flask'

mongo=PyMongo(app)

@app.route('/todo/api/v1.0/tasks',methods=['GET'])
def list():
  mylist=[]
  ret= mongo.db.tasks.find()
  for x in ret:
      print (x)
      mylist.append({'title':x['title'], 'description':x['description'], 'done':x['done']})
  return jsonify({'SaylaniStudents': mylist})

@app.route('/todo/api/v1.0/tasks/<id>',methods=['GET'])
def listone(id):
  x=mongo.db.tasks.find_one_or_404({'_id': bson.ObjectId(oid=str(id))})
  return jsonify({'SaylaniStudents': {'title':x['title'], 'description':x['description'], 'done':x['done']}})

@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def add():
  #add = mongo.db.tasks.insert({'title':'Pray Fajr' , 'description':'Configure alarm and rise for Fajr', 'done':False})
  add = mongo.db.tasks.insert({'title':request.form['title'] , 'description':request.form['description'], 'done':request.form['done']})
  ret= mongo.db.tasks.find()
  mylist=[]
  for x in ret:
      print (x)
      mylist.append({'title':x['title'], 'description':x['description'], 'done':x['done']})
  return jsonify({'SaylaniStudents': mylist})
  #return 'Added success'


## update ````````````
@app.route('/todo/api/v1.0/tasks/<id>',methods=['PUT'])
def updateTask(id):
  x=mongo.db.tasks.find_one_or_404({'_id': bson.ObjectId(oid=str(id))})
  dataDict=json.loads(request.data)
  if dataDict['title'] is not None:
    x.title=dataDict['title']
  if dataDict['description'] is not None:
    x.title=dataDict['description']
  if dataDict['done'] is not None:
    x.title=dataDict['done']
  mongo.db.tasks.save(x)
  return "Success"

@app.route("/")
def index():
    return ''' 
<form action="/todo/api/v1.0/tasks" method="POST">
<input type="text" name="title" placeholder="title"><br>
<input type="text" name="description" placeholder="description"><br>
<input type="text" name="done" placeholder="done"><br>
<input type="submit" value="Send">
</form>
'''

app.run(host='0.0.0.0', port=5000,debug=True)