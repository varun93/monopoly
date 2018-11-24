import RL_Agent.rl_agent as buddy
import RL_Agent.Obs_Area as Obs_Area
import RL_Agent.Obs_Finance as Obs_Finance
import RL_Agent.Obs_Position as Obs_Position
import RL_Agent.Observation as Observation
"""
For each of the below needs a variable for isTraining if that is true consider that as training phase.

"""
class Agent:
	def __init__(self, id):
		self.id = id
		self.rl_agent = buddy.RLAgent(id)


	def getBMSTDecision(self, state):
		pass

	def respondTrade(self, state):
		return False

	def buyProperty(self, state):
		pass
	def auctionProperty(self, state):
		pass
	def receiveState(self, state):
		pass

	def jailDecision(self, state):
		pass
	def parseDebt(self, state, current_player):
		pass
	def respondMortgage(self, state):
		pass


	"""
	Helper methods to transform states passed by adjudicator to ones expected by RLAgent
	"""
	def playFirstMove(self):
		"""Think about the handling of first move from agent. This is required for Q-learning first step"""
		"""agent_start Method will be called here"""
		pass
	def playGame(self):
		"""Calculate the initial reward, take an action"""
		pass

	def createPosition(self):
		pass

	def createFinance(self):
		pass

	def createArea(self):
		pass

	def calculateReward(self):
		reward = 0
		pass

	def smoothFunction(self, x, factor):
		return (x/factor)/(1 + abs(x/factor))

	def createObs(self):
		position = Obs_Position.Obs_Position(self.createPosition())
		finance = Obs_Finance.Obs_Finance(self.createFinance())
		area = Obs_Area.Obs_Area(self.createArea())
		return Observation.Observation(area, position, finance)
