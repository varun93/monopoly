# Monopoly

Data Science Project CSE 519
Monopoly game playing AI Agent

## Install the Dependencies

```
pip install -r requirements.txt
```

## Run the code

```
export FLASK_APP=app.py
flask run

To run the adjudicator program without the UI implementation, run:
python adjudicator.py

To run testcases, run:
python testcases_x.py to run individual testcases.

To run the entire suite, run:
python testsuite.py

To run the user interface
cd react-user-interface
npm install
npm start

```

## App Structure
The master branch consists of the implementation of the Adjudicator for the monopoly game.

app.py is the controller.  
templates for rendering templates.  
static has all static assets js, css and images.

adjudicator.py:
Consist of the actual implementation of the Adjudicator. The game is started by invoking the method: 

runGame(player1, player2)

This method accepts 2 Agents and runs the game. Over the course of the run, it determines which Agent is the winner.

testcase_x.py:

All files of this format represent test cases that can be independently run to simulate individual flows of the Adjudicator. The testcases may be run over a single game turn or over multiple turns.
The program accepts an Adjudicator and 2 Agents as arguments and checks whether the testcase passes for the simulation run.

testsuite.py
Runs all the testcases as a single suite.

test_functional.py:

Consists of testcases which test the correctness of individual functions. Used to ensure future code changes don't break the expected value from a function.
