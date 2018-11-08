import config
import dice
import constants
from cards import Cards
from agent import Agent
import numpy as np
#from utils import combineStates

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
			(0,0),#player's position; 2
			(0,0), #player's cash; 3
			0, #phase number; 4
			None, #phase payload; 5
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

		state[PHASE_NUMBER_INDEX] = 0

		(b,m,s,t) = agentOne.run(state)
		# handleBMST
		(b,m,s,t) = agentTwo.run(state)
		# handleBMST


	def parseAction(self):
		pass

	"""To reset dice for a new turn"""
	def pass_dice(self):
		self.dice = dice.Dice()

    def update_turn(self):
        self.turn += 1
            
            
    """
    Phases
    1 = Initial BSTM
    2 = BSTM Before applying turn effect
    3 = Unowned Property, Buying
    4 = Unowned Property, Auction
    5 = Owned Property, Pay Rent
    6 = Tax (i.e., Pay/Receive money from the Bank.)
    7 = Cards (Will there need to be nesting here?)
    Imcomplete
    
    
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
    def dice_roll(self):

    	# 
        self.pass_dice()
        self.dice.roll()

        playerPosition = state[PLAYER_POSITION_INDEX][current_player]
        
        if self.dice.double_counter == 3:
            self.send_player_to_jail(state)
            #End current player's turn here
            #Should there be a GoToJail state to let the player know?
        else:
            #Update player position
            current_player = state[PLAYER_TURN_INDEX] % 2
            
            #Jail
            if playerPosition == -1:
                #Do special handling and return here
                return
            playerPosition += self.dice.roll_sum
            
            #Passing Go
            if playerPosition >= 40:
                playerPosition = playerPosition % 40
                playerPosition += 200
			
            state[PLAYER_POSITION_INDEX][current_player] = playerPosition
			#Next, perform square effect
            #Preparation for next phase:
            self.update_state()
            
            
    def update_state(self):
    	
    	current_player = state[PLAYER_TURN_INDEX] % 2
        propertyToSpaceMap = constants.property_to_space_map
        isProperty = (state.position in propertyToSpaceMap)
        position = None
        
        phase_properties = {}

        playerPosition = state[PLAYER_POSITION_INDEX][current_player]
        playerProperty = state[PROPERTY_STATUS_INDEX][propertyToSpaceMap[playerPosition]]

        if isProperty:
        	# if its not taken by anyone
            if prop_value == 0:
                #Unowned
                state[PHASE_NUMBER_INDEX] = 3 # buying phase
            else:
                #Check if owned by opponent
                if current_player == 0:
                    owned = prop_value < 0
                else:
                    owned = prop_value > 0
                
                state[PHASE_NUMBER_INDEX] = 5
        else:
            if constants.board[playerPosition]['class'] == 'Chance':
                #Chance
                pass
            elif constants.board[playerPosition]['class'] == 'Chest':
                # Community
                card = self.chest.draw_card()
                if card.type == 1:
                    #What should we do if we are receiving cash here? Should there be a BSTM?
                    phase_properties.cash = card.money
                    phase_properties.source = "bank"
                elif card.type == 2:
                    phase_properties.cash = card.money
                    phase_properties.source = "opponent"
                elif card.type == 3:
                    if card.position == -1:
                        self.send_player_to_jail(state)
                    else:
                        if card.position < state.position:
                            #Passes Go
                            state.current_cash[current_player] += 200
                        state.position = card.position
                        # 
                        self.update_state()
				elif card.type == 2:
                    pass
				elif card.type == 4:
					pass
                    
            elif constants.board[state.position]['class'] == 'Tax':
                #Tax
                #First ask for BSTM
                phase_properties.cash = constants.board[state.position]['tax']
                phase_properties.source = "bank"
            elif constants.board[state.position]['class'] == 'Idle':
                pass

        state[5] = phase_properties
    		

	def send_player_to_jail(self,state):
        current_player = state.turn%2
        state.position[current_player] = -1 #sending the player to jail
        
	def update_turn(self):
		self.turn += 1
			
			
	"""
	Phases
	1 = Initial BSTM
	2 = BSTM Before applying turn effect
	3 = Unowned Property, Buying
	4 = Unowned Property, Auction
	5 = Cards (Will there need to be nesting here?)
	
	6 = Post turn BSTM
	
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

		# 
		self.pass_dice()
		
		current_player = state[0] % 2
		playerPosition = state[PLAYER_POSITION_INDEX][current_player]
		playerCash = state[PLAYER_CASH_INDEX][current_player]
		#Jail
		if playerPosition == -1:
			#Do special handling and return here
			return
		
		self.dice.roll()
		
		if self.dice.double_counter == 3:
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

			state[PLAYER_POSITION_INDEX[current_player] = playerPosition
			state[PLAYER_CASH_INDEX[current_player] = playerCash

			self.update_state(state)
			
	def handle_in_jail_state(self,state):
		pass
			
			
	def update_state(self,state):
		current_player = state[0]%2
		playerPosition = state[PLAYER_POSITION_INDEX][current_player]
		
		isProperty = (playerPosition in constants.space_to_property_map)
		
		state[5] = {} # Should this be done? Clearing of phase payload/properties?
			
		if isProperty:
			output = self.handle_property(state)
			if 'phase' in output:
				state[4] = output['phase']
			if 'phase_properties' in output:
				state[5] = output['phase_properties']
					
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
				state[PHASE_PAYLOAD_INDEX]['cash'] = constants.board[playerPosition]['tax']
				state[PHASE_PAYLOAD_INDEX]['source'] = "bank"
			
			elif constants.board[playerPosition]['class'] == 'Idle':
				pass
	
	"""
	Given that the current space is a property, determine what is to be done here.
	"""
	def handle_property(self,state):
		current_player = state[0]%2
		prop_value = state[1][ constants.space_to_property_map[playerPosition] ]
		playerPosition = state[PLAYER_POSITION_INDEX][current_player]
		output = {}
		if prop_value == 0:
			#Unowned
			output['phase'] = 3
			output['phase_properties'] = {}
			output['phase_properties']['cash'] = constants.board[playerPosition]['price']
			output['phase_properties']['source'] = "bank"
		else:
			#Check if owned by opponent
			if current_player == 0:
				owned = (prop_value < 0)
			else:
				owned = (prop_value > 0)
			
			if owned:
				rent = 0
				abs_prop_value = abs(prop_value)
				
				if abs_prop_value == 1:
					rent = constants.board[playerPosition]['rent']
					monopolies = constants.board[playerPosition]['monopoly_group_elements']
					sign = prop_value/abs_prop_value
					
					counter = 1
					for monopoly in monopolies:
						monopoly_sign = state[1][constants.space_to_property_map[monopoly]]
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
				
				elif abs_prop_value == 2:
					rent = constants.board[playerPosition]['rent_house_1']
				elif abs_prop_value == 3:
					rent = constants.board[playerPosition]['rent_house_2']
				elif abs_prop_value == 4:
					rent = constants.board[playerPosition]['rent_house_3']
				elif abs_prop_value == 5:
					rent = constants.board[playerPosition]['rent_house_4']
				elif abs_prop_value == 6:
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
		current_player = state[0]%2
		playerPosition = state[PLAYER_POSITION_INDEX][current_player]
		playerCash = state[PLAYER_CASH_INDEX][current_player]

		if card.type == 1:
			#What should we do if we are receiving cash here? Should there be a BSTM?
			state[5]['cash'] = card.money
			state[5]['source'] = "bank"

		elif card.type == 2:
			state[5]['cash'] = card.money
			state[5]['source'] = "opponent"
			
		elif card.type == 3:
			if card.position == -1:
				self.send_player_to_jail(state)
			else:
				if card.position < playerPosition:
					#Passes Go
					playerCash += 200
				playerPosition = card.position

				state[PLAYER_POSITION_INDEX][current_player] = playerPosition
				state[PLAYER_CASH_INDEX][current_player] = playerCash
				self.update_state(state)
				
		elif card.type == 4:
			"""
			Get out of Jail free
			property_status:
			28 = Chance
			29 = Community Chest
			"""
			if deck == 'Chest':
				prop_value = 29
			else:
				prop_value = 28
			
			if current_player == 0:
				state[1][prop_value] = 1
			else:
				state[1][prop_value] = -1
				
		elif card.type == 5:
			n_houses = 0
			n_hotels = 0
			if current_player == 0:
				#first player
				for prop in state[1]:
					if prop in range(2,6):
						n_houses+= (i-1)
					if prop == 6:
						n_hotels+= 1
			else:
				#second player
				for prop in state[1]:
					if prop in range(-5,-1):
						n_houses+= (abs(i)-1)
					if prop == -6:
						n_hotels+= 1
			state[5]['cash'] = card.money*n_houses + card.money2*n_hotels
			state[5]['source'] = "bank"
		
		elif card.type == 6:
			#Advance to nearest railroad. Pay 2x amount if owned
			railroads = [i for i in range(len(board)-1) if board[i]['class']=='Railroad']
			if (playerPosition < 5) or (playerPosition>=35):
				playerPosition = 5
				if (playerPosition>=35):
					#Passes Go
					state[3][current_player] += 200
			elif (playerPosition < 15) and (playerPosition>=5):
				playerPosition = 15
			elif (playerPosition < 25) and (playerPosition>=15):
				playerPosition = 25
			elif (playerPosition < 35) and (playerPosition>=25):
				playerPosition = 35
			
			state[PLAYER_POSITION_INDEX][current_player] = playerPosition
			state[PLAYER_CASH_INDEX][current_player] = playerCash
			# 
			output = self.handle_property(state)
			if 'phase' in output:
				state[4] = output['phase']
			if 'phase_properties' in output:
				state[5] = output['phase_properties']
			
			#We need to double rent if the player landed on opponent's property.
			if state[5]['source'] == 'opponent':
				state[5]['cash'] *= 2
		
		elif card.type == 7:
			#Advance to nearest utility. Pay 10x dice roll if owned
			utilities = [i for i in range(len(board)-1) if board[i]['class']=='Utility']
			if (playerPosition < 12) or (playerPosition>=28):
				playerPosition = 12
				if (playerPosition>=28):
					#Passes Go
					playerCash += 200
			elif (playerPosition < 28) and (playerPosition>=12):
				playerPosition = 28
			
				prop_value = state[1][ constants.space_to_property_map[playerPosition] ]
				if prop_value == 0:
					#Unowned
					state[PHASE_NUMBER_INDEX] = 3
					state[PHASE_PAYLOAD_INDEX]['cash'] = constants.board[playerPosition]['price']
					state[PHASE_PAYLOAD_INDEX]['source'] = "bank"
				else:
					#Check if owned by opponent
					if current_player == 0:
						owned = (prop_value < 0)
					else:
						owned = (prop_value > 0)
					
					if owned:
						abs_prop_value = abs(prop_value)
						#This point is up for contention.
						#The rules of the card if taken literally state that you would need to pay even if the property is mortgaged.
						#But, not considering that as it doesn't seem to be in the spirit of the game.
						if abs_prop_value == 1:
							self.dice.roll(True)
							state[PHASE_PAYLOAD_INDEX]['cash'] = 10 * self.dice.roll_sum
							state[PHASE_PAYLOAD_INDEX]['source'] = "opponent"
		
		elif card.type == 8:
			#Go back 3 spaces
			state[PLAYER_POSITION_INDEX][current_player]-= 3
			self.update_state(state)
		else:
			logger.info('Invalid card type {type}...'.format(type=card.type))


		# update the player positon and cash and call update_state and property here?
		state[PLAYER_POSITION_INDEX][current_player] = playerPosition
		state[PLAYER_CASH_INDEX][current_player] = playerCash
		# make further calls
	
	def send_player_to_jail(self,state):
		current_player = state[PLAYER_TURN_INDEX]%2
		state[PLAYER_POSITION_INDEX][current_player] = -1 #sending the player to jail
		
	
	def runPlayerOnState(self):
	
		# conduct a BMST phase
		nextPlayer = (state[0] + 1)%2 
		(b,s,m,t) = agent.run(state)
		actionTaken = None
	
		# upadate the state
		state[0] = nextPlayer

		self.rollDice()

		# diceValue = rollDice()
		# state[4] = 3
		# state[5] = diceValue

		if nextPlayer == 0:
			actionTaken = agent.run(state)
		else:
			actionTaken = agent.run(state)

		parseAction(actionTaken,state)
