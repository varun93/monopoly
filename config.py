n_players = 2 # Number of players

verbose = {'pay': True, #Player has a debt to pay handle_payments method
           'buy': True, #player is buying an unowned property
           'bstm':True,
           'auction':True,
           'cards':True, #when player falls on chance or community cards
           'state': True, #state information during each turn
           'dice': True, #dice value for each turn
           'board':False,
           'win_condition':False, #information of how winner was chosen
           'turn':False, #info about turn
           'jail':True, #info if player goes to jail
           'win':True #who finally won
           }

f = open("monopoly.log", "a")
f.write("----------------------------------------------------------\n")

def log(section,msg):
  if verbose[section]:
    f.write(str(msg)+'\n')
  