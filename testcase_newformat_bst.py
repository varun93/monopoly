import adjudicator

PLAYER_TURN_INDEX = 0
PROPERTY_STATUS_INDEX = 1
PLAYER_POSITION_INDEX = 2
PLAYER_CASH_INDEX = 3
PHASE_NUMBER_INDEX = 4
PHASE_PAYLOAD_INDEX = 5

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
		else:
			print("Cash doesn't match")
	
	if 'position' in expected_output:
		if (state[PLAYER_POSITION_INDEX][0] == expected_output['position'][0]) and (state[PLAYER_POSITION_INDEX][1] == expected_output['position'][1]):
			passCounter+=1
		else:
			print("Position doesn't match")
			
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
			
	if passCounter == len(expected_output):
		return True
	else:
		return False

def testcase_buying_houses(Adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	final_state = adjudicator.state
	
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
	
def testcase_selling_houses(Adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	final_state = adjudicator.state
	
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

def testcase_trade(Adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
			stcharles = state[PROPERTY_STATUS_INDEX][11]
			virginia = state[PROPERTY_STATUS_INDEX][14]	
			
			if (virginia == 1) and (self.trade_status==None):
				return ("T",50,[19],0,[14])
			
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			phase = state[PHASE_NUMBER_INDEX]
			if phase == 1:#Trade Offer Phase
				self.trade_status = state[PHASE_PAYLOAD_INDEX]['tradeResponse']
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3],[2,3]],None,[0])
	
	final_state = adjudicator.state
	
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

def testcase_buying_houses_invalid_1(Adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
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
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[1,5],[5,6],[1,1],[5,4],[2,6]],None,[0])
	
	final_state = adjudicator.state
	
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
	
	print("")
	
	return result

def testcase_buying_houses_invalid_2(Adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	final_state = adjudicator.state
	
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

def testcase_mortgaging_unmortgaging(Adjudicator):
	class AgentOne:
		def __init__(self, id):
			self.id = id
			self.erronous_bstm_counter = 0
		
		def getBMSTDecision(self, state):
			oriental = state[PROPERTY_STATUS_INDEX][6]
			vermont = state[PROPERTY_STATUS_INDEX][8]
			connecticut = state[PROPERTY_STATUS_INDEX][9]
			
			if (oriental == 1) and (vermont == 1) and (connecticut == 1):
				return ("M", [6,8,9])
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
			
		def getBMSTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return True
	
		def auctionProperty(self, state):
			return False
		
		def receiveState(self, state):
			pass
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[1,5],[5,6],[1,1],[5,4],[2,6],[5,4],[6,3]],None,[0])
	
	final_state = adjudicator.state
	
	expected_output = {
		"cash": [1500-100-100+200-120+50+50+60,1500-140-200-150],
		"position":[9,28],
		"properties":[(6,7),(8,7),(9,7),(11,-1),(19,-1),(28,-1)]
	}
	
	result = compare_states(final_state,expected_output)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	return result

print("This testcase validates the following:")
print("a) Buying of houses")
print("b) Selling of houses")
print("c) Trade")
print("d) Trying to buy houses without completing monopoly")
print("e) Trying to buy an invalid number of houses in a completed monopoly")
print("f) Unmortgaging a property")

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


tests = [
	testcase_buying_houses,
	testcase_selling_houses,
	testcase_trade,
	testcase_buying_houses_invalid_1,
	testcase_buying_houses_invalid_2,
	testcase_mortgaging_unmortgaging
]

#Execution
for test in tests:
	test(adjudicator.Adjudicator)