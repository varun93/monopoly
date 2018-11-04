from agent import Agent
from utils import combineStates


class Adjudicator:
	
	def __init__(self):
		self.state =  {
			"turn" : 0,
		    "property_status" : [
		        (1, -1),
		        (12, 3),
		    ],
		    "position" : (1,5),#can take values from -1 to 40,
		    "current_cash" : (20,30), #0 to infinity
		    "current_phase" : "Please complete this this"
		}

		self.agentOne = Agent(self.state)
		self.agentTwo = Agent(self.state)
		

	def runPlayerOnState(self):
		
		actionAgentOne = agent.run(state)
		actionAgentTwo = agent.run(state)

