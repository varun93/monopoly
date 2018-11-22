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
	agentOne = Agent(1)
	agentTwo = Agent(2)
	adjudicator = Adjudicator(socketio)
	adjudicator.runGame(agentOne,agentTwo)

if __name__ == '__main__':
	socketio.run(app, debug=True)


