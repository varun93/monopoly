import adjudicator
import constants
import copy

class Test_Adjudicator:
    
    def __init__(self):
        self.adjudicator = adjudicator.Adjudicator()
    
    def unit_test(self,test_name,method,input_states,output_states):
        print("Starting tests for "+test_name)
        for i in range( len(input_states) ):
            output = method( input_states[i] )
            flag = True
            for attribute in output_states[i]:
                if attribute in output:
                    if output_states[i][attribute] != output[attribute]:
                        flag = False
                else:
                    flag = False
                    break
            if flag:
                print("Pass")
            else:
                print("Fail")
                print("Expected Output: "+str(output_states[i]))
                print("Received Output: "+str(output))
    
    def test_handle_property(self):
        input_states =  [[
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [12,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [9,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [9,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,-1,-1,-2,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [9,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,-1,-1,-2,0,0,0,0,-1,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [15,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ]
        ]
        output_states =  [{'phase': 3, 'phase_properties': {'cash': 150, 'source': 'bank'}},
                          {'phase_properties': {'cash': 8, 'source': 'opponent'}},
                          {'phase_properties': {'cash': 16, 'source': 'opponent'}},
                          {'phase_properties': {'cash': 40, 'source': 'opponent'}},
                          {'phase_properties': {'cash': 50, 'source': 'opponent'}}]
        
        self.unit_test("handle_property method",self.adjudicator.handle_property,input_states,output_states)
        
    def test_update_state(self):
        input_state =  [
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [2,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ]
    
    def test_handle_cards_pre_turn(self):
        input_states =  [[
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [2,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            [7,9],#player's position; 2
            [1300,1380], #player's cash; 3
            0, #phase number; 4
            {} #phase payload; 5
        ]]
        
        print("Starting tests for handle_cards_pre_turn method")
        for i in range( len(input_states) ):
            current_player = input_states[i][0]%2
            current_position = input_states[i][2][current_player]
            deck_type = constants.board[current_position]['class']
            
            cards = constants.communityChestCards
            if deck_type == 'Chance':
                cards = constants.chanceCards
            
            for card in cards:
                input_modified = copy.deepcopy(input_states[i])
                self.adjudicator.handle_cards_pre_turn( input_modified ,card,deck_type )
                flag = True
                print("Card: "+deck_type+" "+str(card['id'])+", Text: "+str(card['content']))
                print("State before card effect: "+str(input_states[i]))
                print("State after card effect: "+str(input_modified))
        
	def test_case_1(self):
		input_state = [19, array([ 0,  0,  0, -1,  0,  0,  1,  0,  0,  1, -1,  0, -1,  0,  1, -1,  0,
        0,  0,  0,  1,  0,  0,  1,  0,  1,  0, -1,  0,  0]), [21, 6], [240, 540], 4, {}]
		actions = [True]
		no_of_turns = 1
		dice = [[2,5]]
		
		output_state = [19, array([ 0,  0,  0, -1,  0,  0,  1,  0,  0,  1, -1,  0, -1,  0,  1, -1,  0,
        0,  0,  0,  1,  0,  0,  1,  0,  1,  0, -1,  0,  0]), [21, 6], [240, 540], 4, {}]
        
	
	
test_adjudicator = Test_Adjudicator()
test_adjudicator.test_handle_property()
test_adjudicator.test_handle_cards_pre_turn()
test_adjudicator.test_update_state()

    