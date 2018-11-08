import numpy as np

class Cards:
    def __init__(self, items):
        self.deck = list(map(lambda item : self.transformCard(item), items))
        np.random.shuffle(self.deck)
        
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
        card['id'] = item['Id']
        card['content'] = item['Content']
        card['type'] = item['Type']
        card['position'] = item['Position']
        card['money'] = item['Money']
        card['money2'] = item['Money2']

        return card
        

    def draw_card(self):
        drawn_card = self.deck.pop()

        if drawn_card.type is not 4:
            self.deck.append(drawn_card)
        
        return drawn_card
