from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import bson , json


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app= Flask(__name__ )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    done= db.Column(db.Boolean, default=False)

    def __init__(self, title, description, done=False):
        self.title = title
        self.description = description
#get all
@app.route('/todo/api/v1.0/tasks',methods=['GET'])
def list():
  mylist=[]
  ret= Task.query.all()
  for x in ret:
      print (x)
      mylist.append({'title':x.title, 'description':x.description, 'done':x.done})
  return jsonify({'Tasks': mylist})

@app.route('/todo/api/v1.0/tasks/<id>',methods=['GET'])
def listone(id):
  x=Task.query.filter_by(id=id).first_or_404()
  return jsonify({'Task': {'title':x.title, 'description':x.description, 'done':x.done}})

@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def add():
  #add = mongo.db.tasks.insert({'title':'Pray Fajr' , 'description':'Configure alarm and rise for Fajr', 'done':False})
  add = Task(title = request.form['title'] , description= request.form['description'], done=request.form['done'])
  db.session.add(add)
  db.session.commit()
  ret= Task.query.all()
  mylist=[]
  for x in ret:
      print (x)
      mylist.append({'title':x.title, 'description':x.description, 'done':x.done})
  return jsonify({'Tasks': mylist})

#update
@app.route('/todo/api/v1.0/tasks/<id>',methods=['PUT'])
def updateTask(id):
  x=Task.query.filter_by(id=id).first_or_404()
  dataDict=json.loads(request.data)
  if 'title' in dataDict:
    x.title=dataDict['title']
  if 'description' in dataDict:
    x.description=dataDict['description']
  if 'done' in dataDict:
    if dataDict['done']=='true': x.done=True
    else: x.done=False
  db.session.commit()
  return "Success"

#delete
@app.route('/todo/api/v1.0/tasks/<id>',methods=['DELETE'])
def updateTask(id):
  x=Task.query.filter_by(id=id).first_or_404()
  db.session.delete(x)
  db.session.commit()
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