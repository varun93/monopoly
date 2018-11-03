import agent from agent
import combineStates from utils

class Adjudicator:
	
	def __init__(self):
		self.state = {}
		self.agentOne = new Agent(self.state)
		self.agentTwo = new Agent(self.state)
		

	def runPlayerOnState(self):
		actionAgentOne = agent.run(state)
		actionAgentTwo = agent.run(state)

