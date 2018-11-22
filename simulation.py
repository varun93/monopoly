from adjudicator import Adjudicator
from agent import Agent
import random_agent

winners = [0, 0, 0]

for i in range(1, 101):
	adjudicator = Adjudicator(Agent, random_agent.Agent)
	winners[adjudicator.runGame()] += 1

print(winners)