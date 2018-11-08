import config
import dice
import constants
from cards import Cards
from agent import Agent
from utils import combineStates


class BMST:
	
	def __init__(self,state,player):
		self.state = state
		self.player = player
		
	def setState(self,state):
		self.state = state

	def setPlayer(self, player):
		self.player = player

	# change the property to a key value pair 
	def handleBuy(self,player, b):
		
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

	# S = ("S", [(properties_numbers, number of houses)])				


	def handleSell(self, player, s):
		sale_payload = s[1]
		pass

	def handleMortgage(self, player, m):
		mortage_payload = m[1]
		pass

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

		self.agentOne = Agent(self.state)
		self.agentTwo = Agent(self.state)
		self.turn = 0
        self.dice = None
        self.chest = Cards(constants.communityChestCards)
        self.chance = Cards(constants.chanceCards)          
        
	

	def conductBMST(state):

		state[4] = 0

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
	    self.dice.roll()
	    
	    if self.dice.double_counter == 3:
	        self.send_player_to_jail(state)
	        #End current player's turn here
	        #Should there be a GoToJail state to let the player know?
	    else:
	        #Update player position
	        current_player = state[0] % 2
	        
	        #Jail
	        if state[2][current_player] == -1:
	            #Do special handling and return here
	            return
	        state[2][current_player] += self.dice.roll_sum
	        
	        #Passing Go
	        if state[2][current_player]>=40:
	            state[2][current_player] = state[2][current_player] % 40
	            state[3][current_player] += 200
	        #Next, perform square effect
	        #Preparation for next phase:
	        self.update_state()
	        
	        
	def update_state(self):
		current_player = state[0]%2
        isProperty = (state[2][current_player] in constants.property_to_space_map)
        
        state[5] = {}
            
        if isProperty:
            prop_value = state[1][ constants.property_to_space_map[state[2][current_player]] ]
            if prop_value == 0:
                #Unowned
                state[4] = 3 # buying phase
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
				        rent = constants.board[state[2][current_player]]['rent']
				        monopolies = constants.board[state[2][current_player]]['monopoly_group_elements']
				        sign = prop_value/abs_prop_value
				        flag = True
				        for monopoly in monopolies:
				            if constants.property_to_space_map[monopoly]/abs(constants.property_to_space_map[monopoly]) != sign:
				                flag = False
				        if flag:
				            rent = rent*2
				    elif abs_prop_value == 2:
				        rent = constants.board[state[2][current_player]]['rent_house_1']
				    elif abs_prop_value == 3:
				        rent = constants.board[state[2][current_player]]['rent_house_2']
				    elif abs_prop_value == 4:
				        rent = constants.board[state[2][current_player]]['rent_house_3']
				    elif abs_prop_value == 5:
				        rent = constants.board[state[2][current_player]]['rent_house_4']
				    elif abs_prop_value == 6:
				        rent = constants.board[state[2][current_player]]['rent_hotel']
				        
				    state[5].cash = rent
				    state[5].source = "opponent"
				
				state[4] = 5
        else:
            if constants.board[state[2][current_player]]['class'] == 'Chance':
                #Chance
				card = self.chance.draw_card()
				self.handle_cards_pre_turn(state,'Chance')
            elif constants.board[state[2][current_player]]['class'] == 'Chest':
				#Community
				card = self.chest.draw_card()
				self.handle_cards_pre_turn(state,'Chest')
                    
            elif constants.board[state[2][current_player]]['class'] == 'Tax':
                #Tax
                #First ask for BSTM
                state[5].cash = constants.board[state[2][current_player]]['tax']
                state[5].source = "bank"
            elif constants.board[state[2][current_player]]['class'] == 'Idle':
                pass
	
	"""
	Method handles various events for Chance and Community cards
	"""
	def handle_cards_pre_turn(self,state,deck):
		if card.type == 1:
		    #What should we do if we are receiving cash here? Should there be a BSTM?
		    state[5].cash = card.money
		    state[5].source = "bank"

		elif card.type == 2:
		    state[5].cash = card.money
		    state[5].source = "opponent"
		    
		elif card.type == 3:
		    if card.position == -1:
		        self.send_player_to_jail(state)
		    else:
		        if card.position < state[2][current_player]:
		            #Passes Go
		            state[3][current_player] += 200
		        state[2][current_player] = card.position
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
		    state[5].cash = card.money*n_houses + card.money2*n_hotels
		    state[5].source = "bank"
		elif card.type == 6:
		    #Advance to nearest railroad. Pay 2x amount if owned
		    railroads = [i for i in range(len(board)-1) if board[i]['class']=='Railroad']
		    if (state[2][current_player] < 5) or (state[2][current_player]>=35):
		        state[2][current_player] = 5
		        if (state[2][current_player]>=35):
		            #Passes Go
		            state[3][current_player] += 200
		    elif (state[2][current_player] < 15) and (state[2][current_player]>=5):
		        state[2][current_player] = 15
		    elif (state[2][current_player] < 25) and (state[2][current_player]>=15):
		        state[2][current_player] = 25
		    elif (state[2][current_player] < 35) and (state[2][current_player]>=25):
		        state[2][current_player] = 35
		elif card.type == 7:
		    #Advance to nearest utility. Pay 10x dice roll if owned
		    utilities = [i for i in range(len(board)-1) if board[i]['class']=='Utility']
		    if (state[2][current_player] < 12) or (state[2][current_player]>=28):
		        state[2][current_player] = 12
		        if (state[2][current_player]>=28):
		            #Passes Go
		            state[3][current_player] += 200
		    elif (state[2][current_player] < 28) and (state[2][current_player]>=12):
		        state[2][current_player] = 28
		elif card.type == 8:
		    #Go back 3 spaces
		    state[2][current_player]-= 3
		    self.update_state(state)
		else:
		    logger.info('Invalid card type {type}...'.format(type=card.type))
	
	def send_player_to_jail(self,state):
	    current_player = state[0]%2
	    state[2][current_player] = -1 #sending the player to jail
	    
	
	def runPlayerOnState(self):
	
		# conduct a BMST phase
		nextPlayer = (state[0] + 1)%2 
		(b,s,m,t) = agent.run(state)
		actionTaken = None
	
		# upadate the state
		state[0] = nextPlayer
	
		diceValue = rollDice()
		state[4] = 3
		state[5] = diceValue
	
		if nextPlayer == 0:
			actionTaken = agent.run(state)
		else:
			actionTaken = agent.run(state)
	
		parseAction(actionTaken,state)
