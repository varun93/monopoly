import RL_Agent.rl_agent as buddy
import RL_Agent.Obs_Area as Obs_Area
import RL_Agent.Obs_Finance as Obs_Finance
import RL_Agent.Obs_Position as Obs_Position
import RL_Agent.Observation as Observation
import constants
"""
For each of the below needs a variable for isTraining if that is true consider that as training phase.

"""
class Agent:
	def __init__(self, id):
		self.id = id
		self.rl_agent = buddy.RLAgent(id)
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


	def getBMSTDecision(self, state):
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
		pass
	def respondMortgage(self, state):
		pass


	"""
	Helper methods to transform states passed by adjudicator to ones expected by RLAgent
	"""
	def playFirstMove(self):
		"""Think about the handling of first move from agent. This is required for Q-learning first step"""
		"""agent_start Method will be called here"""
		pass
	def playGame(self):
		"""Calculate the initial reward, take an action"""
		pass

	def createPosition(self, property):
		group_id = constants.board[property]["monopoly_group_id"]
		relativePlayArea = (group_id + 1) / 10
		return relativePlayArea

	def createFinance(self, state):
		totalAssests = 0
		money = state[self.PLAYER_CASH_INDEX][self.current_player]
		if self.current_player == 0:
			sign = 1
			other_player_id = 1
		else:
			sign = -1
			other_player_id = 0
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		for property in owned_properties:
			num_houses = (sign * state[self.PROPERTY_STATUS_INDEX][property]) - 1
			totalAssests += num_houses * constants.board[property]['build_cost'] * 0.5
			totalAssests += constants.board[property]["price"]*0.5
		otherPlayerAssests = 0
		other_player_properties = self.get_owned_property_not_morgaged(state, other_player_id)
		for property in other_player_properties:
			num_houses = (sign * state[self.PROPERTY_STATUS_INDEX][property]) - 1
			otherPlayerAssests += num_houses * constants.board[property]['build_cost'] * 0.5
			otherPlayerAssests += constants.board[property]["price"]*0.5
		return (totalAssests/(totalAssests + otherPlayerAssests), self.smoothFunction(money, 1500))



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

	def findMonopolyGroups(self, state, current_player):
		monopoly_groups = []
		range_status = [[1,6], [-6, -1]]
		properties_status = state[self.PROPERTY_STATUS_INDEX]
		i = 0
		for status in properties_status:
			if status >= range_status[current_player][0] and status <= range_status[current_player][1] and i in constants.property_to_space_map:
				property_id = constants.property_to_space_map[i]
				groupElements = constants.board[property_id]["monopoly_group_elements"]
				have_monopoly = True
				for element in groupElements:
					state_property_id = constants.space_to_property_map[element]
					status_element = state[self.PROPERTY_STATUS_INDEX][state_property_id]
					if status_element >= range_status[current_player][0] and status_element <= range_status[current_player][1]:
						have_monopoly = True
					else:
						have_monopoly = False
						break
				if have_monopoly == True:
					group = []
					if constants.board[property_id]['build_cost'] != 0:
						group.append(property_id)
						for element in groupElements:
							group.append(element)
						monopoly_groups.append(group)
			i = i + 1
		d = {}
		unique_monopoly_groups = []
		for group in monopoly_groups:
			for property in group:
				if property not in d:
					unique_monopoly_groups.append(group)
					for p in group:
						d[p] = 1
		return unique_monopoly_groups

	def getMonopolyGroups(self, state, player):
		group_ids = []
		groups = self.findMonopolyGroups(state, player)
		for group in groups:
			for property in group:
				id = constants.board[property]["monopoly_group_id"]
				group_ids.append(id)
				break
		return group_ids

	def createArea(self, state):
		if self.current_player == 0:
			other_player_id = 1
			sign = 1
		else:
			other_player_id = 0
			sign = -1
		group_ids_owned = self.getMonopolyGroups(state, self.current_player)
		other_player_groups = self.getMonopolyGroups(state, other_player_id)
		owned_properties = self.get_owned_property_not_morgaged(state, self.current_player)
		other_player_properties = self.get_owned_property_not_morgaged(state, other_player_id)
		number_properties_owned_in_group = [0] * 10
		number_properties_owned_in_group_other_player = [0]*10
		area = [[0] * 2 for i in range(10)]

		for i in owned_properties:
			group = constants.board[i]["monopoly_group_id"]
			if group in group_ids_owned:
				num_houses = (sign * state[self.PROPERTY_STATUS_INDEX][i]) - 1
				"""Catch: This number represents number of houses and hotels in case of monopoly group"""
				number_properties_owned_in_group[group] += num_houses
			else:
				number_properties_owned_in_group[group] += 1

		for i in range(10):
			if i in group_ids_owned:
				area[i][0] = (12 + (number_properties_owned_in_group[i]/constants.groupLengthMap[i]))/(17)
			else:
				area[i][0] = (12/(number_properties_owned_in_group[i]*constants.groupLengthMap[i]))/17

		for i in other_player_properties:
			group = constants.board[i]["monopoly_group_id"]
			if group in other_player_groups:
				num_houses = (sign * -1 * state[self.PROPERTY_STATUS_INDEX][i]) - 1
				"""Catch: This number represents number of houses and hotels in case of monopoly group"""
				number_properties_owned_in_group_other_player[group] += num_houses
			else:
				number_properties_owned_in_group_other_player[group] += 1

		for i in range(10):
			if i in other_player_groups:
				area[i][1] = (12 + (number_properties_owned_in_group_other_player[i]/constants.groupLengthMap[i]))/(17)
			else:
				area[i][1] = (12/(number_properties_owned_in_group_other_player[i]*constants.groupLengthMap[i]))/17

		return area

	def calculateReward(self):
		reward = 0
		pass

	def smoothFunction(self, x, factor):
		return (x/factor)/(1 + abs(x/factor))

	def createObs(self, state):
		position = Obs_Position.Obs_Position(self.createPosition(state[self.PLAYER_POSITION_INDEX][self.current_player]))
		value = self.createFinance(state)
		finance = Obs_Finance.Obs_Finance(value[0], value[1])
		area = Obs_Area.Obs_Area(self.createArea())
		return Observation.Observation(area, position, finance)
