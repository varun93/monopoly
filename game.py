import logging

import pandas as pd

import config
import dice
import spaces
import constants
import cards

logger = logging.getLogger(__name__)

class Game:
    """Keeps track of all game pieces."""

    def __init__(self):

        self.turn = 0
        self.dice = None
        self.end_turn = False #Signal showing that it is ok to end the turn. Used to account for Double Throws.
        self.chest = Cards(pd.read_csv(config.community_chest_filename))
        self.chance = Cards(pd.read_csv(config.chance_filename))          
        
    """To reset dice for a new turn"""
    def pass_dice(self):
        self.dice = dice.Dice()

    def update_turn(self):
        self.turn += 1
        if config.verbose['turn']:
            logger.info('\n')
            logger.info('Starting turn {turn}...'.format(turn=self.turn))
            
            
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
    def dice_roll(self,state):
        self.pass_dice()
        self.dice.roll()
        
        if self.dice.double_counter == 3:
            self.send_player_to_jail(state)
            #End current player's turn here
            #Should there be a GoToJail state to let the player know?
        else:
            #Update player position
            current_player = state.turn%2
            
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
            self.handle_space(state)
            
            
    def handle_space(self,state):
        current_player = state.turn%2
        isProperty = (state.position in constants.property_to_space_map)
        
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
                        self.handle_space(state)
                elif card.type == 4:
                    pass
                elif card.type == 2:
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
        
    
    """Phase 3: BSTM"""
    #def unowned_property(self):
        
g = Game()
g.dice_roll()
    
