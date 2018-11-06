import numpy as np

class GetOutOfJailFree:
    """Get out of Jail free card. There are 2 of these, each one being present
    in the Chance and Community Chest card sets."""
    """Realise it might not be semantically correct to term this as a Space.
    Can change as required."""
    def __init__(self,attrib):
        #For now, this is just a 2x1 array containing owner information for each card
        self.name = attrib['name']
        self.card_owner = None
    
    """Return if the assigning of ownership was successful
    Can optionally specify previous owner in case this is a trade"""
    def add_ownership(self,owner,previous_owner=None):
        if self.card_owner is previous_owner:
            self.card_owner = owner
            return True
        return False
    
    """Removes ownership, represents the usage of the card.
    Must return the card to the bottom of the corresponding deck
    Returns if the removal of ownership was successful."""
    def remove_ownership(self,owner):
        if self.card_owner is owner:
            self.card_owner = None
            #Should the logic to return the card to the deck be here?
            return self.name
        return None

class Card:
    def __init__(self,attrib):
        #Type:
        #1 = Money to/from the bank
        #2 = Money to/from other players
        #3 = Change position to self.position
        #4 = Get out of Jail free
        #5 = Pay for each house self.money and for each hotel, self.money2
        #6 = Advance to nearest Railroad
        #7 = Advance to nearest Utility
        #8 = Go back 3 spaces
        self.id = attrib['Id']
        self.content = attrib['Content']
        self.type = attrib['Type']
        self.position = attrib['Position']
        self.money = attrib['Money']
        self.money2 = attrib['Money2']

class Cards:
    def __init__(self, df):
        self.deck = []
        for _, attributes in df.iterrows():
            self.deck.append(Card(attributes))
        np.random.shuffle(self.deck)
        
    def draw_card(self):
        drawn_card = self.deck.pop()
        if drawn_card.type is not 4:
            self.deck.append(drawn_card)
        return drawn_card
