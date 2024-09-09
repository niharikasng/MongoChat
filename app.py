from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

client = MongoClient('mongodb://localhost:27017/')
db = client['chatapp']
messages_collection = db['messages']

@socketio.on("message")
def sendMessage(data):
    username = data['username']
    message = data['message']
    # Store message along with the username in MongoDB
    messages_collection.insert_one({'username': username, 'message': message})
    # Broadcast the message to all clients
    send({'username': username, 'message': message}, broadcast=True)

@app.route("/")
def signUp():
    return render_template("getuser.html")

@app.route("/index")
def message():
    username = request.args.get("username")
    if username:
        # Retrieve chat history from MongoDB
        chat_history = list(messages_collection.find())
        return render_template("index.html", username=username, chat_history=chat_history)
    else:
        return redirect(url_for('signUp'))

if __name__ == "__main__":
    socketio.run(app, debug=True)