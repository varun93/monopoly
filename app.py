from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
	state = {}
	return render_template('index.html', state=state)
