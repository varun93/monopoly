import adjudicator

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
				print("")
		if flag:
			passCounter += 1
		else:
			print("Property"+str(property)+" don't match")
			
	if passCounter == len(expected_output):
		return True
	else:
		return False
	
def testcase_auction(Adjudicator):
	print("Test #1 Description:")
	print("AgentTwo will fall on Vermont Avenue(Position 8) and will decide to auction it.")
	print("AgentTwo will bid $170 and AgentOne $160")
	print("The auction would be won by AgentTwo")
	
	class AgentOne:
		def __init__(self, id):
			self.id = id
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return False
	
		def auctionProperty(self, state):
			return 170.5
		
		def receiveState(self, state):
			pass
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	adjudicator = Adjudicator()
	[winner,final_state] = adjudicator.runGame(agentOne,agentTwo,[[3,5]],None,None)
	
	final_state = adjudicator.state
	
	expected_output = {
		"cash": [1500,1500-170],
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

def testcase_payment(Adjudicator):
	print("Test #2 Description:")
	print("AgentTwo will fall on Income Tax(Position 4) and has to pay the bank $200.")
	
	class AgentOne:
		def __init__(self, id):
			self.id = id
		
		def getBMSTDecision(self, state):
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
			
		def getBMSTDecision(self, state):
			return None
			
		def buyProperty(self, state):
			return False
	
		def auctionProperty(self, state):
			return 170
		
		def receiveState(self, state):
			pass
	
	agentOne = AgentOne(1)
	agentTwo = AgentTwo(2)
	adjudicator = Adjudicator()
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
	
	print("")
	
	return result

tests = [
	testcase_auction,
	testcase_payment
]	

#Execution
for test in tests:
	test(adjudicator.Adjudicator)