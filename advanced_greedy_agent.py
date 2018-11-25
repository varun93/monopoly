import constants

class Agent:
	def __init__(self, id):
		self.id = id
		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5
		self.DEBT_INDEX = 6
		self.STATE_HISTORY_INDEX = 7
		self.CHANCE_GET_OUT_OF_JAIL_FREE = 40
		self.COMMUNITY_GET_OUT_OF_JAIL_FREE = 41
		self.current_player = self.id - 1
		self.threshold = 0.7

	def getPropertyValue(self, property_id, player):
		pass #Return worth for the property

	def getBMSTDecision(self, state):
		debt = self.parseDebt(state, self.current_player)[1]
		money = state[self.PLAYER_CASH_INDEX][self.current_player]

		if debt == 0:
			(total_money_required, list_of_unmortgage_property_or_buying_houses) = self.buying_houses_or_unmortgaging_strategy()
			if total_money_required <= money:
				return list_of_unmortgage_property_or_buying_houses
			else:
				mortgaged_property_ids = self.mortgaging_property_strategy(state, total_money_required - money)
				if len(mortgaged_property_ids) != 0:
					return mortgaged_property_ids

		elif debt > 0 and debt > money:
			actual_debt = debt - money

			if self.isDebtForBuyPropertyPhase(state):
				if self.isPropertyWorthToBuy(state, self.current_player):
					mortgaged_property_ids = self.mortgaging_property_strategy()
					if len(mortgaged_property_ids) != 0:
						return mortgaged_property_ids
					else:
						selling_number_pf_houses_for_properties = self.selling_house_strategy()
						return selling_number_pf_houses_for_properties
				else:
					self.storeAuctionValue()
			else:
				mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt)
				if len(mortgaged_property_ids) != 0:
					return mortgaged_property_ids
				else:
					selling_number_pf_houses_for_properties = self.selling_house_strategy(state, actual_debt)
					return selling_number_pf_houses_for_properties

	def setAuctionValue(self, propertyId):
		"""Stores the bid for Auction"""
		pass

	def getAuctionValue(self, propertyId):
		"""Returns the auction value"""
		pass

	def selling_house_strategy(self, state, actual_debt):
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		for property in owned_properties:
			#Calculate worth and sort them
		pass #return list of properties and number of houses to be sold.

	def mortgaging_property_strategy(self, state, actual_debt):
		"""Mortgage only the properties with zero houses"""
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		for property in owned_properties:
			# Calculate worth and sort them
		pass


	def isPropertyWorthToBuy(self, state, current_player):
		"""Calculate the worth of the property and then return boolean true or false based on threshold"""
		pass


	def isDebtForBuyPropertyPhase(self, state):
		return False #Should return True or False

	def estimateWealth(severityLevel={"NORMAL", "DANGER"}):
		"""Summation of property with zero houses and liquid money"""
		total_wealth = 0
		return total_wealth

	def buying_houses_or_unmortgaging_strategy(self):
		#It should evaluate the buying house and unmortgaging property as an atomic action and then return a decision.
		#Calculate worth of both the actions by calculating the increase in rent and then return.
		wealth = self.estimateWealth("NORMAL")
		threshold_wealth = self.threshold * wealth
		"""Decide to buy houses or unmortgaging based on threshold wealth"""
		pass

	def respondTrade(self, state):
		return False

	def buyProperty(self, state):
		pass

	def auctionProperty(self, state):
		pass

	def receiveState(self, state):
		pass

	def jailDecision(self, state):
		pass

	def parseDebt(self, state, current_player):
		debt = state[self.DEBT_INDEX]
		money_owed = 0
		source = 0
		if current_player == 0:
			money_owed = debt[1]
			source = debt[0]
		else:
			money_owed = debt[3]
			source = debt[2]
		return (source, money_owed)

	def respondMortgage(self, state):
		pass

	def get_owned_property_not_morgaged(self, state, current_player):
		owned_properties = []
		i = 0
		for status in state[self.PROPERTY_STATUS_INDEX]:
			if current_player == 0 and status > 0 and status != 7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			elif current_player == 1 and status < 0 and status != -7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			i = i + 1
		return owned_properties
