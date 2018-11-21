import numpy as np
import constants

class Cards:
	def __init__(self, items):
		self.deck = list(map(lambda item : self.transformCard(item), items))
		np.random.shuffle(self.deck)
	
	#Reinitialize the given deckType(Community or Chance) using only the cards specified and in the order specified
	def reinit(self,deckType,cardIds):
		self.deck = [ deckType[id] for id in cardIds ]
		
	def transformCard(self,item):
		card = {}
		 #Type:
		#1 = Money to/from the bank
		#2 = Money to/from other players
		#3 = Change position to self.position
		#4 = Get out of Jail free
		#5 = Pay for each house self.money and for each hotel, self.money2
		#6 = Advance to nearest Railroad
		#7 = Advance to nearest Utility
		#8 = Go back 3 spaces
		card['id'] = item['id']
		card['content'] = item['content']
		card['type'] = item['type']
		card['position'] = item['position']
		card['money'] = item['money']
		card['money2'] = item['money2']

		return card
		

	def draw_card(self):
		drawn_card = self.deck.pop(0)

		if drawn_card['type'] is not 4:
			self.deck.append(drawn_card)
		
		return drawn_card