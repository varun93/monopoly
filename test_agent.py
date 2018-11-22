import agent
import constants

class Test_Agent:
	def __init__(self):
		self.agent = agent.Agent(1)

	def test_buy_houses(self):
		input_states = [
		[
			2,  # player turn; 0
			[0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			# player properties; 1
			[12, 9],  # player's position; 2
			[1300, 1380],  # player's cash; 3
			0,  # phase number; 4
			{}  # phase payload; 5
		],

		[
				2,  # player turn; 0
				[0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				# player properties; 1
				[9, 9],  # player's position; 2
				[1300, 1380],  # player's cash; 3
				0,  # phase number; 4
				{'cash': 1380, 'source': 'opponent'}
		],

		[
				2,  # player turn; 0
				[0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				# player properties; 1
				[9, 9],  # player's position; 2
				[1300, 1380],  # player's cash; 3
				0,  # phase number; 4
				{'cash': 1380, 'source': 'opponent'}
		],

		[
				2,  # player turn; 0
				[0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				# player properties; 1
				[6, 9],  # player's position; 2
				[1300, 60],  # player's cash; 3
				4,  # phase number; 4
				{'property': 6}  # phase payload; 5
		],

		[
				2,  # player turn; 0
				[0, 0, 1, -1, -1, -2, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
				# player properties; 1
				[15, 9],  # player's position; 2
				[1300, 1380],  # player's cash; 3
				0,  # phase number; 4
				{}  # phase payload; 5
		]

		]

		output_state = ("B", [(14,1), (11, 1), (13, 1)])
		b = self.agent.buying_strategy(input_states[0],0)
		print("Expected Output State: ", output_state)
		print("Actual Output State", b)

		output_state = ("M", [11,13]) #Order is important here.
		m = self.agent.getBMSTDecision(input_states[1])
		print("Expected Output State", output_state)
		print("Actual Output State", m)

		output_state = ('S', [(11, 1), (13, 1), (14, 1)])
		s = self.agent.getBMSTDecision(input_states[2])
		print("Expected Output State", output_state)
		print("Actual Output State", s)

		output_state = 61
		auction = self.agent.auctionProperty(input_states[3])
		print("Expected Output State", output_state)
		print("Actual Output State", auction)

		output_state = ('C', 28)
		auction = self.agent.jailDecision(input_states[4])
		print("Expected Output State", output_state)
		print("Actual Output State", auction)



test_agent = Test_Agent()
test_agent.test_buy_houses()