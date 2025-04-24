from flask import Flask, render_template, request
from flask_socketio import SocketIO,emit,join_room,leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('chat.html')


@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    emit('message',{'msg':'User joined room', 'sender': 'system'},room=room, broadcast=True)


@socketio.on('leave')
def leave(data):
    room = data['room'] 
    leave_room(room)
    emit('message', {'msg':'User left room', 'sender': 'system'}, room=room, broadcast=True)


@socketio.on('message')
def message(data):
    room = data['room']
    message = data['msg']
    emit('message', {'msg': message, 'sender': 'self'}, include_self=True)
    emit('message', {'msg': message, 'sender': 'other'}, room=room, skip_sid=request.sid)


if __name__ == '__main__':
    socketio.run(app,debug=True)
    