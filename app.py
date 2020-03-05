from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
directory = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directory, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init database
db = SQLAlchemy(app)
# Init ma
mml = Marshmallow(app)

# Message Class/Model
class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  msg = db.Column(db.String(400))

  def __init__(self, msg):
    self.msg = msg

# Message Schema
class MessageSchema(mml.Schema):
  class Meta:
    fields = ('id', 'msg')

# Init schema
Message_schema = MessageSchema()
Messages_schema = MessageSchema(many=True)

#Create a Message
@app.route('/message', methods=['POST'])
def add_Message():
    msg = request.json['msg']
    
    new_Message = Message(msg)

    db.session.add(new_Message)
    db.session.commit()

    return Message_schema.jsonify(new_Message)

# Get All Messages
@app.route('/message', methods=['GET'])
def get_Messages():
    all_Messages = Message.query.all()
    result = Messages_schema.dump(all_Messages)
    return jsonify(result)

# Get Single Message
@app.route('/message/<id>', methods=['GET'])
def get_Message(id):
    Message = Message.query.get(id)
    return Message_schema.jsonify(Message)
     
#Update a Message
@app.route('/message/<id>', methods=['PUT'])
def update_Message(id):
    Message = Message.query.get(id)
    msg = request.json['msg']
    Message.msg = msg
    
    db.session.commit()

    return Message_schema.jsonify(Message)

# Delete a Message
@app.route('/message/<id>', methods=['DELETE'])
def delete_Message(id):
    Message = Message.query.get(id)
    db.session.delete(Message)
    db.session.commit()
    
    return Message_schema.jsonify(Message)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)