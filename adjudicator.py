from config import log
import dice
import constants
from cards import Cards
from agent import Agent
import copy
import timeout_decorator
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
	""" Special json encoder for numpy types """
	def default(self, obj):
		if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
			np.int16, np.int32, np.int64, np.uint8,
			np.uint16, np.uint32, np.uint64)):
			return int(obj)
		elif isinstance(obj, (np.float_, np.float16, np.float32, 
			np.float64)):
			return float(obj)
		elif isinstance(obj,(np.ndarray,)): #### This is the fix
			return obj.tolist()


		return json.JSONEncoder.default(self, obj)

# make sure the state is not mutated
class Adjudicator:
	
	def __init__(self,AgentOne,AgentTwo,socket=None):
		
		num_properties = len(constants.space_to_property_map) + 2
		self.socket = socket
		self.state =  [
			0, #player turn; 0
			[0]*30, #player properties; 1
			[0,0],#player's position; 2
			[1500,1500], #player's cash; 3
			0, #phase number; 4
			{}, #phase payload; 5
		]
	
		self.TOTAL_NO_OF_TURNS = 50
		self.DiceClass = dice.Dice

		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5
		
		self.CHANCE_GET_OUT_OF_JAIL_FREE = 28
		self.COMMUNITY_GET_OUT_OF_JAIL_FREE = 29
		
		self.BOARD_SIZE = 40
		self.PASSING_GO_MONEY = 200
		
		"""
		Phases
		Initial Idea:
		self.INITIAL_BSTM = 0
		self.TRADE_OFFER = 1
		self.PRETURN_BSTM = 2
		self.DICE_ROLL = 3
		self.BUYING = 4
		self.AUCTION = 5
		self.PAYMENT = 6
		self.JAIL = 7
		self.CHANCE_CARD = 8
		self.COMMUNITY_CHEST_CARD = 9 
		self.POSTTURN_BSTM = 10
		"""
		self.BSTM = 0
		self.TRADE_OFFER = 1
		self.DICE_ROLL = 2
		self.BUYING = 3
		self.AUCTION = 4
		self.PAYMENT = 5
		self.JAIL = 6
		self.CHANCE_CARD = 7
		self.COMMUNITY_CHEST_CARD = 8
		"""
		Phase Payload Description:
		Buying Phase:
		{'property': 6, 'cash': 100, 'source': 'bank'}
		BSTM:
		{'source': 'opponent', 'cash': 4}
		
		"""
		

		self.agentOne = AgentOne(self.state)
		self.agentTwo = AgentTwo(self.state)
		self.dice = None
		self.chest = Cards(constants.communityChestCards)
		self.chance = Cards(constants.chanceCards)
		
	def notifyUI(self):
		send = copy.deepcopy(self.state)
		send = json.dumps(send, cls=NumpyEncoder)
		self.socket.emit('game_state_updated', {'state': json.loads(send) } )
			

	def conductBSTM(self,state=[]):

		state = state or self.state

		# might move these as class methods at a later point
		def getPropertyStatus(state,propertyId):
			mappingId = constants.space_to_property_map[propertyId]
			return state[self.PROPERTY_STATUS_INDEX][mappingId]
		
		def updatePropertyStatus(state,propertyId,propertyStatus):
			mappingId = constants.space_to_property_map[propertyId]
			state[self.PROPERTY_STATUS_INDEX][mappingId] = propertyStatus
		
		def getCurrentPlayer(state):
			#turn = state[self.PLAYER_TURN_INDEX] % 2
			
			#if turn == 0:
			#	return 1
			#else:
			#	return 2
			return state[self.PHASE_PAYLOAD_INDEX]['id']+1
	
		def getPlayerCash(state,player):
			return state[self.PLAYER_CASH_INDEX][player-1]
	
		# handleBMST
		#currentPlayer = getCurrentPlayer(state)
			
		def rightOwner(propertyStatus, player):
			if player == 1 and propertyStatus <= 0:
				return False
			if player == 2 and propertyStatus  >= 0:
				return False

			return True

		def hasBuyingCapability(currentPlayer, properties):
			playerCash = getPlayerCash(state, currentPlayer)
			for propertyObject in properties:
				(propertyId,constructions) = propertyObject
				space = constants.board[propertyId]
				playerCash -= space['build_cost']*constructions
				if playerCash < 0:
					break

			return playerCash >= 0
				
		def validBuyingSequence(currentPlayer, properties):

			for propertyObject in properties:

				(propertyId,constructions) = propertyObject
				propertyStatus = getPropertyStatus(state, propertyId)

				if propertyStatus == 7 or propertyStatus == -7 or propertyStatus == 0:
					return False

				if constructions < 0 or constructions > 5:
					return False

				if not rightOwner(propertyStatus, currentPlayer):
					return False

				currentConstructionsOnProperty = abs(propertyStatus) - 1 

				if (currentConstructionsOnProperty + constructions) > 5:
					return False

			return True

		# house can be built only if you own a monopoly of colours 
		# double house can be built only if I have built one house in each colour 
		# order of the tuples to be taken into account
		def handleBuy(properties):
			currentPlayer = getCurrentPlayer(state)
			propertyConstructionSites = list(map(lambda x : x[0],filter(lambda x : x[1] > 0, properties)))

			# determine if the agent actually has the cash to buy all this?
			# only then proceed; important for a future sceanrio
			if not hasBuyingCapability(currentPlayer, properties):
				return

			if not validBuyingSequence(currentPlayer,properties):
				return

			# ordering of this tuple becomes important  
			for propertyObject in properties:

				(propertyId,constructions) = propertyObject
				space = constants.board[propertyId]
				groupElements = space['monopoly_group_elements']
				playerCash = getPlayerCash(state, currentPlayer)
				propertyStatus = getPropertyStatus(state, propertyId)
				currentConstructionsOnProperty = abs(propertyStatus) - 1 

				if constructions and constructions > 0:
					# does the agent own the all spaces in the group?
					for groupElement in groupElements:
						groupElementPropertyStatus = getPropertyStatus(state,groupElement) 
						if currentPlayer == 1 and groupElementPropertyStatus < 1:
					 		return
						if currentPlayer == 2 and groupElementPropertyStatus > -1:
					 		return

					# if the player wishes to construct more than a single house 
					if constructions > 1 and currentConstructionsOnProperty < 2:

						missingElementsInGroup = []
							
						for groupElement in groupElements:
							groupElementPropertyStatus = getPropertyStatus(state,groupElement) 
							if currentPlayer == 1 and (groupElementPropertyStatus == 1 or groupElementPropertyStatus == 7):
								missingElementsInGroup.append(groupElement)
							
							if currentPlayer == 2 and (groupElementPropertyStatus == -1 or groupElementPropertyStatus == -7):
								missingElementsInGroup.append(groupElement)

						# not a convincing logic but the best I could think of
						# examine the tuples if he wants to buy 
						for groupElement in missingElementsInGroup:
							if groupElement not in propertyConstructionSites:
								return


					playerCash -= space['build_cost']*constructions
					
					if playerCash >= 0:

						propertyStatus = constructions + currentConstructionsOnProperty + 1
						
						if currentPlayer == 2:
							propertyStatus *= -1

						updatePropertyStatus(state,propertyId,propertyStatus)
						state[self.PLAYER_CASH_INDEX][currentPlayer-1] = playerCash

					else:
						return

		def handleSell(properties):
			currentPlayer = getCurrentPlayer(state)
			for propertyObject in properties:

				(propertyId,constructions) = propertyObject
				space = constants.board[propertyId]
				playerCash = getPlayerCash(state, currentPlayer)
				propertyStatus = getPropertyStatus(state,propertyId)
				
				if constructions == 0:
					return
				
				if not rightOwner(propertyStatus,currentPlayer):
					return

				houseCount = abs(propertyStatus) - 1
				
				if houseCount < 1 or constructions > houseCount:
					return

				houseCount -= constructions 
				playerCash += (space['build_cost']*0.5*constructions)

				propertyStatus = houseCount + 1

				if currentPlayer == 2:
					propertyStatus *= -1

				updatePropertyStatus(state,propertyId,propertyStatus)
				state[self.PLAYER_CASH_INDEX][currentPlayer-1] = playerCash
				
				#First subtract what you can from the player debt.
				#self.handle_payment(state)
	
		# agent mortages a particular property
		# agent gets 50% of original money of the property 
		# penalizing the agent by selling the property with constructions too;
		# its a negligence on the part of the agent 
		def handleMortgage(properties):
			currentPlayer = getCurrentPlayer(state)
			for propertyId in properties:
				space = constants.board[propertyId]
				playerCash = getPlayerCash(state, currentPlayer)
				propertyStatus = getPropertyStatus(state,propertyId)
				
				propertyPrice = space['price']
				mortagePrice = propertyPrice/2
				
				if not rightOwner(propertyStatus,currentPlayer):
					return

				if propertyStatus in [-7,7]:
					propertyStatus = 1

					if currentPlayer == 2:
						propertyStatus *= -1

					unmortgagePrice = mortagePrice + mortagePrice*0.1

					if playerCash >= unmortgagePrice:
						playerCash -= unmortgagePrice 
					else:
						return
				else:
					playerCash += mortagePrice
					propertyStatus = 7

					if currentPlayer == 2:
						propertyStatus *= -1
				
				updatePropertyStatus(state,propertyId,propertyStatus)
				state[self.PLAYER_CASH_INDEX][currentPlayer-1] = playerCash
				#First subtract what you can from the player debt.
				#self.handle_payment(state)


		def handleTrade(cashOffer,propertiesOffer,cashRequest,propertiesRequest):
			currentPlayer = getCurrentPlayer(state)
			cashRequest = cashRequest or 0
			cashOffer = cashOffer or 0

			# very clumsy; we understand
			otherPlayer = list(set([1,2]) - set([currentPlayer]))[0]
			
			currentPlayerCash = getPlayerCash(state,currentPlayer)
			otherPlayerCash = getPlayerCash(state,otherPlayer)

			if cashOffer > currentPlayerCash:
				return

			if cashRequest > otherPlayerCash:
				return

			for propertyOffer in propertiesOffer:
				propertyStatus = getPropertyStatus(state,propertyOffer)
				if not rightOwner(propertyStatus,currentPlayer):
					return


			# check if the other agent actually cash and properties to offer
			for propertyRequest in propertiesRequest:
				propertyStatus = getPropertyStatus(state,propertyRequest)
				if not rightOwner(propertyStatus,otherPlayer):
					return

			# update the values in the payload index 
			state[self.PHASE_NUMBER_INDEX] = self.TRADE_OFFER
			phasePayload = state[self.PHASE_PAYLOAD_INDEX]
			
			if not phasePayload:
				phasePayload = {}

			phasePayload['cashOffer'] = cashOffer 
			phasePayload['propertiesOffer'] = propertiesOffer 
			phasePayload['cashRequest'] = cashRequest 
			phasePayload['propertiesRequest'] = propertiesRequest

			state[self.PHASE_PAYLOAD_INDEX] = phasePayload

			tradeResponse = False

			if currentPlayer == 1:
				tradeResponse = self.runPlayerOnStateWithTimeout(self.agentTwo,state)
			else:
				tradeResponse = self.runPlayerOnStateWithTimeout(self.agentOne,state)

			# if the trade was successful update the cash and property status
			if tradeResponse:

				currentPlayerCash += (cashRequest - cashOffer)
				otherPlayerCash += (cashOffer - cashRequest)
				
				state[self.PLAYER_CASH_INDEX][currentPlayer-1] = currentPlayerCash 
				state[self.PLAYER_CASH_INDEX][otherPlayer-1] = otherPlayerCash

				for propertyOffer in propertiesOffer:
					propertyStatus = getPropertyStatus(state,propertyOffer) 
					updatePropertyStatus(state,propertyOffer,propertyStatus*-1)

				for propertyRequest in propertiesRequest:
					propertyStatus = getPropertyStatus(state,propertyRequest)
					updatePropertyStatus(state,propertyRequest,propertyStatus*-1)
			
			#Receive State
			phasePayload['tradeResponse'] = tradeResponse
			phasePayload['receiveState'] = True
			state[self.PHASE_PAYLOAD_INDEX] = phasePayload
			if currentPlayer == 1:
				self.runPlayerOnStateWithTimeout(self.agentOne,state)
			else:
				self.runPlayerOnStateWithTimeout(self.agentTwo,state)

		def takeBMSTAction(action):

			intent = action[0]
			
			if intent == "B":
				handleBuy(action[1])

			elif intent == "S":
				handleSell(action[1])
			
			elif intent == "M":
				handleMortgage(action[1])

			elif intent == "T":
				handleTrade(action[1],action[2],action[3],action[4])

		# TODO:merging of states; and hiding the bmst decison of first agent to the second
		previousPhaseNumber = state[self.PHASE_NUMBER_INDEX]
		while True:
			
			state[self.PHASE_NUMBER_INDEX] = self.BSTM
			state[self.PHASE_PAYLOAD_INDEX]['id'] = 0
			
			bstmActionAgentOne = self.runPlayerOnStateWithTimeout(self.agentOne,state)
		
			if bstmActionAgentOne is not None:
				takeBMSTAction(bstmActionAgentOne)
			
			state[self.PHASE_PAYLOAD_INDEX]['id'] = 1
			
			bstmActionAgentTwo = self.runPlayerOnStateWithTimeout(self.agentTwo,state)

			if bstmActionAgentTwo is not None:
				takeBMSTAction(bstmActionAgentTwo)
			
			"""
			Both players must be done with their BSTM
			"""
			if (bstmActionAgentOne is None) and (bstmActionAgentTwo is None):
				#Counter against case where we fall on an idle position and do BSTM.
				#The previous phase would be dice roll. But it doesn't make sense to set that back.
				if previousPhaseNumber > self.DICE_ROLL:
					state[self.PHASE_NUMBER_INDEX] = previousPhaseNumber
				
				state[self.PHASE_PAYLOAD_INDEX].pop('id',None)
				break
		
		
	def send_player_to_jail(self,state):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		
		log("jail","Player "+str(current_player)+" has been sent to jail")
		
		state[self.PLAYER_POSITION_INDEX][current_player] = -1 #sending the player to jail
		state[self.PHASE_NUMBER_INDEX] = self.JAIL
	
	def update_turn(self,state):
		state[self.PLAYER_TURN_INDEX] += 1
	
	""" ACTION METHODS """
	
	"""Scenario where current player is in jail at the start of the turn.
	Processes the response to the agent.jailDecision function."""
	"""
	Incoming action format:
	("R") : represents rolling to get out
    ("P") : represents paying $50 to get out (BSMT should follow)
    ("C", propertyNumber) : represents using a get out of jail card, 
    but in case someone has both, needs to specify which one they are using. 
    In general, should always specify the number (either 28 or 29)
	Return values:
	List of 2 boolean values:
	1. Whether the player is out of jail.
	2. Whether there was a dice throw while handling jail state.
	"""
	def handle_in_jail_state(self,state,action):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		if action[0] == 'P':
			"""
			Should there be a BSTM here?
			Assuming player has the money
			"""
			playerCash = state[self.PLAYER_CASH_INDEX][current_player]
			if playerCash >= 50:
				playerCash -= 50
				state[self.PLAYER_CASH_INDEX][current_player] = playerCash
				return [True,False]
		
		elif action[0] == 'C':
			#Check if the player has the mentioned property card.
			if (len(action)>1) & (action[1] in [28,29]):
				if current_player == 0:
					owned = (action[1] < 0)
				else:
					owned = (action[1] > 0)
				
				if owned:
					if action[1] == self.COMMUNITY_GET_OUT_OF_JAIL_FREE:
						state[self.PROPERTY_STATUS_INDEX][ action[1] ] = 0
						self.chest.deck.append(constants.communityChestCards[4])
						return [True,False]
					
					elif action[1] == self.CHANCE_GET_OUT_OF_JAIL_FREE:
						
						state[self.PROPERTY_STATUS_INDEX][ action[1] ] = 0
						self.chance.deck.append(constants.chanceCards[7])
						return [True,False]
		
		"""If both the above method fail for some reason, we default to dice roll."""
		diceThrow = None
		if (self.diceThrows is not None) and len(self.diceThrows)>0:
			diceThrow = self.diceThrows.pop(0)
		self.dice.roll(dice=diceThrow)
		if self.dice.double:
			#Player can go out
			#Need to ensure that there is no second turn for the player in this turn.
			self.dice.double = False
			return [True,True]
		
		return [False,True]

	def parseAction(self):
			pass

	"""To reset dice for a new turn"""
	def pass_dice(self):
		self.dice = self.DiceClass()

	"""
	Method starts a blind auction.
	First turn in the auction goes to the player who didn't start it. Bidding starts at 1. 
	Any lower bid/ failure to bid in time would result in the property going to the other player. 
	NOTE: This function only accepts UNOWNED PROPERTIES. ENSURE THIS IN THE CALLING FUNCTION.
	"""
	def start_auction(self,state):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		
		log("auction","Player "+str(current_player)+" is starting an Auction")
		
		opponent = abs(current_player - 1)
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		
		#Unowned
		state[self.PHASE_NUMBER_INDEX] = self.AUCTION
		state[self.PHASE_PAYLOAD_INDEX] = {}
		#Below mentioned property needed if the auction is not blind
		#state[self.PHASE_PAYLOAD_INDEX]['subphase'] = "start"
		state[self.PHASE_PAYLOAD_INDEX]['property'] = playerPosition
	
	"""
	Accepts the actions of the blind auction from both players and performs it.
	NOTE: The expected type of action is int. If the input is float, it will be typecast.
	If the action is in some other type, following rules will be applied:
		If opponent got the type of action wrong, current player wins.
		else Opponent wins. i.e., opponent would win even if his action has incorrect type
		as long as the current player also made a mistake in the type of his action
	"""	
	def handle_auction(self,state,actionOpponent,actionCurrentPlayer):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		opponent = abs(current_player - 1)
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		propertyMapping = constants.space_to_property_map[playerPosition]
		
		winner = None
		
		try:
			actionCurrentPlayer = int(actionCurrentPlayer)
		except:
			actionCurrentPlayer = None
		try:
			actionOpponent = int(actionOpponent)
		except:
			actionOpponent = None
		
		log("auction","Bids from the players: "+str(actionCurrentPlayer)+","+str(actionOpponent))	
		
		if actionOpponent is not None and actionCurrentPlayer is not None:
			if actionCurrentPlayer > actionOpponent:
				#Current Player wins the auction
				winner = current_player
				winningBid = actionCurrentPlayer
			else:
				#Opponent wins
				winner = opponent
				winningBid = actionOpponent
					
		else:
			if actionCurrentPlayer is not None:
				#Only current player sent a valid response. He wins.
				winner = current_player
				winningBid = actionCurrentPlayer
			elif actionOpponent is not None:
				winner = opponent
				winningBid = actionOpponent
		
		#Winner is None when both Agents send invalid responses
		if winner is not None:
			log("auction","Player "+str(winner)+" won the Auction")
			state[self.PLAYER_CASH_INDEX][winner] -= winningBid
			if winner == 0:
				state[self.PROPERTY_STATUS_INDEX][ propertyMapping ] = 1
			else:
				state[self.PROPERTY_STATUS_INDEX][ propertyMapping ] = -1
			
			#Receive State
			phasePayload = {}
			phasePayload['auctionWinner'] = winner
			phasePayload['receiveState'] = True
			state[self.PHASE_PAYLOAD_INDEX] = phasePayload
			if winner == 1:
				self.runPlayerOnStateWithTimeout(self.agentOne,state)
			else:
				self.runPlayerOnStateWithTimeout(self.agentTwo,state)
		
		#Clearing the payload as the auction has been completed
		state[self.PHASE_PAYLOAD_INDEX] = {}
	
	"""
	Handle the action response from the Agent for buying an unowned property
	"""	
	def handle_buy_property(self,state):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		propertyMapping = constants.space_to_property_map[playerPosition]
		
		if self.handle_payment(state, False):
			if current_player == 0:
				state[self.PROPERTY_STATUS_INDEX][ propertyMapping ] = 1
			else:
				state[self.PROPERTY_STATUS_INDEX][ propertyMapping ] = -1

			log('buy',"Player "+str(current_player)+" has bought "+constants.board[playerPosition]['name'])
			
			#Clearing the payload as the buying has been completed
			state[self.PHASE_PAYLOAD_INDEX] = {}
			return True
		
		#This would indicate going to Auction?
		return False
	
	"""
	Handling payments the player has to make to the bank/opponent
	"""
	def handle_payment(self,state,take=True):
		
		if 'cash' not in state[self.PHASE_PAYLOAD_INDEX]:
			#No payment to be made
			return True
		
		debt = state[self.PHASE_PAYLOAD_INDEX]['cash']
		receiver = state[self.PHASE_PAYLOAD_INDEX]['source']
		
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		opponent = abs(current_player - 1)
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		
		log('pay',"Player "+str(current_player)+" has to pay $"+str(debt)+" to the "+receiver)
		
		if playerCash >= debt:
			state[self.PLAYER_CASH_INDEX][current_player] -= debt
			if receiver == 'opponent':
				state[self.PLAYER_CASH_INDEX][opponent] += debt
				
			#All the debt has been paid
			state[self.PHASE_PAYLOAD_INDEX].pop('cash',None)
			state[self.PHASE_PAYLOAD_INDEX].pop('source',None)
			return True
		elif take:
			#Take what you can get from the indebted
			if receiver == 'opponent':
				state[self.PLAYER_CASH_INDEX][opponent] += playerCash
			state[self.PLAYER_CASH_INDEX][current_player] = 0
			
			#Update with only the remaining debt
			state[self.PHASE_PAYLOAD_INDEX]['cash'] = (debt - playerCash)
		
		return False
	
	"""
	(Q: Will there need to be a BSTM if the player receives money?)
	Phase Properties:
	Is the property owned?
	If unowned, there are 3 sequential sub-phases: BSTM,Buying,Auction. Which one are you in?
	If owned, 2 sub-phases: BSTM,rent. Note: BSTM here for opponent must be applied after the turn.
	If cards, draw top card,do effect, return it to bottom of the deck.
	If Go To Jail, send to jail. Immediately end the turn.
	If currently in Jail, 3 ways to get out.
	"""
	
	"""
	Dice Roll Function
	1. Checks if player is currently in Jail and handles separately if that is the case.
	2. else, rolls the dice, checks for all the dice events.
	3. Then moves the player to new position and finds out what the effect of the position is.
	"""
	def dice_roll(self,state,player):
		
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		
		outOfJail = True #If the player is currently not in jail
		diceThrown = False # Represents if the dice has already been thrown for the turn.
		
		#Jail
		if playerPosition == -1:
			state[self.PHASE_NUMBER_INDEX] = self.JAIL
			state[self.PHASE_PAYLOAD_INDEX] = {}
			action = self.runPlayerOnStateWithTimeout(player,state)
			[outOfJail,diceThrown] = self.handle_in_jail_state(state,action)
		
		if not diceThrown:
			diceThrow = None
			if (self.diceThrows is not None) and len(self.diceThrows)>0:
				diceThrow = self.diceThrows.pop(0)
			self.dice.roll(dice=diceThrow)
			
		"""
		We need to call agent.receiveState and pass on the dice roll for the turn.
		There could be a couple of scenarios:
		1. Player rolls non-doubles
		2. Player rolls doubles.
		3. Player rolls doubles while in Jail.
		4. Player rolls non-doubles while in Jail.
		5. Player rolls doubles for 3 third time in a row in a single turn.
		"""
		state[self.PHASE_NUMBER_INDEX] = self.DICE_ROLL
		state[self.PHASE_PAYLOAD_INDEX] = {}
		state[self.PHASE_PAYLOAD_INDEX]['dice_1'] = self.dice.die_1
		state[self.PHASE_PAYLOAD_INDEX]['dice_2'] = self.dice.die_2
		state[self.PHASE_PAYLOAD_INDEX]['inJail'] = outOfJail #Implies player will not move this turn.
		state[self.PHASE_PAYLOAD_INDEX]['anotherChance'] = self.dice.double #Implies player gets another round in the same turn.
		state[self.PHASE_PAYLOAD_INDEX]['receiveState'] = True
		self.runPlayerOnStateWithTimeout(player,state)
		
		"""If the player is still in Jail, end turn immediately."""
		if not outOfJail:
			return False
		
		if self.dice.double_counter == 3:
			self.send_player_to_jail(state)
			return False
			#End current player's turn here
			#Should there be a GoToJail state to let the player know?
		else:
			#Update player position
			
			playerPosition += (self.dice.die_1 + self.dice.die_2)
			
			#Passing Go
			if playerPosition>=self.BOARD_SIZE:

				playerPosition = playerPosition % self.BOARD_SIZE
				playerCash += self.PASSING_GO_MONEY
			
			#Next, perform square effect
			#Preparation for next phase:
			state[self.PLAYER_POSITION_INDEX][current_player] = playerPosition
			state[self.PLAYER_CASH_INDEX][current_player] = playerCash

			self.determine_position_effect(state,player)
			
			if state[self.PHASE_NUMBER_INDEX] == self.JAIL:
				return False
			else:
				return True
	
	def isPositionProperty(self,position):
		return (constants.board[position]['class'] == 'Street') or (constants.board[position]['class'] == 'Railroad') or (constants.board[position]['class'] == 'Utility')
	
	"""
	Performed after dice is rolled and the player is moved to a new position.
	Determines the effect of the position and action required from the player.
	"""		
	def determine_position_effect(self,state,player):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		
		isProperty = self.isPositionProperty(playerPosition)
		
		state[self.PHASE_PAYLOAD_INDEX] = {} # Should this be done? Clearing of phase payload/properties?
			
		if isProperty:
			output = self.handle_property(state)
			if 'phase' in output:
				state[self.PHASE_NUMBER_INDEX] = output['phase']
			if 'phase_properties' in output:
				state[self.PHASE_PAYLOAD_INDEX] = output['phase_properties']
					
		else:
			if constants.board[playerPosition]['class'] == 'Chance':
				#Chance
				card = self.chance.draw_card()
				
				log("cards","Chance card \""+str(card['content'])+"\" has been drawn")
				
				#ReceiveState
				state[self.PHASE_NUMBER_INDEX] = self.CHANCE_CARD
				state[self.PHASE_PAYLOAD_INDEX] = {}
				state[self.PHASE_PAYLOAD_INDEX]['card_id'] = card['id']
				state[self.PHASE_PAYLOAD_INDEX]['receiveState'] = True
				self.runPlayerOnStateWithTimeout(player,state)
				
				self.handle_cards_pre_turn(state,card,'Chance',player)
				
			elif constants.board[playerPosition]['class'] == 'Chest':
				#Community
				card = self.chest.draw_card()
				
				log("cards","Community Chest card \""+str(card['content'])+"\" has been drawn")
				
				#ReceiveState
				state[self.PHASE_NUMBER_INDEX] = self.COMMUNITY_CHEST_CARD
				state[self.PHASE_PAYLOAD_INDEX] = {}
				state[self.PHASE_PAYLOAD_INDEX]['card_id'] = card['id']
				state[self.PHASE_PAYLOAD_INDEX]['receiveState'] = True
				self.runPlayerOnStateWithTimeout(player,state)
				
				self.handle_cards_pre_turn(state,card,'Chest',player)
			   
			elif constants.board[playerPosition]['class'] == 'Tax':
				#Tax
				state[self.PHASE_NUMBER_INDEX] = self.PAYMENT
				state[self.PHASE_PAYLOAD_INDEX]['cash'] = constants.board[playerPosition]['tax']
				state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
			
			elif constants.board[playerPosition]['class'] == 'Idle':
				#Represents Go,Jail(Visiting),Free Parking
				pass
	
	"""
	Given that the current space is a property, determine what is to be done here.
	"""
	def handle_property(self,state):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		
		#Could add a check here for whether this is a property. If not there will be an error here.
		propertyValue = state[self.PROPERTY_STATUS_INDEX][ constants.space_to_property_map[playerPosition] ]
		output = {}
		if propertyValue == 0:
			#Unowned
			output['phase'] = self.BUYING
			output['phase_properties'] = {}
			output['phase_properties']['cash'] = constants.board[playerPosition]['price']
			output['phase_properties']['source'] = "bank"
			output['phase_properties']['property'] = playerPosition
		else:
			#Check if owned by opponent
			if current_player == 0:
				owned = (propertyValue < 0)
			else:
				owned = (propertyValue > 0)
			
			if owned:
				rent = 0
				absPropertyValue = abs(propertyValue)
				
				if absPropertyValue == 1:
					rent = constants.board[playerPosition]['rent']
					monopolies = constants.board[playerPosition]['monopoly_group_elements']
					sign = propertyValue/absPropertyValue
					
					counter = 1
					for monopoly in monopolies:
						monopoly_sign = state[self.PROPERTY_STATUS_INDEX][constants.space_to_property_map[monopoly]]
						if monopoly_sign!=0 and monopoly_sign/abs(monopoly_sign) == sign:
							counter += 1
					
					if (constants.board[playerPosition]['class'] == 'Street'):
						if (counter==len(monopolies)+1):
							rent = rent * 2
					elif (constants.board[playerPosition]['class'] == 'Railroad'):
						rent = rent * counter
					elif (constants.board[playerPosition]['class'] == 'Utility'):
						if (counter==len(monopolies)+1):
							rent = 10
						rent = rent * (self.dice.die_1 + self.dice.die_2)
				
				elif absPropertyValue == 2:
					rent = constants.board[playerPosition]['rent_house_1']
				elif absPropertyValue == 3:
					rent = constants.board[playerPosition]['rent_house_2']
				elif absPropertyValue == 4:
					rent = constants.board[playerPosition]['rent_house_3']
				elif absPropertyValue == 5:
					rent = constants.board[playerPosition]['rent_house_4']
				elif absPropertyValue == 6:
					rent = constants.board[playerPosition]['rent_hotel']
				
				output['phase'] = self.PAYMENT
				output['phase_properties'] = {}
				output['phase_properties']['cash'] = rent
				output['phase_properties']['source'] = "opponent"
			
			else:
				#When the property is owned by us
				pass
		
		return output
				
	
	"""
	Method handles various events for Chance and Community cards
	"""
	def handle_cards_pre_turn(self,state,card,deck,player):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		updateState = False

		state[self.PHASE_PAYLOAD_INDEX] = {}
		
		if card['type'] == 1:
			#What should we do if we are receiving cash here? Should there be a BSTM?
			if card['money']<0:
				state[self.PHASE_NUMBER_INDEX] = self.PAYMENT
				state[self.PHASE_PAYLOAD_INDEX]['cash'] = abs(card['money'])
				state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
			else:
				playerCash += abs(card['money'])

		elif card['type'] == 2:
			#-ve represents you need to pay
			state[self.PHASE_NUMBER_INDEX] = self.PAYMENT
			state[self.PHASE_PAYLOAD_INDEX]['cash'] = card['money']
			state[self.PHASE_PAYLOAD_INDEX]['source'] = "opponent"
			
		elif card['type'] == 3:
			if card['position'] == -1:
				#sending the player to jail
				playerPosition = -1
				self.send_player_to_jail(state)
			else:
				if (card['position'] - 1) < playerPosition:
					#Passes Go
					playerCash += self.PASSING_GO_MONEY
				playerPosition = card['position'] - 1
				updateState = True
				
				
		elif card['type'] == 4:
			"""Get out of Jail free"""
			if deck == 'Chest':
				propertyValue = self.COMMUNITY_GET_OUT_OF_JAIL_FREE
			else:
				propertyValue = self.CHANCE_GET_OUT_OF_JAIL_FREE
			
			if current_player == 0:
				state[self.PROPERTY_STATUS_INDEX][propertyValue] = 1
			else:
				state[self.PROPERTY_STATUS_INDEX][propertyValue] = -1
				
		elif card['type'] == 5:
			n_houses = 0
			n_hotels = 0
			if current_player == 0:
				#first player
				for prop in state[self.PROPERTY_STATUS_INDEX]:
					if prop in range(2,6):
						n_houses+= (prop-1)
					if prop == 6:
						n_hotels+= 1
			else:
				#second player
				for prop in state[self.PROPERTY_STATUS_INDEX]:
					if prop in range(-5,-1):
						n_houses+= (abs(prop)-1)
					if prop == -6:
						n_hotels+= 1
			rent = abs(card['money'])*n_houses + abs(card['money2'])*n_hotels
			if rent > 0:
				state[self.PHASE_NUMBER_INDEX] = self.PAYMENT
				state[self.PHASE_PAYLOAD_INDEX]['cash'] = rent
				state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
		
		elif card['type'] == 6:
			#Advance to nearest railroad. Pay 2x amount if owned
			railroads = [i for i in range(len(constants.board)-1) if constants.board[i]['class']=='Railroad']
			if (playerPosition < 5) or (playerPosition>=35):
				if (playerPosition>=35):
					#Passes Go
					playerCash += self.PASSING_GO_MONEY
				playerPosition = 5
			elif (playerPosition < 15) and (playerPosition>=5):
				playerPosition = 15
			elif (playerPosition < 25) and (playerPosition>=15):
				playerPosition = 25
			elif (playerPosition < 35) and (playerPosition>=25):
				playerPosition = 35
			
			state[self.PLAYER_POSITION_INDEX][current_player] = playerPosition
			state[self.PLAYER_CASH_INDEX][current_player] = playerCash
			# 
			output = self.handle_property(state)
			if 'phase' in output:
				state[self.PHASE_NUMBER_INDEX] = output['phase']
			if 'phase_properties' in output:
				state[self.PHASE_PAYLOAD_INDEX] = output['phase_properties']
			
			#We need to double rent if the player landed on opponent's property.
			#We could fall on our own property in which case there is no source payload attribute
			if ('source'in state[self.PHASE_PAYLOAD_INDEX]) and (state[self.PHASE_PAYLOAD_INDEX]['source'] == 'opponent'):
				state[self.PHASE_PAYLOAD_INDEX]['cash'] *= 2
		
		elif card['type'] == 7:
			#Advance to nearest utility. Pay 10x dice roll if owned
			utilities = [i for i in range(len(constants.board)-1) if constants.board[i]['class']=='Utility']
			if (playerPosition < 12) or (playerPosition>=28):
				if (playerPosition>=28):
					#Passes Go
					playerCash += self.PASSING_GO_MONEY
				playerPosition = 12
			elif (playerPosition < 28) and (playerPosition>=12):
				playerPosition = 28
			
				propertyValue = state[self.PROPERTY_STATUS_INDEX][ constants.space_to_property_map[playerPosition] ]
				if propertyValue == 0:
					#Unowned
					state[self.PHASE_NUMBER_INDEX] = self.BUYING
					state[self.PHASE_PAYLOAD_INDEX]['cash'] = constants.board[playerPosition]['price']
					state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
					state[self.PHASE_PAYLOAD_INDEX]['property'] = playerPosition
				else:
					#Check if owned by opponent
					if current_player == 0:
						owned = (propertyValue < 0)
					else:
						owned = (propertyValue > 0)
					
					if owned:
						absPropertyValue = abs(propertyValue)
						#This point is up for contention.
						#The rules of the card if taken literally state that you would need to pay even if the property is mortgaged.
						#But, not considering that as it doesn't seem to be in the spirit of the game.
						if absPropertyValue == 1:
							diceThrow = None
							if (self.diceThrows is not None) and len(self.diceThrows)>0:
								diceThrow = self.diceThrows.pop(0)
							self.dice.roll(ignore=True,dice=diceThrow)
							
							state[self.PHASE_NUMBER_INDEX] = self.PAYMENT
							state[self.PHASE_PAYLOAD_INDEX]['cash'] = 10 * (self.dice.die_1 + self.dice.die_2)
							state[self.PHASE_PAYLOAD_INDEX]['source'] = "opponent"
		
		elif card['type'] == 8:
			#Go back 3 spaces
			playerPosition -= 3 
			updateState = True
			# state[self.PLAYER_POSITION_INDEX][current_player] -= 3
			# playerPosition = -5
			# self.determine_position_effect(state,player)
		else:
			logger.info('Invalid card type {type}...'.format(type=card['type']))


		# update the player positon and cash and call determine_position_effect and property here?
		#Countermeasure against card type 8 code right above
		state[self.PLAYER_POSITION_INDEX][current_player] = playerPosition
		state[self.PLAYER_CASH_INDEX][current_player] = playerCash
		# make further calls
		if updateState:
			self.determine_position_effect(state,player)
	
	"""Function calls the relevant method of the Agent"""
	def turn_effect(self,state,current_player,opponent):
		phase = state[self.PHASE_NUMBER_INDEX]
		if phase == self.BUYING:
			action = self.runPlayerOnStateWithTimeout(current_player,state)
			if action:
				if self.handle_buy_property(state):
					return True
			
			#Auction
			self.start_auction(state)
			actionOpponent = self.runPlayerOnStateWithTimeout(opponent,state)
			actionCurrentPlayer = self.runPlayerOnStateWithTimeout(current_player,state)
			self.handle_auction(state,actionOpponent,actionCurrentPlayer)
			return True
			
		if phase == self.PAYMENT:
			return self.handle_payment(state)
		
		return True
	
	"""
	On final winner calculation, following are considered:
	Player's cash,
	Property value as on the title card,
	House and Hotel purchase value,
	Mortgaged properties at half price.
	"""
	def final_winning_condition(self,state):
		agentOneCash = state[self.PLAYER_CASH_INDEX][0]
		agentTwoCash = state[self.PLAYER_CASH_INDEX][1]
		agentOnePropertyWorth = 0
		agentTwoPropertyWorth = 0
		
		for i in constants.property_to_space_map:
			#In 0 to 39 board position range
			propertyValue =  state[self.PROPERTY_STATUS_INDEX][i]
			propertyPosition = constants.board[ constants.property_to_space_map[ i ] ]
			
			if propertyValue in range(-6,0):
				agentTwoPropertyWorth += (propertyPosition['price'] + ( (abs(propertyValue)-1)*propertyPosition['build_cost'] ) )
			elif propertyValue == -7:
				agentTwoPropertyWorth += (propertyPosition['price']/2)
			elif propertyValue in range(1,7):
				agentOnePropertyWorth += (propertyPosition['price'] + ( (propertyValue-1)*propertyPosition['build_cost'] ) )
			elif propertyValue == 7:
				agentOnePropertyWorth += (propertyPosition['price']/2)
		
		if state[self.PROPERTY_STATUS_INDEX][28] == -1:
			agentTwoPropertyWorth += 50
		elif state[self.PROPERTY_STATUS_INDEX][28] == 1:
			agentOnePropertyWorth += 50
		
		if state[self.PROPERTY_STATUS_INDEX][29] == -1:
			agentTwoPropertyWorth += 50
		elif state[self.PROPERTY_STATUS_INDEX][29] == 1:
			agentOnePropertyWorth += 50
		
		log("win_condition","AgentOne Cash: "+str(agentOneCash))
		log("win_condition","AgentOne Property Value: "+str(agentOnePropertyWorth))
		log("win_condition","AgentTwo Cash: "+str(agentTwoCash))
		log("win_condition","AgentTwo Property Value: "+str(agentTwoPropertyWorth))
		
		if ( (agentOneCash+agentOnePropertyWorth) > (agentTwoCash+agentTwoPropertyWorth) ):
			return 0
		elif ( (agentOneCash+agentOnePropertyWorth) < (agentTwoCash+agentTwoPropertyWorth) ):
			return 1
		else:
			#Tie
			return 2
	
	def initialize_debug_state(self,diceThrows,chanceCards,communityCards):
		if isinstance(diceThrows, list) and len(diceThrows)>0:
			self.diceThrows = diceThrows
		else:
			self.diceThrows = diceThrows
			
		if isinstance(chanceCards, list) and len(chanceCards)>0:
			self.chance.reinit(constants.chanceCards,chanceCards)
		
		if isinstance(communityCards, list) and len(communityCards)>0:
			self.chest.reinit(constants.communityChestCards,communityCards)
			
	def broadcastState(self,state):
		pass
	
	"""
	Function to be called to start the game.
	First turn or Turn 0 goes to AgentOne.
	"""
	def runGame(self,diceThrows=None,chanceCards=None,communityCards=None):
		
		#Setting an initial state. Used during testing.
		#if isinstance(state,list) and len(state)==6:
		#	self.state = state
		self.initialize_debug_state(diceThrows,chanceCards,communityCards)
		
		winner = None
			
		while (self.state[self.PLAYER_TURN_INDEX] < self.TOTAL_NO_OF_TURNS) and ( (self.diceThrows is None) or (len(self.diceThrows)>0) ):
			
			log("turn","Turn "+str(self.state[self.PLAYER_TURN_INDEX])+" start")
			
			#Temporary measure to clear phase payload
			self.state[self.PHASE_PAYLOAD_INDEX] = {}
			
			#Storing the state at the start of the turn
			constants.state_history.append(copy.deepcopy(self.state))
			
			"""BSTM"""
			self.conductBSTM(self.state)

			"""Determining whose turn it is"""
			current_player = self.agentOne
			opponent = self.agentTwo
			if (self.state[self.PLAYER_TURN_INDEX] % 2) == 1:
				current_player = self.agentTwo
				opponent = self.agentOne
		
			"""Resets dice roll before each turn"""
			self.pass_dice()
			
			log("state","Turn "+str(self.state[self.PLAYER_TURN_INDEX]))
			log("state","State at the start of the turn:")
			log("state",self.state)
			
			while True:
				
				"""rolls dice, moves the player and determines what happens on the space he has fallen on."""
				notInJail = self.dice_roll(self.state,current_player)
				
				if notInJail:
					
					log("state","State after moving the player position and updating state with effect of the position:")
					log("state",self.state)
					
					"""BSTM"""
					self.conductBSTM(self.state)
					
					"""State now contain info about the position the player landed on"""
					"""Performing the actual effect of the current position"""
					if not self.turn_effect(self.state,current_player,opponent):
						current_playerIndex = self.state[self.PLAYER_TURN_INDEX] % 2
						opponentIndex = abs(current_playerIndex - 1)
						winner = opponentIndex
						break
				
				"""BSTM"""
				self.conductBSTM(self.state)
				
				log("state","State at the end of the turn:")
				log("state",self.state)
				
				if (not self.dice.double):
					break
				else:
					log("dice","Rolled Doubles. Play again.")
			
			#Storing the state at the end of the turn
			constants.state_history.append(copy.deepcopy(self.state))
			# notify UI about the state change
			self.notifyUI()
			
			log("turn","Turn "+str(self.state[self.PLAYER_TURN_INDEX])+" end")
			
			"""Update the turn counter"""
			self.update_turn(self.state)
			
			if winner is not None:
				break
		
		#Storing the state_history to log file
		f = open("state_history.log", "w")
		for history in constants.state_history:
			f.write(str(history)+",\n")
		
		"""Determine the winner"""
		if winner==None:
			winner = self.final_winning_condition(self.state)
		
		if winner == 0:
			log("win","AgentOne won the Game.")
		elif winner == 1:
			log("win","AgentTwo won the Game.")
		else:
			log("win","It's a Tie!")
		
		return winner
	
	"""
	This function is called whenever adjudicator needs to communicate with the agent
	The function to called on the agent is determined by reading the state.
	All threading and signal based logic must go in here
	self.INITIAL_BSTM = 0
	self.TRADE_OFFER = 1
	self.PRETURN_BSTM = 2
	self.PAYMENT = 6
	self.POSTTURN_BSTM = 10
	"""

	@timeout_decorator.timeout(3000, timeout_exception=TimeoutError)
	def runPlayerOnStateWithTimeout(self, player,state):
		try:
			return self.runPlayerOnState(player,state)
		except TimeoutError:
			print("Agent Timed Out")
			"""Change the return value here to ensure agent loose"""
			return None


	def runPlayerOnState(self,player,state):
		
		action = None
		
		current_phase = state[self.PHASE_NUMBER_INDEX]
		payload = state[self.PHASE_PAYLOAD_INDEX]
		
		if 'receiveState' in payload:
			state[self.PHASE_PAYLOAD_INDEX].pop('receiveState',None)
			action = player.receiveState(state)
		elif current_phase == self.BSTM:
			action = player.getBMSTDecision(state)
		elif current_phase == self.TRADE_OFFER:
			action = player.respondTrade(state)
		elif current_phase == self.BUYING:
			action = player.buyProperty(state)
		elif current_phase == self.AUCTION:
			action = player.auctionProperty(state)
		elif current_phase == self.PAYMENT:
			pass
		elif current_phase == self.JAIL:
			action = player.jailDecision(state)
		
		return action

#Testing
#adjudicator = Adjudicator(Agent,Agent)
