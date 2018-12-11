import constants
import itertools
import collections
import math


# Get property status
# Get player cash
# Current Player; Opponent Player
#

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
		self.bidthreshold = 0.7
		self.jail_counter = 0
		self.auction_value = {}
		# In a particular BMST phase, we can decide to buy houses and then unmortgage properties.
		# Adjudicator accept only one kind of action Buy or Mortgage at a time.
		# So, maintain this list when next time asked send this list.
		self.unmortgage_list = []
		self.unmortgageMoney = 0
		
		self.visitationFrequencies = [.0368, .0252, .0223, .0256, .0277, .0352, .0268, .0102, .0274, .0272, .0269,
									  .0321, .0310, .0281, .0293, .0346, .0331, .0307, .0349, .0366, .0343, .0336,
									  .0125, .0325, .0377, .0364, .0321, .0318, .0333, .0307, .0469, .0318, .0312,
									  .0282, .0297, .0289, .0102, .0260, .0260, .0312]
		
		self.diceThrowProbabalities = {
			1: 0 / 36,
			2: 1 / 36,
			3: 2 / 36,
			4: 3 / 36,
			5: 4 / 36,
			6: 5 / 36,
			7: 6 / 36,
			8: 5 / 36,
			9: 4 / 36,
			10: 3 / 36,
			11: 2 / 36,
			12: 1 / 36
		}
		
		#Orange,Light Blue,Red,Pink,Blue,Yellow,Green,Railroad,Brown,Utilities
		self.monopoly_code = {
			1:8,
			3:8,
			5:7,
			6:1,
			8:1,
			9:1,
			11:3,
			12:9,
			13:3,
			14:3,
			15:7,
			16:0,
			18:0,
			19:0,
			21:2,
			23:2,
			24:2,
			25:7,
			26:5,
			27:5,
			28:9,
			29:5,
			31:6,
			32:6,
			34:6,
			35:7,
			37:4,
			39:4
		}

	def getValueForSellingHouses(self, state, properties, player):
		# return [(property_id1, worth1), (property_id2, worth2 )]
		visitationFrequencies = self.visitationFrequencies
		diceThrowProbabalities = self.diceThrowProbabalities
		opponent = (player + 1) % 2
		opponentsPosition = state[self.PLAYER_POSITION_INDEX][opponent]
		reverse = True
		ballots = []

		for i in range(0, 4):
			ballot = []
			for propertyId in properties:
				space = constants.board[propertyId]
				propertyStatus = self.getPropertyStatus(state, propertyId)
				numberOfConstructions = abs(propertyStatus) - 1
				space = constants.board[propertyId]
				monopolyGroupElements = space["monopoly_group_elements"]

				if numberOfConstructions > 0:
					continue

				# decreasing order
				if i == 0:
					ballot.append((propertyId, visitationFrequencies[propertyId]))

				# decreasing order
				if i == 1:
					totalRent = self.getPropertyRent(propertyStatus, space)
					ballot.append((propertyId, totalRent))

				if i == 2:
					if not self.canConstructOnProperty(state, space, propertyStatus,self.current_player):
						continue

					currentPropertyRent = self.getPropertyRent(propertyStatus, space)
					potentialRentIfConstructed = self.getPropertyRent(propertyStatus + 1, space)
					increaseInRent = potentialRentIfConstructed - currentPropertyRent
					ballot.append((propertyId, increaseInRent))

				# decreasing order
				# jail condition; treat as 10
				if i == 3:
					if opponentsPosition == -1:
						opponentsPosition = 10

					diff = propertyId - opponentsPosition

					if diff < 0:
						diff += 40

					probabilityOfLanding = diceThrowProbabalities[diff]

					if not probabilityOfLanding:
						probabilityOfLanding = 0

					ballot.append((propertyId, probabilityOfLanding))

			if len(ballot):
				ballot = sorted(ballot, key=lambda x: x[1], reverse=reverse)
				ballot = [vote[0] for vote in ballot]
				ballotOrder = []
				for index in range(0, len(ballot) - 1):
					comparisionOperator = ">"
					if ballot[index] == ballot[index + 1]:
						comparisionOperator = "="
					ballotOrder.append(ballot[index])
					ballotOrder.append(comparisionOperator)
					ballotOrder.append(ballot[index + 1])

				ballotOrder = "".join(ballotOrder)
				ballots.append(ballot)

		ballots = self.rank(ballots)
		orderedProperties = [int(ballot) for ballot in ballots]
		return orderedProperties

	# taken from https://stackoverflow.com/questions/9242450/borda-count-using-python
	def rank(self, ballots):
		def borda(ballot):
			n = len([c for c in ballot if c.isalpha()]) - 1
			score = itertools.count(n, step=-1)
			result = {}
			for group in [item.split('=') for item in ballot.split('>')]:
				s = sum(next(score) for item in group) / float(len(group))
				for pref in group:
					result[pref] = s
			return result

		def tally():
			result = collections.defaultdict(int)
			for ballot in ballots:
				for pref, score in borda(ballot).items():
					result[pref] += score
			result = dict(result)
			return result

		if len(ballots):
			return list(tally())

		return []

	def getPropertyStatus(self, state, propertyId):
		return state[self.PROPERTY_STATUS_INDEX][propertyId]

	def updatePropertyStatus(self, state, propertyId, propertyStatus):
		mappingId = constants.space_to_property_map[propertyId]
		self.updateState(state, self.PROPERTY_STATUS_INDEX, mappingId, propertyStatus)

	def getPlayerCash(self, state, player):
		return state[self.PLAYER_CASH_INDEX][player]

	def doIOwn(self, propertyStatus, id):
		if id == 0 and propertyStatus <= 0:
			return False
		if id == 1 and propertyStatus >= 0:
			return False

		return True

	def getPropertyRent(self, propertyStatus, space):
		numberOfConstructions = abs(propertyStatus) - 1
		totalRent = 0
		for i in range(1, numberOfConstructions):
			key = i
			if i == 5:
				key = "hotel"

			totalRent += space["rent_house_" + key]

		return totalRent

	def getTotalNumberOfConstructions(self, state):
		numberOfHouses = 0
		numberOfHotels = 0

		for propertyStatus in state[self.PROPERTY_STATUS_INDEX]:
			propertyStatus = abs(propertyStatus)

			if propertyStatus > 1 and propertyStatus < 6:
				numberOfHouses += propertyStatus
			if propertyStatus == 6:
				numberOfHotels += 1

		return (numberOfHouses, numberOfHotels)

	"""
	Used to decide if we can build houses on these properties
	"""

	def doIOwnMonopoly(self, state, monopolyGroupElements, player):

		for monopolyGroupElement in monopolyGroupElements:
			monopolyGroupElementStatus = self.getPropertyStatus(state, monopolyGroupElement)
			if not self.doIOwn(monopolyGroupElementStatus, player):
				return False

		return True

	def canConstructOnProperty(self, state, space, propertyStatus, player,shouldAllowHotels=True):

		monopolyGroupElements = space["monopoly_group_elements"]

		if space["class"] != "Street":
			return False

		if not self.doIOwn(propertyStatus,player):
			return False

		if not self.doIOwnMonopoly(state, monopolyGroupElements, player):
			return False

		currentConstructionCount = abs(propertyStatus) - 1
		(numberOfHouses, numberOfHotels) = self.getTotalNumberOfConstructions(state)
		
		if currentConstructionCount >= 5:
			return False

		# the agent intends to build a hotel
		if currentConstructionCount == 4 and numberOfHotels == 12 and not shouldAllowHotels:
			return False

		if currentConstructionCount > 0 and currentConstructionCount < 5 and numberOfHouses == 32:
			return False

		# diff between current and rest should never be more than one
		for monopolyGroupElement in monopolyGroupElements:
			monopolyGroupElementStatus = self.getPropertyStatus(state, monopolyGroupElement)
			numberOfConstructionsInGroupElement = abs(monopolyGroupElementStatus) - 1
			if currentConstructionCount > numberOfConstructionsInGroupElement:
				return False

		return True

	def getPercentageMonopolyOwned(self, state, propertyStatus, space, player):
		monopolyGroupElements = space["monopoly_group_elements"]

		if len(monopolyGroupElements) == 0:
			return 0

		ownedCount = 0

		for monopolyGroupElement in monopolyGroupElements:
			groupElementPropertyStatus = self.getPropertyStatus(state, monopolyGroupElement)
			if ((player == 0 and groupElementPropertyStatus > 0) or (player == 1 and groupElementPropertyStatus < 0)):
				ownedCount += 1

		ownedPercentage = ownedCount / len(monopolyGroupElements)
		return ownedPercentage

	def getValueForMortgageProperties(self, state, properties, player):
		visitationFrequencies = self.visitationFrequencies
		diceThrowProbabalities = self.diceThrowProbabalities
		opponent = (player + 1) % 2
		opponentsPosition = state[self.PLAYER_POSITION_INDEX][opponent]
		reverse = True
		ballots = []

		for i in range(0, 5):
			ballot = []
			for propertyId in properties:
				space = constants.board[propertyId]
				propertyStatus = self.getPropertyStatus(state, propertyId)
				numberOfConstructions = abs(propertyStatus) - 1
				space = constants.board[propertyId]
				monopolyGroupElements = space["monopoly_group_elements"]

				if numberOfConstructions > 0:
					continue

				if self.doIOwnMonopoly(state, monopolyGroupElements, id):
					continue

				# decreasing order
				if i == 0:
					ballot.append((propertyId, visitationFrequencies[propertyId]))

				# decreasing order
				if i == 1:
					totalRent = self.getPropertyRent(propertyStatus, space)
					ballot.append((propertyId, totalRent))

				# decreasing order
				if i == 2:
					ownedPercentage = self.getPercentageMonopolyOwned(state, propertyStatus, space, id)
					ballot.append((propertyId, ownedPercentage))

				# increasing order
				# actually
				if i == 3:
					reverse = False
					ownedPercentage = self.getPercentageMonopolyOwned(state, propertyStatus, space, opponent)
					ballot.append((propertyId, ownedPercentage))

				# decreasing order
				# jail condition; treat as 10
				if i == 4:
					if opponentsPosition == -1:
						opponentsPosition = 10

					diff = propertyId - opponentsPosition

					if diff < 0:
						diff += 40

					probabilityOfLanding = diceThrowProbabalities[diff]

					if not probabilityOfLanding:
						probabilityOfLanding = 0

					ballot.append((propertyId, probabilityOfLanding))

			if len(ballot):
				ballot = sorted(ballot, key=lambda x: x[1], reverse=reverse)
				ballot = [vote[0] for vote in ballot]
				ballotOrder = []
				for index in range(0, len(ballot) - 1):
					comparisionOperator = ">"
					if ballot[index] == ballot[index + 1]:
						comparisionOperator = "="
					ballotOrder.append(ballot[index])
					ballotOrder.append(comparisionOperator)
					ballotOrder.append(ballot[index + 1])

				ballotOrder = "".join(ballotOrder)
				ballots.append(ballot)

		ballots = self.rank(ballots)
		orderedProperties = [int(ballot) for ballot in ballots]
		return orderedProperties

	def isPropertyWorthToBuy(self, state, propertyId, currentPlayer):
		"""Calculate the worth of the property and then return boolean true or false"""
		"""This method is same as getValueForBuying in our doc"""

		opponent = (currentPlayer + 1) % 2
		space = constants.board[propertyId]
		propertyPrice = space["price"]
		opponentCash = self.getPlayerCash(state, opponent)
		propertyStatus = self.getPropertyStatus(state, propertyId)
		if propertyPrice > opponentCash:
			return False

		currentPlayerMonopolyPercent = self.getPercentageMonopolyOwned(state, propertyStatus, space, id)
		opponentPlayerMonopolyPercent = self.getPercentageMonopolyOwned(state, propertyStatus, space, opponent)

		if currentPlayerMonopolyPercent == 0 and opponentPlayerMonopolyPercent > 0:
			return True

		if currentPlayerMonopolyPercent >= 0 and opponentPlayerMonopolyPercent == 0:
			return True

		return False
	   
	"""
	Used while unmortgaging. If the property completes a monopoly, it should be unmortgaged first
	"""
	def getMortgagedPropertiesThatCompleteMonopolies(self,state,mortgageCandidates):
		propSign = self.get_property_sign(self.current_player)
		selectedProps = []
		
		for propertyId in mortgageCandidates:
			if propertyId in selectedProps:
				#Already been selected
				continue
			
			monopolies = constants.board[propertyId]['monopoly_group_elements']
			flag = True
			mortgagedMonopolyElements = []
			for monopoly in monopolies:
				#This would mean current player doesnt owns the property
				#If the property is mortgaged, can be unmortgaged
				if self.getPropertyStatus(state, monopoly)*propSign<=0:
					flag = False
				elif self.getPropertyStatus(state, monopoly)*propSign==7:
					mortgagedMonopolyElements.append(monopoly)
			
			if flag:
				selectedProps.append(propertyId)
				if len(mortgagedMonopolyElements)!=0:
					selectedProps.extend(mortgagedMonopolyElements)
			
		return selectedProps
	
	
	"""
	Uses bordas to get sorted set of propids for unmortgaging scenario
	"""
	def checkBordasForUnmortgaging(self,state,mortgageCandidates):
		for propertyId in mortgageCandidates:
			space = constants.board[propertyId]
			propertyStatus = self.getPropertyStatus(state, propertyId)
		
			potentialRentIfUnmortgaged = self.getPropertyRent(1, space)
			delta = potentialRentIfConstructed
			ballots.append((propertyId, delta))
		
		ballots = sorted(ballots, key=lambda x: x[1], reverse=True)
		orderedProperties = [int(ballot[0]) for ballot in ballots]
		return orderedProperties

	# call this method seperately for buying and umortgaging
	def getValueForBuyingConstructionsorUnmortgaging(self, state, buyHousesCandidates, mortgageCandidates, player):
		"""
		Passing buyHousesCandidates and mortgageCandidates separately to avoid parsing state in this method.
		Return value can still be single list with tuples of propertyId.
		If houses can be constructed anywhere, that takes precedence over unmortgaging.
		Except in the case where unmortgaging opens up a new completed monopoly where houses can be built.
		List returned should either consist fully of properties where hosues can be built or which can be unmortgaged
		Take into account
		"""
		ballots = []
		
		if len(buyHousesCandidates)!=0:
			#Buying houses
			for propertyId in buyHousesCandidates:
				space = constants.board[propertyId]
				propertyStatus = self.getPropertyStatus(state, propertyId)
			
				if not self.canConstructOnProperty(state, space, propertyStatus,self.current_player):
					continue
				
				monopolyCode = self.monopoly_code[propertyId]
				ballots.append((propertyId, monopolyCode))
			
			ballots = sorted(ballots, key=lambda x: x[1], reverse=True)
			orderedProperties = [int(ballot[0]) for ballot in ballots]
			return orderedProperties
		else:
			#Unmortgaging
			compMonopolyUnmortgagableProps = self.getMortgagedPropertiesThatCompleteMonopolies(state,mortgageCandidates)
			otherProps = [x for x in mortgageCandidates if x not in compMonopolyUnmortgagableProps]
			otherProps_sorted = checkBordasForUnmortgaging(otherProps)
			return compMonopolyUnmortgagableProps + otherProps

	def respondTrade(self, state):
		# Need to decide strategy for this one/
		return False

	def getBSMTDecision(self, state):
		debt = self.parseDebt(state, self.current_player)[1]
		money = state[self.PLAYER_CASH_INDEX][self.current_player]
		
		#Position is in jail and jail counter is 2 then debt = 50
		position = state[self.PLAYER_POSITION_INDEX][self.current_player]
		if self.jail_counter == 2:
			debt = 50
		
		if debt == 0:
			(action,moneyNeeded,propList) = self.buying_houses_or_unmortgaging_strategy(state)
			if (action=="B" or action=="M") and moneyNeeded <= money and len(propList) > 0:
				return (action, propList)

		elif debt > 0 and debt > money:
			actual_debt = debt - money
			if self.isDebtForBuyPropertyPhase(state):
				property_id = state[self.PHASE_PAYLOAD_INDEX]
				if self.isPropertyWorthToBuy(state, property_id, self.current_player):
					mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt, constants.board[property_id]["monopoly_group_elements"])
					if len(mortgaged_property_ids) != 0:
						return mortgaged_property_ids
			else:
				mortgaged_property_ids = self.mortgaging_property_strategy(state, actual_debt)
				if len(mortgaged_property_ids) != 0:
					return mortgaged_property_ids
				elif actual_debt >= 0:
					"""
					Added below method for the scenario when there is debt and we can mortgage property
					in completed monopoly.
					"""
					mproperties = self.getMortgageStrategyinExtremeCases(state, actual_debt)
					if len(mproperties) != 0:
						return mproperties;
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
	def getPropertyValue(self, state, propertyId, player):

		space = constants.board[propertyId]
		propertyPrice = space["price"]
		return propertyPrice * 0.7

	def storeAuctionValue(self, state, propertyId):
		"""
		Deprecated
		"""
		current_player = self.current_player
		self.auction_value[propertyId] = self.getPropertyValue(state, propertyId, current_player)

	def getAuctionValue(self, propertyId):
		"""Deprecated: Returns the auction value"""
		auctionValue = 0
		if propertyId in self.auction_value:
			auctionValue = self.auction_value[propertyId]
			self.auction_value.pop(propertyId, None)
		return auctionValue

	def find_number_of_houses(self, state, propertyId, current_player):
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
		return state[self.PROPERTY_STATUS_INDEX][propertyId] * sign - 1

	def selling_house_strategy(self, state, actual_debt):
		current_player = self.current_player
		owned_properties = self.get_mortgagable_properties(state, self.current_player)
		properties_with_houses = []
		for property in owned_properties:
			if self.find_number_of_houses(state, property, current_player) > 0:
				properties_with_houses.append(property)
		if len(properties_with_houses) == 0:
			return None

		sorted_properties_worth = self.getValueForSellingHouses(state, properties_with_houses, self.current_player)
		totalNumberOfHouses = {}
		for property in sorted_properties_worth:
			if actual_debt <= 0:
				break
			# Find number of houses
			houses = self.find_number_of_houses(state, property, current_player)
			for i in range(1, houses):
				if actual_debt <= 0:
					break
				actual_debt -= constants.board[property]['build_cost'] * 0.5
				if property in totalNumberOfHouses:
					totalNumberOfHouses[property] = totalNumberOfHouses[property] + 1
				else:
					totalNumberOfHouses[property] = 1
		selling_list = []
		for property in totalNumberOfHouses:
			selling_list.append((property, totalNumberOfHouses[property]))
		if len(selling_list) > 0:
			return ("S", selling_list)
		else:
			return None

	def getMortgageStrategyinExtremeCases(self, state, actual_debt):
		owned_properties = self.get_mortgagable_properties(state, self.current_player)
		properties = self.getPropertyWithZeroHouses(state, owned_properties)
		propertiesToMortgage = []
		for property in properties:
			if actual_debt <= 0:
				break
			actual_debt -= constants.board[property]["price"] * 0.5
			propertiesToMortgage.append(property)

		if len(propertiesToMortgage) > 0:
			return ("M", propertiesToMortgage)
		else:
			return []


	def getPropertyWithZeroHouses(self, state, properties):
		properties_with_zero_houses = []
		for property in properties:
			if self.find_number_of_houses(state, property, self.current_player) == 0:
				properties_with_zero_houses.append(property)
		return properties_with_zero_houses


	def mortgaging_property_strategy(self, state, actual_debt, exclusion_list=[]):
		current_player = self.current_player
		properties = self.get_mortgagable_properties(state, self.current_player)
		owned_properties = []
		for property in properties:
			if property not in exclusion_list:
				owned_properties.append(property)
		properties_with_zero_houses = self.getPropertyWithZeroHouses(state, owned_properties)
		sorted_properties_worth = self.getValueForMortgageProperties(state, properties_with_zero_houses,
																	 self.current_player)
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

	def isDebtForBuyPropertyPhase(self, state):
		"""
		Check if debt is for buy property by checking if source of debt is bank and property status of
		player position is zero.
		:param state:
		:return: True or False
		"""
		tuple = self.parseDebt(state, self.current_player)
		position = state[self.PLAYER_POSITION_INDEX][self.current_player]
		if constants.board[position]["class"] != "Street" or constants.board[position]["class"] != "Utility" or \
						constants.board[position]["class"] != "Railroad":
			return False
		if tuple[0] == 0 and state[self.PROPERTY_STATUS_INDEX][position] == 0:
			return True
		return False

	"""
	Returns the rent from the top 3 properties of the opponent in the next x places from the current position
	"""
	def expectedRentNextNPlaces(self,state,x=12,topX=3):
		currentPosition = state[self.PLAYER_POSITION_INDEX][self.current_player]
		totalRent = 0
		rents = []
		propSign = self.get_property_sign(self.current_player)
		
		for j in range(currentPosition+2,currentPosition+x):
			i = j%40
			dice_sum = (j-currentPosition)
			rent = 0
			
			if constants.board[i]['class']=='Utility':
				"""
				Expected Rent for Electric Company Utility
				"""
				if state[self.PROPERTY_STATUS_INDEX][12]*propSign == -1 and state[self.PROPERTY_STATUS_INDEX][28]*propSign == -1:
					rent = 10*dice_sum
				elif state[self.PROPERTY_STATUS_INDEX][12]*propSign == -1:
					rent = 4*dice_sum
			elif constants.board[i]['class']=='Railroad':
				"""
				Expected Rent for Rail Road
				"""
				if state[self.PROPERTY_STATUS_INDEX][i]*propSign == -1:
					rent = 25
					for property in constants.board[i]["monopoly_group_elements"]:
						if state[self.PROPERTY_STATUS_INDEX][property]*propSign == -1:
							rent *= 2
					
			elif constants.board[i]['class']=='Street':
				propStatus = self.getPropertyStatus(state, i)
				if propStatus*propSign == -1:
					#Also check for completed monopoly here
					flag = True
					for monopoly in constants.board[i]['monopoly_group_elements']:
						monopolyStatus = self.getPropertyStatus(state, monopoly)
						if monopolyStatus*propSign >= 0:
							flag = False
							break
					
					rent = constants.board[i]['rent']
					if flag:
						rent = rent*2
				elif propStatus*propSign == -6:
					rent = constants.board[i]["rent_hotel"]
				elif propStatus*propSign < -1 and propStatus*propSign > -7:
					s = "rent_house_"
					rent = constants.board[i][s + str( (propStatus*propSign*-1)-1 )]
			
			rents.append(rent)
		
		rents = sorted(rents,reverse=True)
		for i in range(topX):
			totalRent += rents[i]
		return math.ceil(totalRent)
	
	"""
	Returns the min amount of cash the player should keep with him.
	Should Ideally be determined by the expected rent in the next 12 places.
	"""   
	def getMinCash(self,state):
		return self.expectedRentNextNPlaces(state)

	def getCashReserve(self, state):
		mortgagable_properties = self.get_mortgagable_properties(state, self.current_player)
		wealth = 0
		for mortgagable_property in mortgagable_properties:
			wealth += (constants.board[mortgagable_property]['price'] / 2)
		return wealth
	
	"""
	Get the list of properties where we can buy houses
	"""
	def get_buying_house_candidates(self,state):
		candidate_properties_for_building_houses = []
		for i in range(1,40):
			status = state[self.PROPERTY_STATUS_INDEX][i]
			propClass = constants.board[i]["class"]
			if propClass != "Street":
				continue

			propSign = self.get_property_sign(self.current_player)
			if (status * propSign >= 1):
				houses = self.find_number_of_houses(state, i, self.current_player)
				if houses <= 4:  # discarding building hotel on property
					isValidCandidate = True
					monopoly_group_properties = constants.board[i]["monopoly_group_elements"]
					for other_property in monopoly_group_properties:
						otherStatus = state[self.PROPERTY_STATUS_INDEX][other_property]
						if (otherStatus * propSign < 1):
							isValidCandidate = False
							break
							
						other_houses = self.find_number_of_houses(state, other_property, self.current_player)
						if houses > other_houses:
							isValidCandidate = False
							break
					if isValidCandidate:
						candidate_properties_for_building_houses.append(i)
		return candidate_properties_for_building_houses
	
	"""
	During a given BSMT, the function should only return either building houses/mortgaging.
	No point in returning both
	so, function return syntax: ("B/M",props,cash_needed)
	"""
	def buying_houses_or_unmortgaging_strategy(self, state):
		# It should evaluate the buying house and unmortgaging property as an atomic action and then return a decision.
		# Calculate worth of both the actions by calculating the increase in rent and then return.
		cash = self.getPlayerCash(state, self.current_player)
		reserveWealth = self.getCashReserve(state)
		
		RESERVEWEALTH_THRESHOLD = 0.7
		THRESHOLD_CASH = self.getMinCash(state)
		threshold_wealth = cash - THRESHOLD_CASH
		
		"""Decide to buy houses or unmortgaging based on threshold wealth"""
		candidate_properties_for_building_houses = self.get_buying_house_candidates(state)
		
		
		mortgaged_properties = self.get_mortgaged_properties(state, self.current_player)
		if len(candidate_properties_for_building_houses + mortgaged_properties) == 0:
			return ("",0,[])
		
		sorted_worth_properties = self.getValueForBuyingConstructionsorUnmortgaging(state,
			candidate_properties_for_building_houses,mortgaged_properties,self.current_player)
		
		moneyNeeded = 0
		propList = []
		action = ""
		for property in sorted_worth_properties:
			#Check for theshold here
			#expecting the sorted worth properties to have properties of same monopoly together
			if property in candidate_properties_for_building_houses:
				action = "B"
				currentMonopolyDict = {}
				
				buildcost = constants.board[property]['build_cost']
				threshold_wealth -= buildcost
				if threshold_wealth >= 0:
					moneyNeeded += buildcost
					currentMonopolyDict[property] = 1
					candidate_properties_for_building_houses.remove(property)
				else:
					break
					
				#We will now build on this property and the other properties in the 
				#same monopoly provided they are also in the list.
				breakFlag = False
				monopoly_elems = constants.board[property]['monopoly_group_elements']
				for monopoly_elem in monopoly_elems:
					if monopoly_elem in candidate_properties_for_building_houses:
						buildcost = constants.board[property]['build_cost']
						threshold_wealth -= buildcost
						if threshold_wealth >= 0:
							moneyNeeded += buildcost
							currentMonopolyDict[monopoly_elem] = 1
							candidate_properties_for_building_houses.remove(monopoly_elem)
						else:
							breakFlag = True
							break
				if breakFlag:
					break
				
				#At this point, we have built houses evenly on this monopoly.
				#Now, we can build on all three.
				while threshold_wealth-buildcost>=0:
					for key in currentMonopolyDict:
						space = constants.board[key]
						propertyStatus = self.getPropertyStatus(state, key)
						if threshold_wealth-buildcost >= 0 and self.canConstructOnProperty(state, space, propertyStatus,self.current_player,shouldAllowHotels=False):
							moneyNeeded += buildcost
							threshold_wealth-=buildcost
							currentMonopolyDict[key]+=1
				
				for entry in currentMonopolyDict:
					propList.append((entry,currentMonopolyDict[entry]))
				
			elif property in mortgaged_properties:
				action = "M"
				unmortgageCost = constants.board[property]['price'] * 0.5* 1.1
				threshold_wealth -= unmortgageCost
				if threshold_wealth >= 0:
					propList.append(property)
					moneyNeeded += unmortgageCost
		
		return (action,moneyNeeded,propList)

	def buyProperty(self, state):
		property_id = state[self.PHASE_PAYLOAD_INDEX]
		propertyPrice = constants.board[property_id]['price']
		current_player = self.current_player
		current_player_money = state[self.PLAYER_CASH_INDEX][current_player]
		propertyValue = self.getPropertyValue(state,property_id, current_player)
		isPropertyWorthy = self.isPropertyWorthToBuy(state, property_id, self.current_player)
		if (not isPropertyWorthy) or propertyValue < current_player_money or current_player_money < propertyPrice: # This should decide whether I planned auction for this property in previous bmst.
			return False
		return True

	def auctionProperty(self, state):
		property_id = state[self.PHASE_PAYLOAD_INDEX][0]
		playerPosition = state[self.PHASE_PAYLOAD_INDEX][0]
		propertyPrice = constants.board[playerPosition]['price']
		current_player = self.current_player
		current_player_money = state[self.PLAYER_CASH_INDEX][current_player]
		propertyValue = self.getPropertyValue(state,property_id, current_player)

		if current_player == 0:
			opponent_money = state[self.PLAYER_CASH_INDEX][1]
		else:
			opponent_money = state[self.PLAYER_CASH_INDEX][0]

		if propertyPrice > opponent_money and current_player_money > (opponent_money + 1) and propertyValue > opponent_money:
			return opponent_money + 1

		if current_player_money > propertyValue:
			return propertyValue
		else:
			return current_player_money * self.bidthreshold

	def receiveState(self, state):
		JAIL = 6
		if state[self.PHASE_NUMBER_INDEX] == JAIL and state[self.PHASE_PAYLOAD_INDEX][0] == True:
			self.jail_counter = 0

	def isDanger(self, state, player):
		rent = self.expectedRentNextNPlaces(state, x=40)
		# Current threshold 50 percent of the player money.
		if rent > state[self.PLAYER_CASH_INDEX][player]:
			return True
		return False

	def jailDecision(self, state):
		current_player = self.current_player
		self.jail_counter = self.jail_counter + 1
		
		if self.isDanger(state, current_player) and self.jail_counter < 3:
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

	"""
	Returns the sign of the property as per ownership
	"""
	def get_property_sign(self, current_player):
		if current_player == 0:
			return 1
		elif current_player == 1:
			return -1

	"""
	Gets the list of properties which can be mortgaged.
	"""
	def get_mortgagable_properties(self, state, current_player):
		owned_properties = []
		for i in range(1,40):
			status = state[self.PROPERTY_STATUS_INDEX][i]
			propClass = constants.board[i]["class"]
			if propClass != "Street" and propClass != "Utility" and propClass != "Railroad":
				continue

			propSign = self.get_property_sign(current_player)
			if (status * propSign == 1) and i in constants.property_to_space_map:
				monopolies = constants.board[i]['monopoly_group_elements']
				flag = True
				for monopoly in monopolies:
					if self.getPropertyStatus(state,monopoly) * propSign > 1:
						# its either mortgaged or has a house
						flag = False
						break
				if flag:
					owned_properties.append(i)
		return owned_properties

	def get_mortgaged_properties(self, state, current_player):
		owned_properties = []
		for i in range(1,40):
			status = state[self.PROPERTY_STATUS_INDEX][i]
			if constants.board[i]["class"] != "Street" and constants.board[i]["class"] != "Utility" and constants.board[i]["class"] != "Railroad":
				continue
			if current_player == 0 and status == 7 and i in constants.property_to_space_map:
				owned_properties.append(i)
			elif current_player == 1 and status == -7 and i in constants.property_to_space_map:
				owned_properties.append(i)
		
		return owned_properties
