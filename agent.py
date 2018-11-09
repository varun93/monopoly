import constants

class Agent:
	def __init__(self, id):
		self.id = id
		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5
	
	
	def getBMSTDecision(self, state):
		# TODO:fill the template
		pass
	def respondTrade(self, state):
		pass

	def buyProperty(self, state):
		debt = state[self.PHASE_PAYLOAD_INDEX]['cash']
		receiver = state[self.PHASE_PAYLOAD_INDEX]['source']
		property = constants.board[state[self.PHASE_PAYLOAD_INDEX]['property']]
		
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		
		if playerCash >= debt:
			return True
		else:
			return False
		

	def auctionProperty(self, state):
		pass

	def receiveState(self, state):
		pass

	def parsePhase(self, state):
		phaseNumber = state["phase"]
		phasePayload = state["phase_payload"]

		# how to distinguish between dice roll bmst and bmst before
		if phaseNumber == 0:
			handleBMSTDecison(state)

		if phaseNumber == 3:
			diceValue = phasePayload["dice_roll"]
			currentPosition = state["player_position"][id]
			# is mod 40 correct?
			newPosition = (currentPosition + diceValue) % 40
			propertyStatus = state["property_status"][newPosition]

			# retrieve the property
			handleBMSTDecison(state)

	def jailDecision(self, state):
		pass

	def run(self, state):
		return {}
