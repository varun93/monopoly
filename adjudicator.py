import config
import dice
import constants
from cards import Cards
from agent import Agent
import numpy as np

class BMST:
	
	def __init__(self,state,player):
		self.state = state
		self.player = player
		
	def setState(self,state):
		self.state = state

	def setPlayer(self, player):
		self.player = player

	# change the property to a key value pair 
	# house can be built only if you own a monopoly of colours 
	# double house can be built only if I have built one house in each colour 
	def handleBuy(self,player,b):
		
		properties = b[1]

		for propertyId in properties:
			propertyPrice = getPropertyValue(propertyId)
			propertyStatus = state[2][propertyId]
			playerCash = state[3][player]
			
			if playerPrice >= propertyPrice:
				state[2][propertyId] = calculatePropertyStatus(player,propertyId)
				state[3][player] = playerCash - propertyPrice
			else:
				# how do you want to handle the exception?
				# how to handle
				raise ValueError("Not Enough Cash")

	def handleSell(self, player, s):
		sale_payload = s[1]
		pass

	# buying/2
	def handleMortgage(self, player, m):
		mortage_payload = m[1]
		pass
	# 
	def handleTrade(self, player, t):
		trade_payload = t[1]
		pass

	def handle():
		pass

# make sure the state is not mutated
class Adjudicator:
	
	def __init__(self):
		self.state =  [
			0, #player turn; 0
			np.zeros(30), #player properties; 1
			[0,0],#player's position; 2
			[0,0], #player's cash; 3
			0, #phase number; 4
			{}, #phase payload; 5
		]

		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5

		self.agentOne = Agent(self.state)
		self.agentTwo = Agent(self.state)
		self.turn = 0
		self.dice = None
		self.chest = Cards(constants.communityChestCards)
		self.chance = Cards(constants.chanceCards)		  
		
	

	def conductBMST(state):

		state[self.PHASE_NUMBER_INDEX] = 0

		(b,m,s,t) = agentOne.getBMSTDecision(state)
		# handleBMST
		(b,m,s,t) = agentTwo.getBMSTDecision(state)
		# handleBMST


	def parseAction(self):
		pass

	"""To reset dice for a new turn"""
	def pass_dice(self):
		self.dice = dice.Dice()

	def send_player_to_jail(self,state):
		pass
	
	"""Scenario where current player is in jail at the start of the turn.
	Processes the response to the agent.jailDecision function."""
	"""
	Incoming action format:
	("R") : represents rolling to get out
    ("P") : represents paying $50 to get out (BSMT should follow)
    ("C", propertyNumber) : represents using a get out of jail card, 
    but in case someone has both, needs to specify which one they are using. 
    In general, should always specify the number (either 28 or 29)

	"""
	def handle_in_jail_state(self,state,decision):
		pass
        
	def update_turn(self):
		self.turn += 1
			
			
	"""
	Phases
	1 = Initial BSTM
	2 = BSTM Before applying turn effect
	3 = Unowned Property, Buying
	4 = Unowned Property, Auction
	5 = rent and other payments to either bank or opponent
	6 = Cards (Will there need to be nesting here?)
	7 = Post turn BSTM
	
	(Q: Will there need to be a BSTM if the player receives money?)
	"""
	
	"""
	Phase Properties:
	Is the property owned?
	If unowned, there are 3 sequential sub-phases: BSTM,Buying,Auction. Which one are you in?
	If owned, 2 sub-phases: BSTM,rent. Note: BSTM here for opponent must be applied after the turn.
	If cards, draw top card,do effect, return it to bottom of the deck.
	If Go To Jail, send to jail. Immediately end the turn.
	If currently in Jail, 3 ways to get out.
	"""
	
	"""Phase 2: Dice Roll"""
	def dice_roll(self,state=[]):
		
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		
		#Jail
		if playerPosition == -1:
			#Do special handling and return here
			action = self.agentOne.jailDecision(state)
			return
	
		self.dice.roll()
		
		if self.dice.double_counter == 3:
			state[self.PLAYER_POSITION_INDEX][current_player] = -1 #sending the player to jail
			self.send_player_to_jail(state)
			#End current player's turn here
			#Should there be a GoToJail state to let the player know?
		else:
			#Update player position
			
			playerPosition += self.dice.roll_sum
			
			#Passing Go
			if playerPosition>=40:

				playerPosition = playerPosition % 40
				playerCash += 200
			#Next, perform square effect
			#Preparation for next phase:

			state[self.PLAYER_POSITION_INDEX[current_player]] = playerPosition
			state[self.PLAYER_CASH_INDEX[current_player]] = playerCash

			self.update_state(state)
			
			
	def update_state(self,state):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		
		isProperty = (playerPosition in constants.space_to_property_map)
		
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
				self.handle_cards_pre_turn(state,card,'Chance')
			
			elif constants.board[playerPosition]['class'] == 'Chest':
				#Community
				card = self.chest.draw_card()
				self.handle_cards_pre_turn(state,card,'Chest')
			   
			elif constants.board[playerPosition]['class'] == 'Tax':
				#Tax
				#First ask for BSTM
				state[self.PHASE_PAYLOAD_INDEX]['cash'] = constants.board[playerPosition]['tax']
				state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
			
			elif constants.board[playerPosition]['class'] == 'Idle':
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
			output['phase'] = 3
			output['phase_properties'] = {}
			output['phase_properties']['cash'] = constants.board[playerPosition]['price']
			output['phase_properties']['source'] = "bank"
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
						rent = rent * self.dice.roll_sum
				
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
	def handle_cards_pre_turn(self,state,card,deck):
		current_player = state[self.PLAYER_TURN_INDEX]%2
		playerPosition = state[self.PLAYER_POSITION_INDEX][current_player]
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		updateState = False

		state[self.PHASE_PAYLOAD_INDEX] = {}
		
		if card['type'] == 1:
			#What should we do if we are receiving cash here? Should there be a BSTM?
			state[self.PHASE_PAYLOAD_INDEX]['cash'] = card['money']
			state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"

		elif card['type'] == 2:
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
					playerCash += 200
				playerPosition = card['position'] - 1
				updateState = True
				
				
		elif card['type'] == 4:
			"""
			Get out of Jail free
			property_status:
			28 = Chance
			29 = Community Chest
			"""
			if deck == 'Chest':
				propertyValue = 29
			else:
				propertyValue = 28
			
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
						n_houses+= (i-1)
					if prop == 6:
						n_hotels+= 1
			else:
				#second player
				for prop in state[self.PROPERTY_STATUS_INDEX]:
					if prop in range(-5,-1):
						n_houses+= (abs(i)-1)
					if prop == -6:
						n_hotels+= 1
			rent = card['money']*n_houses + card['money2']*n_hotels
			if rent > 0:
				state[self.PHASE_PAYLOAD_INDEX]['cash'] = rent
				state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
		
		elif card['type'] == 6:
			#Advance to nearest railroad. Pay 2x amount if owned
			railroads = [i for i in range(len(constants.board)-1) if constants.board[i]['class']=='Railroad']
			if (playerPosition < 5) or (playerPosition>=35):
				if (playerPosition>=35):
					#Passes Go
					playerCash += 200
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
			if state[self.PHASE_PAYLOAD_INDEX]['source'] == 'opponent':
				state[self.PHASE_PAYLOAD_INDEX]['cash'] *= 2
		
		elif card['type'] == 7:
			#Advance to nearest utility. Pay 10x dice roll if owned
			utilities = [i for i in range(len(constants.board)-1) if constants.board[i]['class']=='Utility']
			if (playerPosition < 12) or (playerPosition>=28):
				if (playerPosition>=28):
					#Passes Go
					playerCash += 200
				playerPosition = 12
			elif (playerPosition < 28) and (playerPosition>=12):
				playerPosition = 28
			
				propertyValue = state[self.PROPERTY_STATUS_INDEX][ constants.space_to_property_map[playerPosition] ]
				if propertyValue == 0:
					#Unowned
					state[self.PHASE_NUMBER_INDEX] = 3
					state[self.PHASE_PAYLOAD_INDEX]['cash'] = constants.board[playerPosition]['price']
					state[self.PHASE_PAYLOAD_INDEX]['source'] = "bank"
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
							self.dice.roll(True)
							state[self.PHASE_PAYLOAD_INDEX]['cash'] = 10 * self.dice.roll_sum
							state[self.PHASE_PAYLOAD_INDEX]['source'] = "opponent"
		
		elif card['type'] == 8:
			#Go back 3 spaces
			playerPosition -= 3 
			updateState = True
			# state[self.PLAYER_POSITION_INDEX][current_player] -= 3
			# playerPosition = -5
			# self.update_state(state)
		else:
			logger.info('Invalid card type {type}...'.format(type=card['type']))


		# update the player positon and cash and call update_state and property here?
		#Countermeasure against card type 8 code right above
		state[self.PLAYER_POSITION_INDEX][current_player] = playerPosition
		state[self.PLAYER_CASH_INDEX][current_player] = playerCash
		# make further calls
		if updateState:
			self.update_state(state)


		
	
	def runPlayerOnState(self):
	
		# conduct a BMST phase
		nextPlayer = (state[self.PLAYER_TURN_INDEX] + 1)%2 
		(b,s,m,t) = agent.run(state)
		actionTaken = None
	
		# upadate the state
		state[self.PLAYER_TURN_INDEX] = nextPlayer

		"""Resets dice roll before each turn"""
		self.pass_dice()
		
		"""rolls dice, moves the player and determines what happens on the space he has fallen on."""
		self.dice_roll(state)

		if nextPlayer == 0:
			actionTaken = agent.run(state)
		else:
			actionTaken = agent.run(state)

		parseAction(actionTaken,state)
