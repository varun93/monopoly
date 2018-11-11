# Monopoly

Data Science Project CSE 519

## Install the Dependencies

```
pip install -r requirements.txt
```

## Run the code

```
export FLASK_APP=app.py
flask run
```

## App Structure

app.py is the controller.  
templates for rendering templates.  
static has all static assets js, css and images.

test_adjudicator.py contains the unit test cases for the various functions and scenarios for the adjudicator.
Run this file to see the performance of the adjudicator against each of these test cases.
