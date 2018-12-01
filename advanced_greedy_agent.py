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
		# In a particular BMST phase, we can decide to buy houses and then unmortgage properties.
		# Adjudicator accept only one kind of action Buy or Mortgage at a time.
		# So, maintain this list when next time asked send this list.
		self.unmortgage_list = []
		self.unmortgageMoney = 0

		self.visitationFrequencies = [.0368, .0252, .0223, .0256, .0277, .0352, .0268, .0102, .0274, .0272, .0269, .0321, .0310, .0281, .0293, .0346, .0331, .0307, .0349, .0366, .0343, .0336, .0125, .0325, .0377, .0364, .0321, .0318, .0333, .0307, .0469, .0318, .0312, .0282, .0297, .0289, .0102, .0260, .0260, .0312]

		self.diceThrowProbabalities = {
		  1 : 0/36,
		  2 : 1/36,
		  3 : 2/36,
		  4 : 3/36,
		  5 : 4/36,
		  6 : 5/36,
		  7 : 6/36,
		  8 : 5/36,
		  9 : 4/36,
		  10 : 3/36,
		  11 : 2/36,
		  12 : 1/36
		}

	def getValueForSellingHouses(self, state, properties, player):
		#return [(property_id1, worth1), (property_id2, worth2 )]
		pass
	def getValueForMortgageProperties(self, state, properties, player):
		#return [(property_id1, worth1), (property_id2, worth2 )]
		# 
		# currentPlayerPosition = state[PLAYER_POSITION_INDEX][(player-1)%2]
		# otherPlayerPosition = state[PLAYER_POSITION_INDEX][player%2]
		# currentPlayerVisitationFrequency = visitationFrequencies[currentPlayerPosition]
		# currentPlayerVisitationFrequency = visitationFrequencies[currentPlayerPosition]
		result = []
		visitationFrequencies = self.visitationFrequencies
		diceThrowProbabalities = self.diceThrowProbabalities
		
		for i in range(0,5):
			votes = []
			for propertyId in properties:

				if i == 0:
					#votes visitation frequency
					votes.append(visitationFrequencies[propertyId])
				if i == 1:
					# "rent_house_1":10,
					# "rent_house_2":30,
					# "rent_house_3":90,
					# "rent_house_4":160,
					# "rent_hotel":250,

					pass
				if i == 2:
					# monopoly owned by you 
					pass

				if i == 3:
					# by opponent 
					pass

				if i == 4 :
					pass
		
		pass

	def isPropertyWorthToBuy(self, state, property_id, current_player):
		"""Calculate the worth of the property and then return boolean true or false"""
		"""This method is same as getValueForBuying in our doc"""
		pass

	def getValueForBuyingConstructionsorUnmortgaging(self, state, buyHousesCandidateProperties, mortgageCandidateProperties, player):
		"""Passsing buyHousesCandidates and mortgageCandidates separately to avoid parsing state in this method.
		   If this is not helpful, remove it. Return value can still be single list with tuples of propertyId and worth.
		"""
		# return [(property_id1, worth1), (property_id2, worth2 )]
		pass

	def respondTrade(self, state):
		# Need to decide strategy for this one/
		return False

	def getBSMTDecision(self, state):
		debt = self.parseDebt(state, self.current_player)[1]
		money = state[self.PLAYER_CASH_INDEX][self.current_player]
		if debt == 0:
			if len(self.unmortgage_list) == 0:
				(money_building,properties_houses, money_unmort, properties_unmort) = self.buying_houses_or_unmortgaging_strategy(state)
				if money_building <= money and len(properties_houses) > 0:
					self.unmortgage_list = properties_unmort
					self.unmortgageMoney = money_unmort
					return ("B", properties_houses)
				elif money_unmort <= money and len(properties_unmort) > 0:
					return ("M", properties_unmort)
			else:
				if self.unmortgageMoney <= money and len(self.unmortgage_list) > 0:
					unmortagageProperties = self.unmortgage_list
					self.unmortgage_list = []
					self.unmortgageMoney = 0
					return ("M", unmortagageProperties)
			#else:
			#	mortgaged_property_ids = self.mortgaging_property_strategy(state, total_money_required - money)
			#	if len(mortgaged_property_ids) != 0:
			#		return mortgaged_property_ids

		elif debt > 0 and debt > money:
			actual_debt = debt - money

			if self.isDebtForBuyPropertyPhase(state):
				property_id = state[self.PHASE_PAYLOAD_INDEX][0]
				if self.isPropertyWorthToBuy(state, property_id, self.current_player):
					mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt)
					if len(mortgaged_property_ids) != 0:
						return mortgaged_property_ids
					else:
						selling_number_pf_houses_for_properties = self.selling_house_strategy(state, actual_debt)
						return selling_number_pf_houses_for_properties
				else:
					self.storeAuctionValue(state, property_id)
			else:
				mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt)
				if len(mortgaged_property_ids) != 0:
					return mortgaged_property_ids
				else:
					selling_number_pf_houses_for_properties = self.selling_house_strategy(state, actual_debt)
					return selling_number_pf_houses_for_properties
		return None
	
	"""
	This method estimates how much a property is worth to the given player.
	Factors:
	Short term probability of the opponent falling on the property
	Number of Properties I own in the monopoly group of the current property
	Visitation Frequency of the property*(Rent from the property)
	"""
	def getPropertyValue(self, state, properties, player):
		pass

	def storeAuctionValue(self, state, propertyId):
		current_player = self.current_player
		self.auction_value[propertyId] = self.getPropertyValue(state, propertyId,current_player)


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
		sorted_properties_worth = self.getValueForSellingHouses(state, properties_with_houses, self.current_player)
		totalNumberOfHouses = {}
		for property, worth in sorted_properties_worth:
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
		sorted_properties_worth = self.getValueForMortgageProperties(state, properties_with_zero_houses, self.current_player)
		propertiesToMortgage = []
		for property, worth in sorted_properties_worth:
			if actual_debt <= 0:
				break
			actual_debt -= constants.board[property]["price"] * 0.5
			propertiesToMortgage.append(property)

		if len(propertiesToMortgage) > 0:
			return ("M", propertiesToMortgage)
		else:
			return []

	def isDebtForBuyPropertyPhase(self, state):
		"""
		Check if debt is for buy property by checking if source of debt is bank and property status of
		player position is zero.
		:param state:
		:return: True or False
		"""
		tuple = self.parseDebt(state, self.current_player)
		position = state[self.PLAYER_POSITION_INDEX][self.current_player]
		if tuple[0] == 0 and state[self.PROPERTY_STATUS_INDEX][position] == 0:
			return True
		return False

	def estimateWealth(self,state):
		return state[self.PLAYER_CASH_INDEX][self.current_player]

	def buying_houses_or_unmortgaging_strategy(self, state):
		#It should evaluate the buying house and unmortgaging property as an atomic action and then return a decision.
		#Calculate worth of both the actions by calculating the increase in rent and then return.
		wealth = self.estimateWealth(state)
		threshold_wealth = self.threshold * wealth

		"""Decide to buy houses or unmortgaging based on threshold wealth"""
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		candidate_properties_for_building_houses = []
		for property in owned_properties:
			houses = self.find_number_of_houses(state, property, self.current_player)
			if houses <= 4 : #discarding building hotel on property
				isValidCandidate = True
				monopoly_group_properties = constants.board[property]["monopoly_group_elements"]
				for other_property in monopoly_group_properties:
					if other_property not in owned_properties:
						isValidCandidate = False
						break

					other_houses = self.find_number_of_houses(state, other_property, self.current_player)
					if houses > other_houses:
						isValidCandidate = False
						break
				if isValidCandidate:
					candidate_properties_for_building_houses.append(property)

		mortgaged_properties = self.get_mortgaged_properties(state, self.current_player)
		sorted_worth_properties = self.getValueForBuyingConstructionsorUnmortgaging(state,candidate_properties_for_building_houses,mortgaged_properties,self.current_player)
		buyingHouses_list = []
		unmortgage_list = []
		buyingHousesMoney = 0
		unmortgageMoney = 0
		for property, worth in sorted_worth_properties:
			if threshold_wealth <= 0:
				break
			elif property in candidate_properties_for_building_houses:
				buildcost = constants.board[property]['build_cost']
				threshold_wealth -= buildcost
				if threshold_wealth >= 0:
					buyingHouses_list.append(property)
					buyingHousesMoney += buildcost
			elif property in mortgaged_properties:
				unmortgageCost = constants.board[property]['price']* 0.5 + 0.1 * 0.5 * constants.board[property]['price']
				threshold_wealth -= unmortgageCost
				if threshold_wealth >= 0:
					unmortgage_list.append(property)
					unmortgageMoney += unmortgageCost

		return (buyingHousesMoney, buyingHouses_list, unmortgageMoney, unmortgage_list)

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
			if constants.board[i]["class"] != "Street":
				continue
			if current_player == 0 and status > 0 and status != 7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			elif current_player == 1 and status < 0 and status != -7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			i = i + 1
		return owned_properties

	def get_mortgaged_properties(self, state, current_player):
		owned_properties = []
		i = 0
		for status in state[self.PROPERTY_STATUS_INDEX]:
			if constants.board[i]["class"] != "Street":
				continue
			if current_player == 0 and status == 7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			elif current_player == 1 and status == -7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			i = i + 1
		return owned_properties
