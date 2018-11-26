import RL_Agent.Observation as obs
import RL_Agent.neural_network as nn
import RL_Agent.EligibilityTrace as etrace
import random
class RLAgent:

	def __init__(self, id):
		self.id = id
		self.lastState = obs.Observation(None, None, None)
		self.lastAction = 0
		self.traces = []
		self.network = nn.Neural_Network()
		self.currentEpoch = 1
		self.alpha = 0.2
		self.epsilon = 0.5
		self.gamma = 0.95
		self.lamda = 0.8
		self.properties_purchased = [0]*28
		self.mortgaged_properties = [0]*28
		self.buildingsBuilt = [0]*28
		self.inJail = False
		self.isAlive = True
		#self.position = 0 #Don't think this will be used.
		self.money = 0 #Initialize this with the value with agent gets from adjudicator
		self.name = ""

	def getTotalHouses(self):
		counter = 0
		for i in range(0,len(self.buildingsBuilt)):
			if self.buildingsBuilt[i] > 0 and self.buildingsBuilt[i] < 5:
				counter = counter + 1
		return counter

	def getTotalHotels(self):
		counter = 0
		for i in range(0, len(self.buildingsBuilt)):
			if self.buildingsBuilt[i] == 5:
				counter = counter + 1
		return counter

	def setObservation(self, area, position, finance):
		self.Observation = obs.Observation(area, position, finance)

	def addEligibilityTrace(self, trace):
		self.traces.append(trace)

	def agent_start(self, obs):
		self.currentEpoch = self.currentEpoch + 1
		Q_values = self.calculateQValue(obs)

		action = self.e_greedy_selection(Q_values)

		self.lastAction = action
		self.lastState = obs
		trace = etrace.EligibilityTrace(obs, action, 1)
		self.addEligibilityTrace(trace)
		return action


	def updateQtraces(self, obs, action, reward):
		pass


	def Qlearning(self, lastState, lastAction, obs, best_action, reward):
		pass

	def calculateQValue(self, obs):
		#Define Q values for all actions
		#Create input values, run the network, return the calculated Q values.
		return [0.0, 0.0, 0.0]

	def trainNeural(self, input, QValue):
		pass

	def createInput(self, obs, action):
		pass

	def agent_cleanup(self):
		#Save the trained neural network
		pass

	def check_similarity(self, obs1, obs2):
		#Check the similarity between states
		pass

	def agent_step(self, obs, reward):
		action = 0
		Q_values = self.calculateQValue(obs)
		action = self.e_greedy_selection(Q_values)
		exists = self.updateQtraces(obs, action, reward)
		QValue = self.Qlearning(self.lastState, self.lastAction, obs, self.find_max(Q_values), reward)
		self.trainNeural(self.createInput(self.lastState, self.lastAction), QValue)
		if exists == False:
			self.traces.append(etrace.EligibilityTrace(self.lastState, self.lastAction, 1))

		self.lastAction = action
		self.lastState = obs

		return action

	def agent_end(self, reward):
		self.isAlive = False
		self.updateQtraces(self.lastState, self.lastAction, reward)
		self.epsilon *= 0.99
		self.alpha *= 0.99


	def e_greedy_selection(self, Q_values):
		action = 0
		r = random.random()
		if r >= self.epsilon:
			action = self.find_max(Q_values) #Breaking ties randomnly not implemented.
		else:
			action = random.randint(-1,1)
		return action

	def find_max(self, Q_Values):
		return Q_Values.index(max(Q_Values))














