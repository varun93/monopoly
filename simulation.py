from adjudicator import Adjudicator

import Team007
import Team001
import TeamBoardWalk
import TeamHarambe
import TeamInsertName
import TeamMaverick
import TeamMonopoly
import TeamNoviceGamblers
import TeamVAR

agents = {
1:Team001, #
2:TeamMonopoly, #Working
3:TeamBoardWalk, #Working
4:TeamHarambe, #Working
5:TeamInsertName, #Working
6:TeamMaverick, #Working
7:Team007, #Working
8:TeamNoviceGamblers, #Working
9:TeamVAR #Working
}

orderings = [(1,8),(2,7),(3,6),(4,5),(8,9),(7,1),(6,2),(5,3),(2,9),(3,8),(4,7),(5,6),(9,1),(8,2),(7,3),(6,4),(3,1),(4,9),(5,8),(6,7),(1,2),(9,3),(8,4),(7,5),(4,2),(5,1),(6,9),(7,8),(2,3),(1,4),(9,5),(8,6),(9,7),(1,6),(2,5),(3,4)]
#orderings = [(1,7)]

NO_OF_GAMES = 100

for ordering in orderings:
	winners = []
	final_states = []
	
	#if 4 in ordering:
		#Skipping team harambe
	#	continue
	
	for i in range(1, NO_OF_GAMES+1):
		
		if i>(NO_OF_GAMES/2):
			agentOneId = ordering[0]
			agentTwoId = ordering[1]
			agentOne = agents[agentOneId].Agent(1)
			agentTwo = agents[agentTwoId].Agent(2)
		else:
			agentOneId = ordering[1]
			agentTwoId = ordering[0]
			agentOne = agents[agentOneId].Agent(1)
			agentTwo = agents[agentTwoId].Agent(2)
		
		adjudicator = Adjudicator()
		[winner,final_state] = adjudicator.runGame(agentOne, agentTwo)
		realWinner = 0
		if winner == 1:
			realWinner = agentOneId
		elif winner == 2:
			realWinner = agentTwoId
		elif winner == 0:
			realWinner = 0
		
		if i%20==0:
			print("Game "+str(i)+" completed")
		
		winners.append(realWinner)
		if realWinner in agents:
			winnerName = agents[realWinner].__name__
		else:
			winnerName = "Tie"
		
		opponent = abs(winner - 2)
		
		game_phase={
		0: "BSTM",
		1: "TRADE_OFFER",
		2: "DICE_ROLL",
		3: "BUYING",
		4: "AUCTION",
		5: "PAYMENT",
		6: "JAIL",
		7: "CHANCE_CARD",
		8: "COMMUNITY_CHEST_CARD"	
		}
		
		#String replacement for debt receiver
		if final_state[6][2*opponent] == 0:
			if final_state[6][2*opponent+1] > 0:
				debt_receiver = "Bank"
			else:
				debt_receiver = "No debt"
		elif final_state[6][2*opponent] == 1:
			debt_receiver = agents[agentOneId].__name__
		elif final_state[6][2*opponent] == 2:
			debt_receiver = agents[agentTwoId].__name__
		
		final_states.append(str(realWinner)+"|"+winnerName+"|"+str(final_state[7])+"|"+
		str(final_state[0])+"|"+str(final_state[1])+"|"+str(final_state[2][winner-1])+"|"+
		str(final_state[2][opponent])+"|"+str(final_state[3][winner-1])+"|"+str(final_state[3][opponent])+"|"+
		str(final_state[6][2*opponent+1])+"|"+debt_receiver+"|"+str(game_phase[final_state[4]])+"\n")
	
	f = open("game_stats_"+str(ordering[0])+str(ordering[1])+".txt", "w")
	f.write("winner_id|winner|reason|turn|properties|winner_position|loser_position|winner_cash|loser_cash|loser_debt|debt_receiver|game_phase\n")
	for final_state in final_states:
		f.write(str(final_state))
	f.close()

	print("Results:")
	print("Agent "+agents[agentOneId].__name__+" wins: "+str(winners.count(agentOneId))+" games")
	print("Agent "+agents[agentTwoId].__name__+" wins: "+str(winners.count(agentTwoId))+" games")
	print("Ties: "+str(winners.count(0))+" games")
		
	input("Press Enter to continue...")

	
	
