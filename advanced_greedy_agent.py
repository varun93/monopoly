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
		self.jail_counter = 0
		self.auction_value ={}


	def getPropertyValue(self, property_id, player):
		pass #Return monetary worth for the property

	def getValueForSellingHouses(self, properties, player):
		#return [(property_id1, worth1), (property_id2, worth2 )]
		pass

	def getValueForMortgageProperties(self, properties, player):
		#return [(property_id1, worth1), (property_id2, worth2 )]
		pass

	def getBMSTDecision(self, state):
		debt = self.parseDebt(state, self.current_player)[1]
		money = state[self.PLAYER_CASH_INDEX][self.current_player]

		if debt == 0:
			(total_money_required, list_of_unmortgage_property_or_buying_houses) = self.buying_houses_or_unmortgaging_strategy()
			if total_money_required <= money:
				return list_of_unmortgage_property_or_buying_houses
			#else:
			#	mortgaged_property_ids = self.mortgaging_property_strategy(state, total_money_required - money)
			#	if len(mortgaged_property_ids) != 0:
			#		return mortgaged_property_ids

		elif debt > 0 and debt > money:
			actual_debt = debt - money

			if self.isDebtForBuyPropertyPhase(state):
				property_id = state[self.PHASE_PAYLOAD_INDEX][0]
				if self.isPropertyWorthToBuy(state, self.current_player):
					mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt)
					if len(mortgaged_property_ids) != 0:
						return mortgaged_property_ids
					else:
						selling_number_pf_houses_for_properties = self.selling_house_strategy(state, actual_debt)
						return selling_number_pf_houses_for_properties
				else:
					self.storeAuctionValue(property_id)
			else:
				mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt)
				if len(mortgaged_property_ids) != 0:
					return mortgaged_property_ids
				else:
					selling_number_pf_houses_for_properties = self.selling_house_strategy(state, actual_debt)
					return selling_number_pf_houses_for_properties

	def storeAuctionValue(self, propertyId):
		current_player = self.current_player
		self.auction_value[propertyId] = self.getPropertyValue(propertyId,current_player)


	def getAuctionValue(self, propertyId):
		"""Returns the auction value"""
		auctionValue = 0
		if propertyId in self.auction_value:
			auctionValue = self.auction_value[propertyId]
			self.auction_value[propertyId].pop(propertyId, None)
		return auctionValue

	def find_number_of_houses(self, state, propertyId,current_player):
		"""
		Method returns number of houses on the given property Id and in case of hotel it will return 5.
		:param state:
		:param propertyId:
		:param current_player:
		:return:
		"""
		if current_player == 0:
			sign = 1
		else:
			sign = -1
		return state[self.PROPERTY_STATUS_INDEX][property] * sign - 1


	def selling_house_strategy(self, state, actual_debt):
		current_player = self.current_player
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		properties_with_houses = []
		for property in owned_properties:
			if self.find_number_of_houses(state, property, current_player) > 0:
				properties_with_houses.append(property)
		sorted_properties_worth = self.getValueForSellingHouses(properties_with_houses, self.current_player)
		totalNumberOfHouses = {}
		for property in sorted_properties_worth:
			if actual_debt <= 0:
				break
			#Find number of houses
			houses = self.find_number_of_houses(state, property, current_player)
			for i in range(1, houses):
				if actual_debt <= 0:
					break
				actual_debt -= constants.board[property]['build_cost'] * 0.5
				if property in totalNumberOfHouses:
					totalNumberOfHouses[property] = totalNumberOfHouses[property] + 1
				else:
					totalNumberOfHouses[property] =  1
		selling_list = []
		for property in totalNumberOfHouses:
			selling_list.append((property,totalNumberOfHouses[property]))
		if len(selling_list) > 0:
			return ("S", selling_list)
		else:
			return None

	def mortgaging_property_strategy(self, state, actual_debt):
		current_player = self.current_player
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		properties_with_zero_houses = []
		for property in owned_properties:
			if self.find_number_of_houses(state, property, current_player) == 0:
				properties_with_zero_houses.append(property)
		sorted_properties_worth = self.getValueForSellingHouses(properties_with_zero_houses, self.current_player)
		propertiesToMortgage = []
		for property in sorted_properties_worth:
			if actual_debt <= 0:
				break
			actual_debt -= constants.board[property]["price"] * 0.5
			propertiesToMortgage.append(property)

		if len(propertiesToMortgage) > 0:
			return ("M", propertiesToMortgage)
		else:
			return []



	def isPropertyWorthToBuy(self, state, current_player):
		"""Calculate the worth of the property and then return boolean true or false based on threshold"""
		pass


	def isDebtForBuyPropertyPhase(self, state):
		#Property id and source = 0 and debt
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
		# Need to decide strategy for this one/
		return False

	def buyProperty(self, state):
		property_id = state[self.PHASE_PAYLOAD_INDEX][0]
		if self.getAuctionValue(property_id) > 0: #This should decide whether I planned auction for this property in previous bmst.
			return False
		return True

	def auctionProperty(self, state):
		property_id = state[self.PHASE_PAYLOAD_INDEX][0]
		return self.getAuctionValue(property_id)

	def receiveState(self, state):
		JAIL = 6
		if state[self.PHASE_NUMBER_INDEX] == JAIL and state[self.PHASE_PAYLOAD_INDEX][0] == True:
			self.jail_counter = 0


	def isDanger(self, state, player):
		"""Compute the rent in 12 squares after Jail which I might need to pay"""
		rent = 0
		"""
		Expected Rent for Electric Company Utility
		"""
		if player == 0:
			if state[self.PROPERTY_STATUS_INDEX][12] == -1 and state[self.PROPERTY_STATUS_INDEX][28] == -1:
				rent = 20 #10*2(dice roll)
			elif state[self.PROPERTY_STATUS_INDEX][12] == -1:
				rent = 8
		else:
			if state[self.PROPERTY_STATUS_INDEX][12] == 1 and state[self.PROPERTY_STATUS_INDEX][28] == 1:
				rent = 20
			elif state[self.PROPERTY_STATUS_INDEX][12] == 1:
				rent = 8

		"""
		Expected Rent for Penn Rail Road
		"""
		if player == 0:
			if state[self.PROPERTY_STATUS_INDEX][15] == -1:
				count = 1
				for property in constants.board[15]["monopoly_group_elements"]:
					if state[self.PROPERTY_STATUS_INDEX][property] == -1:
						count = count + 1
				rent = count * 25
		else:
			if state[self.PROPERTY_STATUS_INDEX][15] == 1:
				count = 1
				for property in constants.board[15]["monopoly_group_elements"]:
					if state[self.PROPERTY_STATUS_INDEX][property] == 1:
						count = count + 1
				rent = count * 25
		position = state[self.PLAYER_POSITION_INDEX][player]
		property_owned_by_opponent = []

		if player == 0:
			opponent_sign = -1
		else:
			opponent_sign = 1

		for i in range(2, 12):
			if position + i != 12 and position + i != 15:
				if player == 0 and state[self.PROPERTY_STATUS_INDEX][position + i] < 0 and state[self.PROPERTY_STATUS_INDEX][position + i] != -7:
					property_owned_by_opponent.append(position + i)
				elif player == 1 and state[self.PROPERTY_STATUS_INDEX][position + i] > 0 and state[self.PROPERTY_STATUS_INDEX][position + i] != 7:
					property_owned_by_opponent.append(position+i)

		for property in property_owned_by_opponent:
			if state[self.PROPERTY_STATUS_INDEX][property] == -6 or state[self.PROPERTY_STATUS_INDEX][property] == 6:
				rent += constants.board[property]["rent_hotel"]
			elif state[self.PROPERTY_STATUS_INDEX][property] == -1 or state[self.PROPERTY_STATUS_INDEX][property] == 1:
				rent += constants.board[property]["rent"]
			else:
				s = "rent_house_"
				rent += constants.board[property][s + str(state[self.PROPERTY_STATUS_INDEX][property] * opponent_sign - 1)]
		#Current threshold 50 percent of the player money.
		if rent > 0.5 * state[self.PLAYER_CASH_INDEX][player]:
			return True
		return False

	def jailDecision(self, state):
		current_player = self.current_player
		if self.isDanger(state) and self.jail_counter < 2:
			self.jail_counter = self.jail_counter + 1
			return ("R")
		else:
			playerCash = state[self.PLAYER_CASH_INDEX][current_player]
			check_list = [1, -1]
			if state[self.PROPERTY_STATUS_INDEX][self.CHANCE_GET_OUT_OF_JAIL_FREE] == check_list[current_player]:
				return ("C", self.CHANCE_GET_OUT_OF_JAIL_FREE)
			elif state[self.PROPERTY_STATUS_INDEX][self.COMMUNITY_GET_OUT_OF_JAIL_FREE] == check_list[current_player]:
				return ("C", self.COMMUNITY_GET_OUT_OF_JAIL_FREE)
			elif playerCash >= 50:
				return ("P")
			else:
				return ("R")

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
