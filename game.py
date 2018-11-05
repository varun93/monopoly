import logging

import pandas as pd

import config
import dice
import spaces

logging.basicConfig(filename='monopoly.log', level=logging.INFO)
logger = logging.getLogger(__name__)


class Game:
    """Keeps track of all game pieces."""

    def __init__(self):

        self.turn = 0
        self.dice = None
        self.end_turn = False #Signal showing that it is ok to end the turn. Used to account for Double Throws.            
    
    #Function used to generate board in constants.py
    #Run this again if changes are made on          
    def generate_board_dictionary(self):
        board_df = pd.read_csv(config.board_filename)
        
        monopoly_groups = {};
        for _, attributes in board_df.iterrows():
            if (attributes['monopoly'] not in monopoly_groups):
                monopoly_groups[attributes['monopoly']] = []
            monopoly_groups[attributes['monopoly']].append(attributes)
        
        headers = [key for key in board_df.dtypes.index]
        print("{")
        l=0
        for _, attributes in board_df.iterrows():
            
            outer_comma = ""
            if l is not len(board_df)-1:
                outer_comma = ","   
            
            print(str(attributes['position']-1)+":{");
            
            k=0
            hasMonopolies = ((attributes['class'] == 'Street') or (attributes['class'] == 'Railroad') or (attributes['class'] == 'Utility'))
            for y in [z for z in attributes if z is not 'position']:
                comma = ""
                if (k is not len(headers)-1) or hasMonopolies:
                    comma = ","
                if isinstance(y, int):
                    print("\""+headers[k]+"\":"+str(y)+comma)
                else:
                    print("\""+headers[k]+"\":\""+str(y)+"\""+comma)
                k+=1
            
            if hasMonopolies:
                groups = [x.position-1 for x in monopoly_groups[attributes['monopoly']] if x.name != attributes.name]
                print("\"monopoly_group_elements\":"+str(groups))
                    
            
            print("}"+outer_comma);
            l+=1
        print("}")
        
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
            state.position += self.dice.roll_sum
            #Next, perform square effect
            #Preparation for next phase:
            state.phase = 2 # effect phase
            state.phase_properties = {}
            #state.phase_properties.owned = 
            
    
    
    
    def send_player_to_jail(self,state):
        current_player = state.turn%2
        state.position[current_player] = -1 #sending the player to jail
        
    
    """Phase 3: BSTM"""
    #def unowned_property(self):
        
g = Game()
g.generate_board_dictionary()
    
