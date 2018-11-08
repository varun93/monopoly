import adjudicator

class Test_Adjudicator:
    
    def __init__(self):
        self.adjudicator = adjudicator.Adjudicator()
    
    def test_handle_property(self):
        input_states =  [[
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            (12,9),#player's position; 2
            (1300,1380), #player's cash; 3
            0, #phase number; 4
            None #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            (9,9),#player's position; 2
            (1300,1380), #player's cash; 3
            0, #phase number; 4
            None #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            (9,9),#player's position; 2
            (1300,1380), #player's cash; 3
            0, #phase number; 4
            None #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,-1,-1,-2,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            (9,9),#player's position; 2
            (1300,1380), #player's cash; 3
            0, #phase number; 4
            None #phase payload; 5
        ],
        [
            2, #player turn; 0
            [0,0,1,-1,-1,-2,0,0,0,0,-1,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0], #player properties; 1
            (15,9),#player's position; 2
            (1300,1380), #player's cash; 3
            0, #phase number; 4
            None #phase payload; 5
        ]
        ]
        output_states =  [{'phase': 3, 'phase_properties': {'cash': 150, 'source': 'bank'}},
                          {'phase_properties': {'cash': 8, 'source': 'opponent'}},
                          {'phase_properties': {'cash': 16, 'source': 'opponent'}},
                          {'phase_properties': {'cash': 40, 'source': 'opponent'}},
                          {'phase_properties': {'cash': 50, 'source': 'opponent'}}]
        
        for i in range( len(input_states) ):
            output = self.adjudicator.handle_property( input_states[i] )
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

test_adjudicator = Test_Adjudicator()
test_adjudicator.test_handle_property()
        
    
    