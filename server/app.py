from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at).all()
        messages_dicts = []
        for message in messages:
            messages_dicts.append(message.to_dict())

        return make_response(messages_dicts, 200)
    elif request.method == "POST":
        data = request.get_json()
        message = Message(body=data["body"], username=data["username"])
        
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    if request.method == "PATCH":
        data = request.get_json()
        message = Message.query.filter_by(id=id).first()
        message.body = data["body"]

        db.session.commit()

        return make_response(message.to_dict(), 200)
    elif request.method == "DELETE":
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()
        return make_response({"message":"deleted successfully"}, 200)

if __name__ == '__main__':
    app.run(port=4000)
