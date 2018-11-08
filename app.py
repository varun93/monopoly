from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from adjudicator import Adjudicator
import json

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
	adjudicator = Adjudicator()
	return render_template('index.html')

@socketio.on('start')
def start_game(data):
	pass
	# what is the difference between send and emit?
    # join_room(room)
    # adjudicator
	# emit('state_updated', {'state': state})

if __name__ == '__main__':
	socketio.run(app, debug=True)

