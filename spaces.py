import numpy as np

#Class only stores information about each board position

class Space:
    """Generic space object that initializes the two attributes shared by all spaces: Name and position on the board."""

    def __init__(self, attrib):

        self.name = attrib['name']            # Property name


class Property(Space):
    """Generic property object with the attributes shared by the three space types that can be owned: Streets,
    railroads, and utilities. Inherits attributes from the Space object."""

    def __init__(self, attrib):

        Space.__init__(self, attrib)

        #Static Properties
        self.monopoly = attrib['monopoly']            # Name of monopoly
        self.monopoly_size = attrib['monopoly_size']  # Number of properties in monopoly
        self.price = attrib['price']                  # Price to buy
        self.price_mortgage = self.price / 2          # Mortgage price
        self.rent = attrib['rent']                    # Initial rent

        self.mortgage = False                         # Mortgage status
        self.owner = None                             # Property owner
        self.monopoly_group_elements = []             # List containing other properties in the same monopoly


class Street(Property):
    """Street object that includes attributes related to buildings: cost to build, rent prices at each level of building
    development, and the number of buildings built. Inherits attributes from the Property object."""

    def __init__(self, attrib):

        Property.__init__(self, attrib)

        self.build_cost = attrib['build_cost']        # Building cost
        self.rent_monopoly = self.rent * 2            # Rent with monopoly
        self.rent_house_1 = attrib['rent_house_1']    # Rent with 1 house
        self.rent_house_2 = attrib['rent_house_2']    # Rent with 2 houses
        self.rent_house_3 = attrib['rent_house_3']    # Rent with 3 houses
        self.rent_house_4 = attrib['rent_house_4']    # Rent with 4 houses
        self.rent_hotel = attrib['rent_hotel']        # Rent with hotel
        self.n_buildings = 0                          # Number of buildings

    def get_rent(self):
        
        if self.mortgage:
            return 0
        
        if self.owner is not None:
            flag = False
            for monopolies in self.monopoly_group_elements:
                if monopolies.owner is not self.owner:
                    flag = True
                    break
            if not flag:
                #Monopoly has been formed for the current property
                if self.n_buildings == 0:
                    return self.rent*2
                elif self.n_buildings == 1:
                    return self.rent_house_1
                elif self.n_buildings == 2:
                    return self.rent_house_2
                elif self.n_buildings == 3:
                    return self.rent_house_3
                elif self.n_buildings == 4:
                    return self.rent_house_4
                elif self.n_buildings == 5:
                    return self.rent_hotel
            else:
                return self.rent
        return 0


class Railroad(Property):
    """Railroad object that includes attributes related to rent prices per number of railroads owned. Inherits
    attributes from the Property object."""

    def __init__(self, attrib):

        Property.__init__(self, attrib)

    def get_rent(self):
        if self.mortgage:
            return 0
        
        if self.owner is not None:
            count = 1
            for monopolies in self.monopoly_group_elements:
                if monopolies.owner is self.owner:
                    count+=1
                    break
            return self.rent*count
        return 0


class Utility(Property):
    """Utility object that includes attributes related to rent prices in the Utility monopoly. For this monopoly, rents
    are multipliers of dice rolls rather than absolute values. Inherits attributes from the Property object."""

    def __init__(self, attrib):

        Property.__init__(self, attrib)

        self.rent_monopoly = self.rent + 6

    def get_rent(self,dice_roll):
        if self.mortgage:
            return 0
        
        if self.owner is not None:
            count = 1
            for monopolies in self.monopoly_group_elements:
                if monopolies.owner is self.owner:
                    count+=1
                    break
            if count == 1:
                return self.rent * dice_roll
            else:
                return (self.rent+6) * dice_roll
        return 0

class GetOutOfJailFree(Space):
    """Get out of Jail free card. There are 2 of these, each one being present
    in the Chance and Community Chest card sets."""
    """Realise it might not be semantically correct to term this as a Space.
    Can change as required."""
    def __init__(self,attrib):
        #For now, this is just a 2x1 array containing owner information for each card
        Space.__init__(self, attrib)
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
        

class Tax(Space):
    """Tax object that lists the tax to be paid by a player that lands on a taxed space. Inherits attributes from the
    Space object."""

    def __init__(self, attrib):

        Space.__init__(self, attrib)

        self.tax = attrib['tax']


class Card(object):
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


class Chance:
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

class Chest:
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
