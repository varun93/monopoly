import adjudicator

class AuctionAgent_1:
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
	
class AuctionAgent_2:
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

def compare_states(state1,state2):
	
	if not isinstance(state1,type(state2)) or (len(state1)!=len(state2)):
		print("Inconsistent type or length detected for First argument")
		return false
	else:
		count = 0
		
		if (state1[0] == state2[0]): count+=1
		
		flag = True
		for property,property2 in zip(state1[1],state2[1]):
			if property != property2:
				flag = False
		if flag: count+=1
		
		if (state1[2][0] == state2[2][0]) and (state1[2][1] == state2[2][1]): count+=1
		if (state1[3][0] == state2[3][0]) and (state1[3][1] == state2[3][1]): count+=1
		if (state1[4] == state2[4]): count+=1
		
		if len(state1[5]) == len(state2[5]):
			flag = True
			for key,key2 in zip(state1[5],state2[5]):
				if state1[5][key] != state2[5][key]:
					 flag = False
			if flag: count+=1
		
		if count == 6:
			return True
		else:
			print( str(count)+"/"+str(len(state2))+" arguments are correct."  )
			return False
	
def testcase_1(Adjudicator,AgentOne,AgentTwo):
	print("Test #1 Description:")
	print("AgentTwo will fall on Vermont Avenue(Position 8) and will decide to auction it.")
	print("AgentTwo will bid $90 and AgentOne $80")
	print("The auction would be won by AgentTwo")
	
	adjudicator = Adjudicator(AgentOne,AgentTwo)
	adjudicator.runGame([[3,5]],None,None)
	
	final_state = adjudicator.state
	
	output_state = [1, [ 0,  0,  0,  0,  0,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0], [8, 0], [1500, 1330], 4, {}]
	
	result = compare_states(final_state,output_state)
	
	if result: print("Pass")
	else:
		print("Fail")
		print("Received Output:")
		print(final_state)
	
	print("")
	
	return result
	

#Execution
testcase_1(adjudicator.Adjudicator,AuctionAgent_1,AuctionAgent_2)