import adjudicator

class Debug_Dice:
	def __init__(self):
		
		self.value_list = [[2,3]]
		
		self.die_1 = None
		self.die_2 = None
		self.double = False
		self.double_counter = 0

	def roll(self,ignore=False):
		
		if len(self.value_list)!=0:
			[self.die_1,self.die_2] = self.value_list.pop()
		
			self.double = self.die_1 == self.die_2
			if not ignore:
				self.double_counter += self.double
			
			print('Roll a {die_1} and a {die_2}'.format(die_1=self.die_1, die_2=self.die_2))
			
class AuctionAgent_1:
	def __init__(self, id):
		self.id = id

	def buyProperty(self, state):
		return False
	
	def auctionProperty(self, state):
		return 180
	
	def receiveState(self, state):
		pass
	
class AuctionAgent_2:
	def __init__(self, id):
		self.id = id
		
	def buyProperty(self, state):
		return False

	def auctionProperty(self, state):
		return 200
	
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
	
def testcase_2(Adjudicator,AgentOne,AgentTwo):
	"""
	Test Description:
	AgentTwo will fall on Luxury Tax(Position 38) and has to pay the bank $100.
	"""
	
	input_state =  [11, [ 0,  1,  0,  1,  0,  0, -1,  0,  0,  0,  1,  0,  0,  0, -1,  0,  0,
        0,  1, -1,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0], [3, 33], [580, 780], 4, {}]
	
	output_state = [12, [ 0,  1,  0,  1,  0,  0, -1,  0,  0,  0,  1,  0,  0,  0, -1,  0,  0,
        0,  1, -1,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0], [3, 38], [580, 680], 6, {'source': 'bank', 'cash': 100}]

	
	no_of_turns = 12
	
	adjudicator = Adjudicator(AgentOne,AgentTwo,input_state,Debug_Dice,no_of_turns)
	adjudicator.runGame()
	
	final_state = adjudicator.state
	
	#print(final_state)
	result = compare_states(final_state,output_state)
	
	if result: print("Pass")
	else: print("Fail")
	
	return result
	

#Execution
testcase_2(adjudicator.Adjudicator,AuctionAgent_1,AuctionAgent_2)