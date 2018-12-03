from adjudicator import Adjudicator

PLAYER_TURN_INDEX = 0
PROPERTY_STATUS_INDEX = 1
PLAYER_POSITION_INDEX = 2
PLAYER_CASH_INDEX = 3
PHASE_NUMBER_INDEX = 4
PHASE_PAYLOAD_INDEX = 5
DEBT_INDEX = 6

def compare_states(state,expected_output):
	passCounter = 0
	if 'turn' in expected_output:
		if (state[PLAYER_TURN_INDEX] == expected_output['turn']):
			passCounter+=1
		else:
			print("Turn number doesn't match")
	
	if 'cash' in expected_output:
		if (state[PLAYER_CASH_INDEX][0] == expected_output['cash'][0]) and (state[PLAYER_CASH_INDEX][1] == expected_output['cash'][1]):
			passCounter+=1
			if 'cash_2' in expected_output:
				passCounter+=1
		else:
			print("Cash doesn't match")
			if 'cash_2' in expected_output:
				if (state[PLAYER_CASH_INDEX][0] == expected_output['cash_2'][0]) and (state[PLAYER_CASH_INDEX][1] == expected_output['cash_2'][1]):
					passCounter+=2
				else:
					print("Cash_2 doesn't match")
	
	if 'position' in expected_output:
		if (state[PLAYER_POSITION_INDEX][0] == expected_output['position'][0]) and (state[PLAYER_POSITION_INDEX][1] == expected_output['position'][1]):
			passCounter+=1
			if 'position_2' in expected_output:
				passCounter+=1
		else:
			print("Position doesn't match")
			if 'position_2' in expected_output:
				if (state[PLAYER_POSITION_INDEX][0] == expected_output['position_2'][0]) and (state[PLAYER_POSITION_INDEX][1] == expected_output['position_2'][1]):
					passCounter+=2
				else:
					print("Position_2 doesn't match")
			
	if 'properties' in expected_output:
		flag = True
		for property in expected_output['properties']:
			if state[PROPERTY_STATUS_INDEX][property[0]] != property[1]:
				flag = False
				break
		if flag:
			passCounter += 1
		else:
			print("Property"+str(property)+" don't match")
			
	if passCounter >= len(expected_output):
		return True
	else:
		return False

def testcase_auction(adjudicator):
	print("Test Case: Description:")
	print("AgentTwo will fall on Vermont Avenue(Position 8) and will decide to auction it.")
	print("AgentTwo will bid $175.5 and AgentOne $160")
	print("The auction would be won by AgentTwo who will only pay 175")
	
	class AgentOne:
		def __init__(self, id):
			self.id = id
		
		def getBSMTDecision(self, state):
			return None
	
		def buyProperty(self, state):
			return False
		
		def auctionProperty(self, state):
			return 160
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return False
	
		def auctionProperty(self, state):
			return 175.5
		
		def receiveState(self, state):
			pass
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[3,5]],None,None)
	
	final_state = adjudicator.state
	
	expected_output = {
		"cash": [1500,1500-175],
		"position":[8,0],
		"properties":[(8,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	print("")
	
	return result

def testcase_payment(adjudicator):
	print("Test Case: Description:")
	print("AgentTwo will fall on Income Tax(Position 4) and has to pay the bank $200.")
	
	class AgentOne:
		def __init__(self, id):
			self.id = id
		
		def getBSMTDecision(self, state):
			return None
	
		def buyProperty(self, state):
			return False
		
		def auctionProperty(self, state):
			return 160
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return False
	
		def auctionProperty(self, state):
			return 170
		
		def receiveState(self, state):
			pass
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[3,1]],None,None)
	
	final_state = adjudicator.state
	
	expected_output = {
		"cash": [1500-200,1500],
		"position":[4,0]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else: 
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_buying_houses(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,1),(8,2),(9,1)])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Buying of houses")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120-200,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,2),(8,3),(9,2),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result
	
def testcase_selling_houses(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 2) and (vermont == 3) and (connecticut == 2):
				return ("S", [(6,1),(8,1)])
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,1),(8,2),(9,1)])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Selling of houses")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120-200+50,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,1),(8,2),(9,2),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_trade(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
		def respondTrade(self,state):
			return True
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			self.trade_status = None
			
		def getBSMTDecision(self, state):
			stcharles = state[PROPERTY_STATUS_INDEX][11]
			virginia = state[PROPERTY_STATUS_INDEX][14]	
			
			if (virginia == 1) and (self.trade_status==None):
				return ("T",50.5,[19],0,[14])
			
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			phase = state[PHASE_NUMBER_INDEX]
			if phase == 1:#Trade Offer Phase
				(self.trade_status,cashOffer,propertiesOffer,cashRequest,propertiesRequest) = state[PHASE_PAYLOAD_INDEX]
	
	print("\nTest Case: Trade")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3],[2,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120-160+50,1500-140-200-150-50],
		"position":[14,28],
		"properties":[(6,1),(8,1),(9,1),(11,-1),(14,-1),(19,1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_buying_houses_invalid_1(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1):
				if self.erronous_bstm_counter < 1:
					self.erronous_bstm_counter += 1
					return ("B", [(6,1),(8,2)]) # Erroneous Buy house command
			return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			stcharles = state[PROPERTY_STATUS_INDEX][11]	
			if (stcharles == -1) and (self.erronous_bstm_counter < 1):
				self.erronous_bstm_counter += 1
				return ("B", [(11,1)]) #Erroneous Buying command. Should not do anything.
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Trying to buy houses without completing monopoly")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200,1500-140-200],
		"position":[0,19],
		"properties":[(6,1),(8,1),(11,-1),(19,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_buying_houses_invalid_2(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,1),(8,3),(9,1)])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Trying to buy an invalid number of houses in a completed monopoly")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,1),(8,1),(9,1),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_mortgaging_unmortgaging(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("M", [6,8,9])
			elif (oriental == 7):
				return ("M", [6])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Unmortgaging a property")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120+50+50+60-50-5,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,1),(8,7),(9,7),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_invalid_mortgaging(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			newyork = state[PROPERTY_STATUS_INDEX][19]
			waterworks = state[PROPERTY_STATUS_INDEX][28]
			
			if (newyork == -1):
				return ("M", [19]) #Owned by opponent
			elif (waterworks == -1):
				return ("M", [29]) #Unowned Property
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Trying to mortgage opponent's property and an unowned property")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,1),(8,1),(9,1),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_auction_for_invalid_action(adjudicator):
	print("\nTest Description:")
	print("AgentOne will fall on Vermont Avenue(Position 8) and will decide to auction it.")
	print("AgentTwo will bid $170 and AgentOne will pass Junk Value")
	print("The auction would be won by AgentTwo")

	class AgentOne:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
			return None

		def buyProperty(self, state):
			return False

		def auctionProperty(self, state):
			return "Junk Value"

		def receiveState(self, state):
			pass

	class AgentTwo:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
			return None

		def buyProperty(self, state):
			return False

		def auctionProperty(self, state):
			return 170

		def receiveState(self, state):
			pass

	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	adjudicator.runGame(agentOne,agentTwo,[[3, 5]], None, None)

	final_state = adjudicator.state

	expected_output = {
		"cash": [1500, 1500 - 170],
		"position": [8, 0],
		"properties": [(8, -1)]
	}

	result = compare_states(final_state, expected_output)

	if result:
		print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)

	print("")

	return result

def testcase_trade_for_invalid_action(adjudicator):
	print("Test Description:")
	print("AgentOne falls on Oriental Avenue and buys it.")
	print("AgentTwo falls on St. Charles Avenue and buys it.")
	print("AgentOne will trade Oriental Avenue property for St. Charles Avenue and AgentTwo returns Junk Value")

	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0

		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			if oriental == 1 and self.erronous_bstm_counter == 0:
				self.erronous_bstm_counter = 1
				return ("T", 0, [6], 0, [11])
			return None

		def buyProperty(self, state):
			return True

		def auctionProperty(self, state):
			return 160

		def receiveState(self, state):
			pass

		def respondTrade(self, state):
			return False

	class AgentTwo:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
			return None

		def buyProperty(self, state):
			return True

		def auctionProperty(self, state):
			return 170

		def receiveState(self, state):
			pass

		def respondTrade(self, state):
			return "Junk Value"

	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	adjudicator.runGame(agentOne,agentTwo,[[1, 5], [5, 6]], None, [0])

	final_state = adjudicator.state

	# Since the trade is unsuccessful here
	result = final_state[PROPERTY_STATUS_INDEX][6] == 1

	if result:
		print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)

	print("")

	return result

def testcase_buyproperty_for_invalid_action(adjudicator):
	print("Test Description:")
	print("AgentOne will fall on Vermont Avenue(Position 8) and will return an erroneous value. This should start an auction phase.")
	print("AgentTwo will bid $170 and AgentOne will bid $160")
	print("The auction would be won by AgentTwo")

	class AgentOne:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
			return None

		def buyProperty(self, state):
			return "Junk Value"

		def auctionProperty(self, state):
			return 160

		def receiveState(self, state):
			pass

	class AgentTwo:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
			return None

		def buyProperty(self, state):
			return False

		def auctionProperty(self, state):
			return 170

		def receiveState(self, state):
			pass
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	adjudicator.runGame(agentOne,agentTwo,[[3, 5]], None, None)

	final_state = adjudicator.state

	expected_output = {
		"cash": [1500, 1500 - 170],
		"position": [8, 0],
		"properties": [(8, -1)]
	}

	result = compare_states(final_state, expected_output)

	if result:
		print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)

	return result

def testcase_buying_invalid_two_hotels(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,4),(8,5),(9,5)])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Invalid buying of 2 hotels on two properties in a single monopoly")
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,1),(8,1),(9,1),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_buying_max_houses(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			orange_0 = state[PROPERTY_STATUS_INDEX][16]
			orange_1 = state[PROPERTY_STATUS_INDEX][18]
			orange_2 = state[PROPERTY_STATUS_INDEX][19]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,4),(8,4),(9,4)])
			elif orange_0==1 and orange_1==1 and orange_2==1:
				return ("B", [(16,2),(18,1),(19,1)])
			elif state[PROPERTY_STATUS_INDEX][19]==2:
				#This build operation would fail.Already reached 32 houses.
				return ("B", [(19,1)])
			else:
				return None
	
		def buyProperty(self, state):
			propertyId = state[PHASE_PAYLOAD_INDEX]
			if propertyId == 39:
				return False
			return True
		
		def auctionProperty(self, state):
			return 8
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][11]
			vermont = state[PROPERTY_STATUS_INDEX][13]
			connecticut = state[PROPERTY_STATUS_INDEX][14]
			
			red_0 = state[PROPERTY_STATUS_INDEX][21]
			red_1 = state[PROPERTY_STATUS_INDEX][23]
			red_2 = state[PROPERTY_STATUS_INDEX][24]
			cash = state[PLAYER_CASH_INDEX][1]
			
			if (oriental == -1) and (vermont == -1) and (connecticut == -1):
				return ("B", [(11,4),(13,4),(14,4)])
			elif red_0==-1 and red_1==-1 and red_2==-1 and cash>=600:
				return ("B", [(21,2),(23,1),(24,1)])
			else:
				return None
			
		def buyProperty(self, state):
			return False
	
		def auctionProperty(self, state):
			property = state[PHASE_PAYLOAD_INDEX][0]
			if property==18:
				return 5
			return 10
		
		def receiveState(self, state):
			pass
		
		def jailDecision(self,state):
			return ("P",)
	
	print("\nTest Case: Trying to buy a house when all 32 houses have already been constructed")
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5], [5,6], [1,1],[5,4], [1,1],[5,5],[3,3], [5,4], [2,2],[5,5],[3,3], [3,4], [6,5], [1,2], [6,6],[5,4], [1,2], [5,4], [3,5], [4,3]],[13,0],[0,1,7])
	
	expected_output = {
		"cash": [1500-100-100+200-120-600-180-200+200+200-8-400,1500-10-10-10-50-1200-10-50-10-10+200+200+100-600-10],
		"position":[0,18],
		"properties":[(6,5),(8,5),(9,5),(11,-5),(13,-5),(14,-5),(16,3),(18,2),(19,2),(21,-3),(23,-2),(24,-2),(39,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testGettingOutOfJail(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
		def jailDecision(self,state):
			return ("P",)
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
	print("\nTest Case: AgentOne ends up in Jail by rolling 3 doubles in a row. He pays to get out in the next turn and moves to a certain position.")
	p1 = AgentOne(0)
	p2 = AgentTwo(1)
	dice = [(6, 6), (6, 6),(6, 6), (2, 3),(4,2)]
	
	[winner, final_state] = adjudicator.runGame(p1, p2, dice, [], [])
	
	expected_output = {
		"cash": [1500-150-240-50-180,1500-200],
		"position":[16,5],
		"properties":[(12,1),(24,1),(5,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_selling_hotel_aftermax(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			orange_0 = state[PROPERTY_STATUS_INDEX][16]
			orange_1 = state[PROPERTY_STATUS_INDEX][18]
			orange_2 = state[PROPERTY_STATUS_INDEX][19]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,4),(8,4),(9,4)])
			elif orange_0==1 and orange_1==1 and orange_2==1:
				return ("B", [(16,2),(18,1),(19,1)])
			elif state[PROPERTY_STATUS_INDEX][19]==2:
				return ("B", [(6,1),(18,1),(19,2)])
			elif oriental==6:
				return ("S",[(6,1)]) # Should fail
			else:
				return None
	
		def buyProperty(self, state):
			propertyId = state[PHASE_PAYLOAD_INDEX]
			if propertyId == 39:
				return False
			return True
		
		def auctionProperty(self, state):
			return 8
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][11]
			vermont = state[PROPERTY_STATUS_INDEX][13]
			connecticut = state[PROPERTY_STATUS_INDEX][14]
			
			red_0 = state[PROPERTY_STATUS_INDEX][21]
			red_1 = state[PROPERTY_STATUS_INDEX][23]
			red_2 = state[PROPERTY_STATUS_INDEX][24]
			cash = state[PLAYER_CASH_INDEX][1]
			
			if (oriental == -1) and (vermont == -1) and (connecticut == -1):
				return ("B", [(11,4),(13,4),(14,4)])
			elif red_0==-1 and red_1==-1 and red_2==-1 and cash>=600:
				return ("B", [(21,2),(23,1),(24,1)])
			else:
				return None
			
		def buyProperty(self, state):
			return False
	
		def auctionProperty(self, state):
			property = state[PHASE_PAYLOAD_INDEX][0]
			if property==18:
				return 5
			return 10
		
		def receiveState(self, state):
			pass
		
		def jailDecision(self,state):
			return ("P",)
	
	print("\nTest Case: Trying to sell a hotel when more than 28 houses have already been constructed")
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5], [5,6], [1,1],[5,4], [1,1],[5,5],[3,3], [5,4], [2,2],[5,5],[3,3], [3,4], [6,5], [1,2], [6,6],[5,4], [1,2], [5,4], [3,5], [4,3], [3,4]],[13,0,15],[0,1,7])
	
	expected_output = {
		"cash": [1500-100-100+200-120-600-180-200+200+200-8-400-350+150,1500-10-10-10-50-1200-10-50-10-10+200+200+100-600-10],
		"position":[7,18],
		"properties":[(6,6),(8,5),(9,5),(11,-5),(13,-5),(14,-5),(16,3),(18,3),(19,4),(21,-3),(23,-2),(24,-2),(39,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_trade_mortgage(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			if (state[PROPERTY_STATUS_INDEX][19] == 7):
				return ("M",[19])
			
			return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
		def respondTrade(self,state):
			return True
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			self.trade_status = None
			
		def getBSMTDecision(self, state):
			virginia = state[PROPERTY_STATUS_INDEX][14]	
			
			if (state[PROPERTY_STATUS_INDEX][19] == -1):
				return ("M",[19])
			
			if (state[PROPERTY_STATUS_INDEX][19] == -7) and (virginia == 1) and (self.trade_status==None):
				return ("T",50,[19],0,[14])
			
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			phase = state[PHASE_NUMBER_INDEX]
			if phase == 1:#Trade Offer Phase
				(self.trade_status,cashOffer,propertiesOffer,cashRequest,propertiesRequest) = state[PHASE_PAYLOAD_INDEX]
	
	print("\nTest Case: Trade involving one mortgaged item. The item is unmortgaged in the next turn.")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3],[2,3],[4,3]],None,[0])
	
	expected_output = {
		"cash": [1500-100-100+200-120-160+50-10-110,1500-140-200+100-150-50-200],
		"position":[14,35],
		"properties":[(6,1),(8,1),(9,1),(11,-1),(14,-1),(19,1),(28,-1),(35,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
	
	return result

def testcase_three_jails_a_day_keeps_the_lawyer_away(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,4),(8,4),(9,5)])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
		def jailDecision(self,state):
			return ("R",)
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Player stays in jail for 3 turns and has to pay and get out on the third turn.")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5], [5,6], [1,1],[5,4], [2,6], [5,4], [6,3], [3,3],[5,4], [5,4], [5,1], [5,3], [5,6], [4,3], [4,3], [5,3], [4,5]],None,[0,1])
	
	expected_output = {
		"cash": [1500-100-100+200-120-650-200-240-50-16,1500-140-200-150-350-150+16],
		"position":[19,20],
		"properties":[(5,-1),(6,5),(8,5),(9,6),(12,-1),(15,1),(11,-1),(19,-1),(24,1),(28,-1),(37,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result and winner==2: 
		print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_three_jails_a_day_keeps_the_lawyer_away_2(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBSMTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("B", [(6,4),(8,4),(9,5)])
			else:
				return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
		
		def jailDecision(self,state):
			return ("R",)
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Player stays in jail for 3 turns and has to pay and get out on the third turn. But he doesn't have enough and goes bankrupt.")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[1,5], [5,6], [1,1],[5,4], [2,6], [5,4], [6,3], [3,3],[5,4], [5,4], [1,1],[1,1],[1,1], [5,3], [5,6], [4,3], [4,3], [5,3], [4,3]],None,[0,1])
	
	#Acept the answer if the final cash includes the jail payment or not. This could vary based on adjudicator implementation.
	expected_output = {
		"cash": [1500-100-100+200-120-650-200-240-260-8-50,1500-140-200-150-350+8-150],
		"cash_2": [1500-100-100+200-120-650-200-240-260-8,1500-140-200-150-350+8-150],
		"position":[10,20],
		"position_2":[-1,20],
		"properties":[(5,-1),(6,5),(8,5),(9,6),(12,-1),(15,1),(11,-1),(19,-1),(24,1),(26,1),(28,-1),(37,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result and winner==2: 
		print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_utility_chance_card_owned(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
		
		def getBSMTDecision(self, state):
			return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return 5
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return 0
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Player falls on the Chance card which makes you advance to nearest Utility. But it is owned. Checking if rent is correctly calculated.")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[6,6],[1,2],[4,3],[6,4]],[3],None)
	
	expected_output = {
		"cash": [1500-150-200+100,1500-100],
		"position":[15,12],
		"properties":[(12,1),(15,1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

def testcase_railroad_chance_card_owned(adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
		
		def getBSMTDecision(self, state):
			return None
	
		def buyProperty(self, state):
			return True
		
		def auctionProperty(self, state):
			return 5
		
		def receiveState(self, state):
			pass
		
	class AgentTwo:
		def __init__(self, id):
			self.id = id
			
		def getBSMTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return 0
		
		def receiveState(self, state):
			pass
	
	print("\nTest Case: Player falls on the Chance card which makes you advance to nearest Railroad. But it is owned. Checking if rent is correctly calculated.")
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[6,6],[1,2],[4,3]],[5],None)
	
	expected_output = {
		"cash": [1500-150-200+50,1500-50],
		"position":[15,15],
		"properties":[(12,1),(15,1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

"""
print("Testcase flow Description:")
print("Turn 0:")
print("AgentOne falls on Oriental Avenue and buys it.")
print("Turn 1:")
print("AgentTwo falls on St. Charles Avenue and buys it.")
print("Turn 2:")
print("AgentOne falls on Vermont Avenue and buys it. Double Roll.")
print("AgentOne falls on Community Chest. Advance to Go.")
print("Turn 3:")
print("AgentTwo falls on New York Avenue and buys it.")
print("Turn 4:")
print("AgentOne falls on Connecticut Avenue and buys it. Completes the Monopoly.")
print("During the post turn BSTM, AgentOne purchases 4 houses, with 2 houses on Vermont Avenue.")
print("In the second testcase,additionally, during the post turn BSTM, AgentOne sells 2 houses, one from Oriental Avenue and one from Vermont Avenue.")
print("Turn 5:")
print("AgentTwo falls on Water Works and buys it.")
print("From this point, on events are only for the trade testcase")
print("Turn 6:")
print("AgentOne falls on Virginia Avenue and buys it.")
print("During the post turn BSTM, AgentTwo proposes a trade of $50 and New York Avenue for Virginia Avenue.")
print("AgentOne accepts.\n")
"""
print("This testcase validates the following:")

"""
Testcases that maybe invalid:
testcase_buying_invalid_two_hotels
"""
#20 Testcases in total
tests = [
	testcase_auction,
	testcase_payment,
	testcase_buying_houses,
	testcase_selling_houses,
	testcase_trade,
	testcase_buying_houses_invalid_1,
	testcase_buying_houses_invalid_2,
	testcase_mortgaging_unmortgaging,
	testcase_invalid_mortgaging,
	testcase_auction_for_invalid_action,
	testcase_trade_for_invalid_action,
	testcase_buyproperty_for_invalid_action,
	testGettingOutOfJail,
	testcase_buying_max_houses,
	testcase_trade_mortgage,
	testcase_selling_hotel_aftermax,
	testcase_three_jails_a_day_keeps_the_lawyer_away,
	testcase_three_jails_a_day_keeps_the_lawyer_away_2,
	testcase_utility_chance_card_owned,
	testcase_railroad_chance_card_owned
]

#Execution
for test in tests:
	adjudicator = Adjudicator()
	test(adjudicator)