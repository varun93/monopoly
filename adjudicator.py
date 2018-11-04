from agent import Agent
from utils import combineStates

class Adjudicator:
	
	def __init__(self):
		self.state = {}
		self.agentOne = Agent(self.state)
		self.agentTwo = Agent(self.state)
		

	def runPlayerOnState(self):
		
		actionAgentOne = agent.run(state)
		actionAgentTwo = agent.run(state)

