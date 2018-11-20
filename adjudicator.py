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
			[0]*42, #player properties; 1
			[0,0],#player's position; 2
			[1500,1500], #player's cash; 3
			0, #phase number; 4
			[0,0], #Debt
			(), #phase payload; 5,
			[]
		]
	
		self.TOTAL_NO_OF_TURNS = 50
		self.DiceClass = dice.Dice

		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5
		self.DEBT_INDEX = 6
		self.STATE_HISTORY_INDEX = 7
		
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
		

		self.agentOne = AgentOne(0)
		self.agentTwo = AgentTwo(1)
		self.dice = None
		self.chest = Cards(constants.communityChestCards)
		self.chance = Cards(constants.chanceCards)
		
	def notifyUI(self):
		if self.socket is not None:
			send = copy.deepcopy(self.state)
			send = json.dumps(send, cls=NumpyEncoder)
			self.socket.emit('game_state_updated', {'state': json.loads(send) } )
		
	def updateState(self, state, dimensionOneIndex, dimensionTwoIndex, valueToUpdate):
		if dimensionTwoIndex is None:
			state[dimensionOneIndex] = valueToUpdate
		else:
			state[dimensionOneIndex][dimensionTwoIndex] = valueToUpdate
		
	
	def transformState(self,state):

		transformedState = []

		for element in state:
			if isinstance(element, list):
				transformedState.append(tuple(element))
			elif isinstance(element, dict):
				transformedState.append(tuple([element[1] for element in element.items()]))
			else:
				transformedState.append(element)

		return tuple(transformedState)
	
	def typecast(self,val,thetype,default):
		try:
			return thetype(val)
		except:
			return default

	def conductBSTM(self,state=[]):
		MAX_HOUSES = 32
		MAX_HOTELS = 12

		state = state or self.state

		# might move these as class methods at a later point
		def getPropertyStatus(state,propertyId):
			mappingId = constants.space_to_property_map[propertyId]
			return state[self.PROPERTY_STATUS_INDEX][mappingId]
		
		def updatePropertyStatus(state,propertyId,propertyStatus):
			mappingId = constants.space_to_property_map[propertyId]
			self.updateState(state,self.PROPERTY_STATUS_INDEX,mappingId,propertyStatus)
	
		def getPlayerCash(state,player):
			return state[self.PLAYER_CASH_INDEX][player]
	
		def rightOwner(propertyStatus, player):
			if player == 0 and propertyStatus <= 0:
				return False
			if player == 1 and propertyStatus  >= 0:
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
				
		def validBuyingSequence(currentPlayer, properties,sign):
			
			for propertyObject in properties:

				(propertyId,constructions) = propertyObject
				propertyStatus = getPropertyStatus(state, propertyId)

				if propertyStatus in [7,-7,0]:
					return False

				if not rightOwner(propertyStatus, currentPlayer):
					return False
				
				if constructions<1 or constructions>5:
					return False

				currentConstructionsOnProperty = abs(propertyStatus) - 1 

				if ((currentConstructionsOnProperty + sign*constructions) > 5) or ((currentConstructionsOnProperty + sign*constructions) < 0):
					return False

			return True
		
		def maxHousesHotelsCheck(state,properties,sign):
			#If we dont do this, it replaces the list inplace
			propertyStatus = [ prop for prop in state[self.PROPERTY_STATUS_INDEX] ]
			
			newNumberOfHotels=0
			newNumberOfHouses=0
			
			for (propertyId,constructions) in properties:
				propertyStatus[propertyId] = abs(propertyStatus[propertyId]) + sign*constructions
				
			for status in propertyStatus:
				status = abs(status)
				if status>6 or status<0:
					return False
				elif status == 6:
					newNumberOfHotels += 1
				elif status>1:
					newNumberOfHouses+=(status-1)
				
			if newNumberOfHouses>MAX_HOUSES:
				return False
			if newNumberOfHotels>MAX_HOTELS:
				return False
			
			return True
		
		#Checks consistency of the group elements for current buy/sell house operation
		def monopolyCheck(state,properties,sign):
			propertyStatus = [ prop for prop in state[self.PROPERTY_STATUS_INDEX] ]
			for (propertyId,constructions) in properties:
				space = constants.board[propertyId]
				groupElements = space['monopoly_group_elements']
				for groupElement in groupElements:
					groupElementPropertyStatus = propertyStatus[groupElement]
					#GroupElement's Property Status should be same sign as current property and should be > 0
					if groupElementPropertyStatus*propertyStatus[propertyId] < 1:
						return False
					#House and Hotel related transactions can't take place when there are mortgaged properties in the current monopoly
					if groupElementPropertyStatus in [7,-7]:
						return False
				
				propertyStatus[propertyId] = abs(propertyStatus[propertyId]) + sign*constructions
				
			for (propertyId,constructions) in properties:
				propertyStat = propertyStatus[propertyId]
				
				space = constants.board[propertyId]
				groupElements = space['monopoly_group_elements']
				for groupElement in groupElements:
					#Checking if houses are being built or sold evenly
					groupElementPropertyStatus = abs(propertyStatus[groupElement])
					if groupElementPropertyStatus<(propertyStat-1) or groupElementPropertyStatus>(propertyStat+1):
						return False
			
			return True
						
		# house can be built only if you own a monopoly of colours 
		# double house can be built only if I have built one house in each colour 
		# order of the tuples to be taken into account
		def handleBuy(agent,properties):
			currentPlayer = agent.id
			
			invalidProperties = [x for x in properties if (x[1]<0) or (x[1]>5)]
			if len(invalidProperties) > 0:
				return False

			# determine if the agent actually has the cash to buy all this?
			# only then proceed; important for a future sceanrio
			if not hasBuyingCapability(currentPlayer, properties):
				return False

			if not validBuyingSequence(currentPlayer,properties,1):
				return False
			
			if not maxHousesHotelsCheck(state,properties,1):
				return False
			
			if not monopolyCheck(state,properties,1):
				return False

			# ordering of this tuple becomes important  
			for propertyObject in properties:

				(propertyId,constructions) = propertyObject
				space = constants.board[propertyId]
				groupElements = space['monopoly_group_elements']
				playerCash = getPlayerCash(state, currentPlayer)
				propertyStatus = getPropertyStatus(state, propertyId)
				currentConstructionsOnProperty = abs(propertyStatus) - 1 

				if constructions and constructions > 0:
					playerCash -= space['build_cost']*constructions
					
					if playerCash >= 0:
						propertyStatus = constructions + currentConstructionsOnProperty + 1

						if currentPlayer == 1:
							propertyStatus *= -1

						updatePropertyStatus(state,propertyId,propertyStatus)
						self.updateState(state,self.PLAYER_CASH_INDEX,currentPlayer,playerCash)
					else:
						#Should never occur
						return False
			return True

		def handleSell(agent,properties):
			currentPlayer = agent.id
			
			if not validBuyingSequence(currentPlayer,properties,-1):
				return False
			
			if not maxHousesHotelsCheck(state,properties,-1):
				return False
			
			if not monopolyCheck(state,properties,-1):
				return False
			
			for (propertyId,constructions) in properties:

				space = constants.board[propertyId]
				playerCash = getPlayerCash(state, currentPlayer)
				propertyStatus = getPropertyStatus(state,propertyId)

				houseCount = abs(propertyStatus) - 1
				
				houseCount -= constructions 
				playerCash += (space['build_cost']*0.5*constructions)

				propertyStatus = houseCount + 1

				if currentPlayer == 1:
					propertyStatus *= -1

				updatePropertyStatus(state,propertyId,propertyStatus)
				self.updateState(state,self.PLAYER_CASH_INDEX,currentPlayer,playerCash)
			return True

		# agent mortages a particular property
		# agent gets 50% of original money of the property
		# If the user tries to unmortgage something and he doesn't have the money entire operation fails
		# If user tries to mortgage an invalid property, entire operation fails
		def handleMortgage(agent,properties):
			currentPlayer = agent.id
			playerCash = getPlayerCash(state, currentPlayer)
			propertyStatusList = [ prop for prop in state[self.PROPERTY_STATUS_INDEX] ]
			
			for propertyId in properties:
				space = constants.board[propertyId]
				propertyPrice = space['price']
				mortagePrice = propertyPrice/2
				propertyStatus = propertyStatusList[propertyId]
				
				if (propertyStatus>1 and propertyStatus<7) or (propertyStatus<-1 and propertyStatus>-7):
					return False
				
				if not rightOwner(propertyStatus,currentPlayer):
					return False

				if propertyStatus in [-7,7]:
					
					unmortgagePrice = mortagePrice + mortagePrice*0.1

					if playerCash >= unmortgagePrice:
						playerCash -= unmortgagePrice 
					else:
						return False
					
					propertyStatus = 1
				else:
					playerCash += mortagePrice
					propertyStatus = 7

				if currentPlayer == 1:
						propertyStatus *= -1
				propertyStatusList[propertyId] = propertyStatus
			
			self.updateState(state,self.PROPERTY_STATUS_INDEX,None,propertyStatusList)	
			self.updateState(state,self.PLAYER_CASH_INDEX,currentPlayer,playerCash)
				#First subtract what you can from the player debt.
				#self.handle_payment(state)


		def handleTrade(agent,otherAgent,cashOffer,propertiesOffer,cashRequest,propertiesRequest):
			currentPlayer = agent.id
			cashRequest = cashRequest or 0
			cashOffer = cashOffer or 0

			otherPlayer = abs(currentPlayer - 1)
			
			currentPlayerCash = getPlayerCash(state,currentPlayer)
			otherPlayerCash = getPlayerCash(state,otherPlayer)

			if cashOffer > currentPlayerCash:
				return False

			if cashRequest > otherPlayerCash:
				return False


			for propertyOffer in propertiesOffer:
				propertyStatus = getPropertyStatus(state,propertyOffer)
				if not rightOwner(propertyStatus,currentPlayer):
					return False

			# check if the other agent actually cash and properties to offer
			for propertyRequest in propertiesRequest:
				propertyStatus = getPropertyStatus(state,propertyRequest)
				if not rightOwner(propertyStatus,otherPlayer):
					return False
				
			# update the values in the payload index 

			mortgagedProperties = filter(lambda propertyOffer : getPropertyStatus(state,propertyOffer) in [-7,7], propertiesOffer)
			restOffers = list(set(propertiesOffer) - set(mortgagedProperties))

			for mortgagedProperty in mortgagedProperties:
				space = constants.board[propertyId]
				response = otherAgent.respondMortgage(mortgagedProperty)
				propertyPrice = space['price']
				mortagePrice = propertyPrice/2
				
				multiplier = 1

				if otherPlayer == 1:
					 multiplier -= 1

				if response:
					unmortgagePrice = mortagePrice + 0.1*mortagePrice
					currentPlayerCash += unmortgagePrice
					otherPlayerCash -= unmortgagePrice
					updatePropertyStatus(state,mortgagedProperty,multiplier*1)
					self.updateState(state,self.PLAYER_CASH_INDEX,currentPlayer,currentPlayerCash)
				else:
					otherPlayerCash -= mortagePrice*0.1
				
				self.updateState(state,self.PLAYER_CASH_INDEX,otherPlayer,otherPlayerCash)
			
					
			phasePayload = [cashOffer,restOffers,cashRequest,propertiesRequest]

			self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.TRADE_OFFER)
			self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)

			tradeResponse = self.runPlayerOnStateWithTimeout(otherAgent,state)
			
			self.typecast(tradeResponse, bool, False)
			
			# if the trade was successful update the cash and property status
			if tradeResponse:

				currentPlayerCash += (cashRequest - cashOffer)
				otherPlayerCash += (cashOffer - cashRequest)
				
				self.updateState(state, self.PLAYER_CASH_INDEX,currentPlayer,currentPlayerCash)
				self.updateState(state, self.PLAYER_CASH_INDEX,otherPlayer,otherPlayerCash)
				
				for propertyOffer in propertiesOffer:
					propertyStatus = getPropertyStatus(state,propertyOffer) 
					updatePropertyStatus(state,propertyOffer,propertyStatus*-1)

				for propertyRequest in propertiesRequest:
					propertyStatus = getPropertyStatus(state,propertyRequest)
					updatePropertyStatus(state,propertyRequest,propertyStatus*-1)
			
			#Receive State
			phasePayload.insert(0,tradeResponse)
			self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
			
			self.runPlayerOnStateWithTimeout(agent,state,receiveState=True)

		def takeBMSTAction(agent,otherAgent,action):

			intent = action[0]
			
			if intent == "B":
				handleBuy(agent,action[1])

			elif intent == "S":
				handleSell(agent,action[1])
			
			elif intent == "M":
				handleMortgage(agent,action[1])

			elif intent == "T":
				handleTrade(agent,otherAgent,action[1],action[2],action[3],action[4])

		# TODO:merging of states; and hiding the bmst decison of first agent to the second
		previousPhaseNumber = state[self.PHASE_NUMBER_INDEX]
		agentOneDone = False
		agentTwoDone = False
		
		while True:
			
			self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.BSTM)
			
			bstmActionAgentOne = self.runPlayerOnStateWithTimeout(self.agentOne,state)

			if (bstmActionAgentOne is not None) and not agentOneDone:
				if not takeBMSTAction(self.agentOne,self.agentTwo,bstmActionAgentOne):
					agentOneDone = True
			else:
				agentOneDone = True

			bstmActionAgentTwo = self.runPlayerOnStateWithTimeout(self.agentTwo,state)
			if (bstmActionAgentTwo is not None) and not agentTwoDone:
				#AgentTwo sent an erroneous input. Give it no more BSTM Turns.
				if not takeBMSTAction(self.agentTwo,self.agentOne,bstmActionAgentTwo):
					agentTwoDone = True
			else:
				agentTwoDone = True
			
			"""
			Both players must be done with their BSTM
			"""
			if agentOneDone and agentTwoDone:
				#Counter against case where we fall on an idle position and do BSTM.
				#The previous phase would be dice roll. But it doesn't make sense to set that back.
				if previousPhaseNumber > self.DICE_ROLL:
					self.updateState(state,self.PHASE_NUMBER_INDEX,None,previousPhaseNumber)
				break
		
		
	def send_player_to_jail(self,state):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		log("jail","Player "+str(current_player)+" has been sent to jail")
		self.updateState(state,self.PLAYER_POSITION_INDEX,current_player,-1)
		self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.JAIL)
	
	def update_turn(self,state):
		currentTurn = state[self.PLAYER_TURN_INDEX]
		self.updateState(state,self.PLAYER_TURN_INDEX,None,currentTurn + 1)

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
				self.updateState(state,self.PLAYER_CASH_INDEX,current_player,playerCash)
				return [True,False]
		
		elif action[0] == 'C':
			#Check if the player has the mentioned property card.
			if (len(action)>1) & (action[1] in [self.CHANCE_GET_OUT_OF_JAIL_FREE,self.COMMUNITY_GET_OUT_OF_JAIL_FREE]):
				propertyStatus = state[self.PROPERTY_STATUS_INDEX][ action[1] ]
				
				if current_player == 0:
					owned = (propertyStatus < 0)
				else:
					owned = (propertyStatus > 0)
				
				if owned:
					if action[1] == self.COMMUNITY_GET_OUT_OF_JAIL_FREE:
						self.chest.deck.append(constants.communityChestCards[4])
					elif action[1] == self.CHANCE_GET_OUT_OF_JAIL_FREE:
						self.chance.deck.append(constants.chanceCards[7])
					
					self.updateState(state,self.PROPERTY_STATUS_INDEX,action[1],0)
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
		#Below mentioned property needed if the auction is not blind
		#state[self.PHASE_PAYLOAD_INDEX]['subphase'] = "start"
		phasePayload = state[self.PHASE_PAYLOAD_INDEX] or []
		phasePayload.append(playerPosition)
	
		self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.AUCTION)
		self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
		
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
		
		self.typecast(actionCurrentPlayer, int, 0)
		self.typecast(actionOpponent, int, 0)
		
		log("auction","Bids from the players: "+str(actionCurrentPlayer)+","+str(actionOpponent))	
		
		if actionCurrentPlayer > actionOpponent:
			#Current Player wins the auction
			winner = current_player
			winningBid = actionCurrentPlayer
		else:
			#Opponent wins
			winner = opponent
			winningBid = actionOpponent
		
		log("auction","Player "+str(winner)+" won the Auction")
		
		playerCash = state[self.PLAYER_CASH_INDEX][winner]
		playerCash -= winningBid

		self.updateState(state,self.PLAYER_CASH_INDEX,winner,playerCash)

		propertyStatus = -1

		if winner == 0:
			propertyStatus = 1

		self.updateState(state,self.PROPERTY_STATUS_INDEX,propertyMapping,propertyStatus)	
		
		#Receive State
		phasePayload = [winner]
		
		self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
	
		self.runPlayerOnStateWithTimeout(self.agentOne,state,receiveState=True)
		self.runPlayerOnStateWithTimeout(self.agentTwo,state,receiveState=True)
		
		#Clearing the payload as the auction has been completed
		self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,[])

	
	"""
	Handle the action response from the Agent for buying an unowned property
	"""	
	def handle_buy_property(self,state):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		propertyMapping = constants.space_to_property_map[playerPosition]
		
		if self.handle_payment(state, False):

			propertyStatus = -1 

			if current_player == 0:
				propertyStatus = 1

			self.updateState(state,self.PROPERTY_STATUS_INDEX,propertyMapping,propertyStatus)
			log('buy',"Player "+str(current_player)+" has bought "+constants.board[playerPosition]['name'])
			
			#Clearing the payload as the buying has been completed
			self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,[])
			return True
		
		#This would indicate going to Auction
		return False
	
	"""
	Handling payments the player has to make to the bank/opponent
	"""
	def handle_payment(self,state,take=True):
		
		(receiver,debt) = state[self.DEBT_INDEX]
		
		if debt == 0:
			#No payment to be made
			return True
		
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		opponent = abs(current_player - 1)
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		opponentCash = state[self.PLAYER_CASH_INDEX][opponent]
		receiverString = "bank"
		if receiver>0:
			receiverString = "Agent"+str(receiver)
		
		log('pay',"Player "+str(current_player)+" has to pay $"+str(debt)+" to the "+receiverString)
		
		if playerCash >= debt:
			self.updateState(state,self.PLAYER_CASH_INDEX,current_player,playerCash-debt)
			if receiver == opponent+1:
				self.updateState(state,self.PLAYER_CASH_INDEX,opponent,opponentCash + debt)
				state[self.PLAYER_CASH_INDEX][opponent] += debt
			
			#All the debt has been paid
			self.updateState(state,self.DEBT_INDEX,None,(0,0))
			return True
		elif take:
			#Take what you can get from the indebted
			self.updateState(state,self.PLAYER_CASH_INDEX,current_player,0)
			if receiver == opponent+1:
				self.updateState(state,self.PLAYER_CASH_INDEX,opponent,opponentCash + playerCash)

			#Update with only the remaining debt
			self.updateState(state,self.DEBT_INDEX,None,(receiver,debt - playerCash))

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
			self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.JAIL)
			self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,[])
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
		self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.DICE_ROLL)
		phasePayload = [self.dice.die_1,self.dice.die_2,outOfJail,self.dice.double] #Should outOfJail be in another receiveState call?
		self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
		self.runPlayerOnStateWithTimeout(player,state,receiveState=True)
		
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
			self.updateState(state,self.PLAYER_POSITION_INDEX,current_player,playerPosition)
			self.updateState(state,self.PLAYER_CASH_INDEX,current_player,playerCash)

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
		
		phasePayload = {} # Should this be done? Clearing of phase payload/properties?
			
		if isProperty:
			output = self.handle_property(state)
			if 'phase' in output:
				self.updateState(state,self.PHASE_NUMBER_INDEX,None,output['phase'])
			if 'phase_properties' in output:
				self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,output['phase_properties'])
			if 'debt' in output:
				self.updateState(state,self.DEBT_INDEX,None,output['debt'])
		else:
			if constants.board[playerPosition]['class'] == 'Chance':
				#Chance
				card = self.chance.draw_card()
				
				log("cards","Chance card \""+str(card['content'])+"\" has been drawn")
				
				#ReceiveState
				phasePayload = [card['id']]
				
				self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.CHANCE_CARD)
				self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
				self.runPlayerOnStateWithTimeout(player,state,receiveState=True)
				self.handle_cards_pre_turn(state,card,'Chance',player)
				
			elif constants.board[playerPosition]['class'] == 'Chest':
				#Community
				card = self.chest.draw_card()
				
				log("cards","Community Chest card \""+str(card['content'])+"\" has been drawn")
				
				#ReceiveState
				phasePayload = [card['id']]

				self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.COMMUNITY_CHEST_CARD)
				self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
				self.runPlayerOnStateWithTimeout(player,state,receiveState=True)
				self.handle_cards_pre_turn(state,card,'Chest',player)
			   
			elif constants.board[playerPosition]['class'] == 'Tax':
				#Tax
				cash = constants.board[playerPosition]['tax']
				self.updateState(state,self.PHASE_NUMBER_INDEX,None,self.PAYMENT)
				self.updateState(state,self.DEBT_INDEX,None,(0,cash))
			
			elif constants.board[playerPosition]['class'] == 'Idle':
				#Represents Go,Jail(Visiting),Free Parking
				pass
			
			# 

	"""
	Given that the current space is a property, determine what is to be done here.
	"""
	def handle_property(self,state):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		opponent = abs(current_player - 1)
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		
		#Could add a check here for whether this is a property. If not there will be an error here.
		propertyValue = state[self.PROPERTY_STATUS_INDEX][ constants.space_to_property_map[playerPosition] ]
		output = {}
		if propertyValue == 0:
			#Unowned
			output['phase'] = self.BUYING
			output['phase_properties'] = [playerPosition]
			output['debt'] = (0,constants.board[playerPosition]['price'])
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
				output['phase_properties'] = []
				output['debt'] = (opponent+1,rent)
			
			else:
				#When the property is owned by us
				pass
		
		return output
				
	
	"""
	Method handles various events for Chance and Community cards
	"""
	def handle_cards_pre_turn(self,state,card,deck,player):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		opponent = abs(current_player - 1)
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		phaseNumber = state[self.PHASE_NUMBER_INDEX]
		debt = state[self.DEBT_INDEX]
		propertyStatus = state[self.PROPERTY_STATUS_INDEX][current_player]
		updateState = False

		phasePayload = []
		
		if card['type'] == 1:
			#What should we do if we are receiving cash here? Should there be a BSTM?
			if card['money']<0:
				phaseNumber = self.PAYMENT
				debt = (0,abs(card['money']))
			else:
				playerCash += abs(card['money'])

		elif card['type'] == 2:
			#-ve represents you need to pay
			phaseNumber = self.PAYMENT
			debt = (opponent+1,card['money'])
			
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
				self.updateState(state,self.PROPERTY_STATUS_INDEX,propertyValue,1)
			else:
				self.updateState(state,self.PROPERTY_STATUS_INDEX,propertyValue,-1)
		
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
				phaseNumber = self.PAYMENT
				debt = (0,rent)
		
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
			
			# 
			output = self.handle_property(state)
			if 'phase' in output:
				phaseNumber = output['phase']
			if 'phase_properties' in output:
				phasePayload = output['phase_properties']
			if 'debt' in output:
				debt = output['debt']
				#We need to double rent if the player landed on opponent's property.
				#We could fall on our own property in which case there is no source payload attribute
				if (debt[0]>0):
					debt = (debt[0],debt[1]*2)
		
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
					phaseNumber = self.BUYING
					debt = (0,constants.board[playerPosition]['price'])
					phasePayload.append(playerPosition)
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
							
							phaseNumber = self.PAYMENT
							debt = (opponent+1,10 * (self.dice.die_1 + self.dice.die_2))
		
		elif card['type'] == 8:
			#Go back 3 spaces
			playerPosition -= 3 
			updateState = True
		else:
			logger.info('Invalid card type {type}...'.format(type=card['type']))


		self.updateState(state,self.PHASE_NUMBER_INDEX,None,phaseNumber)
		self.updateState(state,self.PHASE_PAYLOAD_INDEX,None,phasePayload)
		self.updateState(state,self.DEBT_INDEX,None,debt)
		self.updateState(state,self.PLAYER_POSITION_INDEX,current_player,playerPosition)
		self.updateState(state,self.PLAYER_CASH_INDEX,current_player,playerCash)
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
			self.updateState(self.state,self.PHASE_PAYLOAD_INDEX,None,[])
			
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
		
		return [winner,self.state]
	
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
	def runPlayerOnStateWithTimeout(self, player,state,receiveState=False):
		try:
			return self.runPlayerOnState(player,state,receiveState)
		except TimeoutError:
			print("Agent Timed Out")
			"""Change the return value here to ensure agent loose"""
			return None

	def runPlayerOnState(self,player,state,receiveState=False):
		
		action = None
		
		current_phase = state[self.PHASE_NUMBER_INDEX]
		payload = state[self.PHASE_PAYLOAD_INDEX]

		constants.state_history.append((player.id,self.transformState(state)))
		# self.updateState(state, self.STATE_HISTORY_INDEX, None, constants.state_history)

		if receiveState:
			action = player.receiveState(self.transformState(state))
		elif current_phase == self.BSTM:
			action = player.getBMSTDecision(self.transformState(state))
		elif current_phase == self.TRADE_OFFER:
			action = player.respondTrade(self.transformState(state))
		elif current_phase == self.BUYING:
			action = player.buyProperty(self.transformState(state))
		elif current_phase == self.AUCTION:
			action = player.auctionProperty(self.transformState(state))
		elif current_phase == self.PAYMENT:
			pass
		elif current_phase == self.JAIL:
			action = player.jailDecision(self.transformState(state))
		
		return action

#Testing
#adjudicator = Adjudicator(Agent,Agent)
#adjudicator.runGame()