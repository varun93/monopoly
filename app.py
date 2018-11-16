from flask import Flask, render_template
from flask_socketio import SocketIO
from agent import Agent
from adjudicator import Adjudicator
import json

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)


def background_thread():
	adjudicator = Adjudicator(Agent,Agent,socketio)
	adjudicator.runGame()

@app.route('/')
def index():
	socketio.start_background_task(target=background_thread)
	return render_template('index.html')



if __name__ == '__main__':
	socketio.run(app, debug=True)

