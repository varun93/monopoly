class Agent:
    def __init__(self, id):
        self.id = id
        pass
    def getBMSTDecision(self, state):
        # TODO:fill the template
        pass
    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        pass

    def auctionProperty(self, state):
        pass

    def receiveState(self, state):
        pass

    def parsePhase(self, state):
        phaseNumber = state["phase"]
        phasePayload = state["phase_payload"]

        # how to distinguish between dice roll bmst and bmst before
        if phaseNumber == 0:
            handleBMSTDecison(state)

        if phaseNumber == 3:
            diceValue = phasePayload["dice_roll"]
            currentPosition = state["player_position"][id]
            # is mod 40 correct?
            newPosition = (currentPosition + diceValue) % 40
            propertyStatus = state["property_status"][newPosition]

            # retrieve the property
            handleBMSTDecison(state)

    def jailDecision(self, state):
        pass

    def run(self, state):
        return {}
