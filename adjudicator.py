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
		# 

# make sure the state is not mutated
class Adjudicator:
	
	def __init__(self):
		self.state =  [
			0, #player turn; 0
		    [], #player properties; 1
		    (0,0),#player's position; 2
		    (0,0), #player's cash; 3
		    0, #phase number; 4
		    None, #phase payload; 5
		    [] #state history; 6
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
            if state.position[current_player] == -1:
                #Do special handling and return here
                return
            state.position[current_player] += self.dice.roll_sum
            
            #Passing Go
            if state.position[current_player]>=40:
                state.position[current_player] = state.position[current_player] % 40
                state.current_cash[current_player] += 200
            #Next, perform square effect
            #Preparation for next phase:
            self.update_state()
            
            
    def update_state(self):
        current_player = state[0]%2
        propertyToSpaceMap = constants.property_to_space_map
        isProperty = (state.position in propertyToSpaceMap)
        
        state.phase_properties = {}
            
        if isProperty:
            prop_value = state.property_status[ constants.property_to_space_map[state.position] ]
            if prop_value == 0:
                #Unowned
                state.phase = 3 # buying phase
            else:
                #Check if owned by opponent
                if current_player == 0:
                    owned = prop_value < 0
                else:
                    owned = prop_value > 0
                
                state.phase = 5
        else:
            if constants.board[state.position]['class'] == 'Chance':
                #Chance
                pass
            elif constants.board[state.position]['class'] == 'Chest':
                #Community
                card = self.chest.draw_card()
                if card.type == 1:
                    #What should we do if we are receiving cash here? Should there be a BSTM?
                    state.phase_properties.cash = card.money
                    state.phase_properties.source = "bank"
                elif card.type == 2:
                    state.phase_properties.cash = card.money
                    state.phase_properties.source = "opponent"
                elif card.type == 3:
                    if card.position == -1:
                        self.send_player_to_jail(state)
                    else:
                        if card.position < state.position:
                            #Passes Go
                            state.current_cash[current_player] += 200
                        state.position = card.position
                        self.update_state()
				elif card.type == 2:
                    pass
				elif card.type == 4:
					pass
                    
            elif constants.board[state.position]['class'] == 'Tax':
                #Tax
                #First ask for BSTM
                state.phase_properties.cash = constants.board[state.position]['tax']
                state.phase_properties.source = "bank"
            elif constants.board[state.position]['class'] == 'Idle':
                pass
    
    
    def send_player_to_jail(self,state):
        current_player = state.turn%2
        state.position[current_player] = -1 #sending the player to jail
        

	def runPlayerOnState(self):

		# conduct a BMST phase
		nextPlayer = (state[0] + 1)%2 
		(b,s,m,t) = agent.run(state)
		actionTaken = None

		# upadate the state
		state['turn'] = nextPlayer

		diceValue = rollDice()
		state[4] = 3
		state[5] = diceValue

		if nextPlayer == 0:
			actionTaken = agent.run(state)
		else:
			actionTaken = agent.run(state)

		parseAction(actionTaken,state)
