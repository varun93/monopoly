import logging

import pandas as pd

import config
import dice
import spaces


logger = logging.getLogger(__name__)


class Game:
    """Keeps track of all game pieces."""

    def __init__(self):

        self.round = 0
        self.board = {}
        self.dice = None
        self.get_board(config.board_filename)

    def get_board(self, board_file):
        """
        Create board game with properties from CSV file in board_file.
        :param str board_file: Filename of CSV with board parameters
        """

        board_df = pd.read_csv(board_file)

        monopoly_groups = {};
            

        for _, attributes in board_df.iterrows():

            if attributes['class'] == 'Street':
                
                self.board[attributes['position']] = spaces.Street(attributes)
                if (attributes['monopoly'] not in monopoly_groups):
                    monopoly_groups[attributes['monopoly']] = []
                monopoly_groups[attributes['monopoly']].append(self.board[attributes['position']])

            if attributes['class'] == 'Railroad':
                self.board[attributes['position']] = spaces.Railroad(attributes)
                
                if (attributes['monopoly'] not in monopoly_groups):
                    monopoly_groups[attributes['monopoly']] = []
                monopoly_groups[attributes['monopoly']].append(self.board[attributes['position']])

            if attributes['class'] == 'Utility':
                self.board[attributes['position']] = spaces.Utility(attributes)
                if (attributes['monopoly'] not in monopoly_groups):
                    monopoly_groups[attributes['monopoly']] = []
                monopoly_groups[attributes['monopoly']].append(self.board[attributes['position']])

            if attributes['class'] == 'Tax':
                self.board[attributes['position']] = spaces.Tax(attributes)

            if attributes['class'] == 'Chance':
                chance_df = pd.read_csv(config.chance_filename)
                self.board[attributes['position']] = spaces.Chance(chance_df)

            if attributes['class'] == 'Chest':
                comm_df = pd.read_csv(config.community_chest_filename)
                self.board[attributes['position']] = spaces.Chest(comm_df)

            if attributes['class'] in ['Jail', 'Idle']:
                self.board[attributes['position']] = []

        #Grouping together monopolies so that they can accessed more easily later
        for monopoly in monopoly_groups:
            for prop in monopoly_groups[monopoly]:
                prop.monopoly_group_elements.extend([x for x in monopoly_groups[monopoly] if x.name!=prop.name])
                
        if config.verbose['board']:
            self.print_board()
    
    #Debugging Component            
    def print_board(self):
        for x in self.board:
            if isinstance(self.board[x], spaces.Street):
                logger.info("Position "+str(x));
                logger.info("Name: "+self.board[x].name);
                logger.info("Monopoly Group Elements: ");
                for y in self.board[x].monopoly_group_elements:
                    logger.info(y.name)
                logger.info("")

    def pass_dice(self):

        self.dice = dice.Dice()

    def update_round(self):

        self.round += 1

        if config.verbose['round']:
            logger.info('\n')
            logger.info('Starting round {round}...'.format(round=self.round))
