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
  return jsonify({'Tasks': mylist})

@app.route('/todo/api/v1.0/tasks/<id>',methods=['GET'])
def listone(id):
  x=mongo.db.tasks.find_one_or_404({'_id': bson.ObjectId(oid=str(id))})
  return jsonify({'Task': {'title':x['title'], 'description':x['description'], 'done':x['done']}})

@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def add():
  #add = mongo.db.tasks.insert({'title':'Pray Fajr' , 'description':'Configure alarm and rise for Fajr', 'done':False})
  add = mongo.db.tasks.insert({'title':request.form['title'] , 'description':request.form['description'], 'done':request.form['done']})
  ret= mongo.db.tasks.find()
  mylist=[]
  for x in ret:
      print (x)
      mylist.append({'title':x['title'], 'description':x['description'], 'done':x['done']})
  return jsonify({'Tasks': mylist})
  #return 'Added success'


## update ````````````
@app.route('/todo/api/v1.0/tasks/<id>',methods=['PUT'])
def updateTask(id):
  x=mongo.db.tasks.find_one_or_404({'_id': bson.ObjectId(oid=str(id))})
  dataDict=json.loads(request.data)
  if 'title' in dataDict:
    x['title']=dataDict['title']
  if 'description' in dataDict:
    x['description']=dataDict['description']
  if 'done' in dataDict:
    if dataDict['done']=='true': x['done']=True
    else: x['done']=False
  mongo.db.tasks.save(x)
  return "Success"

@app.route('/todo/api/v1.0/tasks/<id>',methods=['DELETE'])
def deleteTask(id):
  x=mongo.db.tasks.delete_one({'_id': bson.ObjectId(oid=str(id))})
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