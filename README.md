# Monopoly

Data Science Project CSE 519
Monopoly game playing AI Agent

## Install the Dependencies

```
pip install -r requirements.txt
```

## Run the code

```
To run the adjudicator program without the UI implementation, run:
from adjudicator import Adjudicator
from agent import Agent
agentOne = Agent(1)
agentTwo = Agent(2)
adjudicator = Adjudicator()
adjudicator.runGame(agentOne, agentTwo)

To run testcases, run:
python testcases.py

To run the user interface:
export FLASK_APP=app.py
flask run
#In a separate terminal window, run the below mentioned code
cd react-user-interface
npm install
npm start
#The server starts up on part 3000
```

## Issue Log
1) If you face issues with running the code on Windows, please check the Issues list.
2) The code doesn't contain an agent. You would need to add your agent in. You can check out testcases.py to get an idea of some sample agents.

## App Structure
The master branch consists of the implementation of the Adjudicator for the monopoly game.
The implementation also consists of a UI for going through the various game states after a game has been completed. 
NOTE: The UI currently shows the board representation and basic information about each Agent on any given turn such as properties owned, cash constructions on each property etc. Finer information regarding the state still remains to be implemented for the UI and is in progress.

**app.py:**<br>
>It is the Flask controller.  
>templates for rendering templates.  
>static has all static assets js, css and images.

**adjudicator.py:**<br>
>Consist of the actual implementation of the Adjudicator. The game is started by invoking the method: 

>runGame(agentOne,agentTwo,diceThrows=None,chanceCards=None,communityCards=None)<br>
>>This method accepts 2 Agents and runs the game. Over the course of the game, it determines which Agent is the winner.<br>
>>The other 3 parameters are for testing purposes only.<br>
>>diceThrows: used to pass in an array of dice rolls (each a 2x1 array of 2 die). The test case would be evaluated by taking a dice roll >>from the array and applying it instead of using the random die.<br>
>>chanceCards: an array of ids of chance cards to be used for a particular testcases. For referencing the values of the ids, please check constants.py.<br>
>>communityCards: an array of ids of community chest cards to be used for a particular testcases. For referencing the values of the ids, please check constants.py.

**config.py:**
>Consists of configurations for logging to the monopoly.log file. You can modify the verbosity of logging for different flows of the adjudicator here.

**constants.py:**
>Contains the constant representations such as the board, chance cards and community chest cards that remain static throughout the runtime of the game.

**testcases.py:**
>Consists of all the testcases written for and tested against the adjudicator. Each testcase contains a short description regarding what it is testing. The testcases each define their own Agents to suit their testing requirements. The testcases each receive an instance of the adjudicator as an argument and perform testcase validation by invoking the runGame method and observing the final results.
The program accepts an Adjudicator and 2 Agents as arguments and checks whether the testcase passes for the simulation run.

## Special Cases:
1. Timeout:
If an agent takes more than 3 seconds to respond to any call from the adjudicator, that agent loses. This is treated separately from the erroneous input situation where the agent passes in an incorrect value to a function call from the adjudicator. (For eg, passing in a string value/negative number to an auction, we default to a bid of 0).

2. We make receiveState calls in the following scenarios:

>>a) When a **Chance** or **Community Chest** card id drawn, it is called from both Agents.
Phase Number will be 7 for Chance cards and 8 for Community.
Phase payload will contain card id.<br>
b) **Dice Roll**
Phase Number = 2
Contains the die value for each dice and whether the player is eligible for another try in his current turn(effect of double. This is to account for cases where the player might not get another chance even if he rolls doubles in certain cases).
Called for both Agents.<br>
c) **Jail**
Phase Number = 6
If an agent was in Jail at the start of his turn, this call informs both Agents whether he is still in Jail after his Jail decision was carried out by the adjudicator.
Phase payload consists of a boolean with True meaning the agent is out of Jail.
Called for both Agents.<br>
d) **Auction**
Phase Number = 4
Called after an auction is completed to let both Agents know who won the auction. Payload consists of (Auctioned Property ID, winning agent id).<br>
e) **TradeResponse**
Phase Number = 1 (Trade offer)
If Agent 1 started a trade, and Agent 2 made a decision on it, this call informs Agent 1 regarding that decision.
The payload is of the form:
(tradeResponse,cashOffer,propertiesOffer,cashRequest,propertiesRequest)
where tradeResponse is a boolean value showing whether the trade was accepted by the other agent or not.

>>NOTE: Please note that this does not include the case where the agent who proposes the trade gives an invalid trade offer (eg, He requested a property from the opponent that has a house on it). If that happens, the opponent is not consulted for a tradeResponse. Thus there would be no receiveState call in that case. This is to be expected as the sole reason this scenario occurred was because the agent who proposed the trade gave an erroneous input. Also, since the input was erroneous, this particular BSTM of the agent would end with this trade request.

3. State History:
The state history is passed as part of the state always. A state is added to the state history whenever the state is handed to the agent as part of a function call from the adjudicator.(i.e., every instance of the state that the agent has seen would be recorded.)

4. Auction:
The way we have implemented BSTM invocation in our Adjudicator is to call it at 3 different points within a turn.
a) Before the Dice Roll (Preturn BSTM)
b) After the Dice Roll. (This would include current position info such as any possible debt or property id in case of unowned property.)
c) Post Agent decisions (Post turn BSTM).

>>Thus, there is a scenario of BSTM not being invoked again for auctions. i.e., in the case where an agent falls on an unowned property, the BSTM call would be made while giving the player this information after moving him to this location. Thus, the current player has to make a decision to either buy or auction the property and make necessary BSTM operations to generate money here. This also puts the opponent at a disadvantage because if the player starts an auction, he wouldn't get a chance to make a BSTM to secure the money needed for the auction. He would instead, have to rely on his cash in hand at that time.

>>We had implemented it this way as we felt it might lead to more strategy involving auctions. Please let us know if you feel another BSTM is needed before the auction.
