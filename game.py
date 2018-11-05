import logging

import pandas as pd

import config
import dice
import spaces
import constants

logger = logging.getLogger(__name__)

class Game:
    """Keeps track of all game pieces."""

    def __init__(self):

        self.turn = 0
        self.dice = None
        self.end_turn = False #Signal showing that it is ok to end the turn. Used to account for Double Throws.            
        
    """To reset dice for a new turn"""
    def pass_dice(self):
        self.dice = dice.Dice()

    def update_turn(self):
        self.turn += 1
        if config.verbose['turn']:
            logger.info('\n')
            logger.info('Starting turn {turn}...'.format(turn=self.turn))
            
            
    """Phases"""
    
    """Phase 2: Dice Roll"""
    def dice_roll(self,state):
        self.pass_dice()
        self.dice.roll()
        
        if self.dice.double_counter == 3:
            send_player_to_jail(state)
            #End current player's turn here
            #Should there be a GoToJail state to let the player know?
        else:
            #Update player position
            current_player = state.turn%2
            state.position[current_player] += self.dice.roll_sum
            #Next, perform square effect
            #Preparation for next phase:
            """
            Phase Properties:
            Is the property owned?
            If unowned, there are 3 sequential sub-phases: BSTM,Buying,Auction. Which one are you in?
            If owned, 2 sub-phases: BSTM,rent. Note: BSTM here for opponent must be applied after the turn.
            If cards, draw top card,do effect, return it to bottom of the deck.
            If Go To Jail, send to jail. Immediately end the turn.
            If currently in Jail, 3 ways to get out.
            """
            isProperty = (state.position in constants.property_to_space_map)
            
            if isProperty:
                prop_value = state.property_status[ constants.property_to_space_map[state.position] ]
                if prop_value == 0:
                    #Unowned
                    state.phase = 3 # buying phase
                    state.phase_properties = {}
                    state.phase_properties.prephase_bstm = True
                else:
                    #Check if owned by opponent
                    if current_player == 0:
                        owned = prop_value < 0
                    else:
                        owned = prop_value > 0
                    
                    state.phase = 5
                    state.phase_properties = {}
                    state.phase_properties.prephase_bstm = True
            else:
                if constants.board[state.position]['class'] == 'Chance':
                    #Chance
                    pass
                elif constants.board[state.position]['class'] == 'Chest':
                    #Community
                    pass
                elif constants.board[state.position]['class'] == 'Tax':
                    #Tax
                    #First ask for BSTM
                    #state.current_cash[current_player]-= constants.board[state.position]['tax']
                    pass
            
    
    
    
    def send_player_to_jail(self,state):
        current_player = state.turn%2
        state.position[current_player] = -1 #sending the player to jail
        
    
    """Phase 3: BSTM"""
    #def unowned_property(self):
        
g = Game()
g.dice_roll()
    
