from flask import Flask
from flask_socketio import SocketIO
from agent import Agent
from adjudicator import Adjudicator
import json

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('start_game')
def startGame():
	adjudicator = Adjudicator(Agent,Agent,socketio)
	adjudicator.runGame()

if __name__ == '__main__':
	socketio.run(app, debug=True)


