"""TODO:Ensure board can't be modified by agents""" 

board = {
-1:{
"class":"Jail",
"name":"Jail",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
0:{
"class":"Idle",
"name":"Go",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
1:{
"class":"Street",
"name":"Mediterranean Avenue",
"monopoly":"Brown",
"monopoly_size":2,
"price":60,
"build_cost":50,
"rent":2,
"rent_house_1":10,
"rent_house_2":30,
"rent_house_3":90,
"rent_house_4":160,
"rent_hotel":250,
"tax":0,
"monopoly_group_elements":[3]
},
2:{
"class":"Chest",
"name":"Community Chest",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
3:{
"class":"Street",
"name":"Baltic Avenue",
"monopoly":"Brown",
"monopoly_size":2,
"price":60,
"build_cost":50,
"rent":4,
"rent_house_1":20,
"rent_house_2":60,
"rent_house_3":180,
"rent_house_4":320,
"rent_hotel":450,
"tax":0,
"monopoly_group_elements":[1]
},
4:{
"class":"Tax",
"name":"Income Tax",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":200
},
5:{
"class":"Railroad",
"name":"Reading Railroad",
"monopoly":"Railroad",
"monopoly_size":4,
"price":200,
"build_cost":0,
"rent":25,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0,
"monopoly_group_elements":[15, 25, 35]
},
6:{
"class":"Street",
"name":"Oriental Avenue",
"monopoly":"Light Blue",
"monopoly_size":3,
"price":100,
"build_cost":50,
"rent":6,
"rent_house_1":30,
"rent_house_2":90,
"rent_house_3":270,
"rent_house_4":400,
"rent_hotel":550,
"tax":0,
"monopoly_group_elements":[8, 9]
},
7:{
"class":"Chance",
"name":"Chance",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
8:{
"class":"Street",
"name":"Vermont Avenue",
"monopoly":"Light Blue",
"monopoly_size":3,
"price":100,
"build_cost":50,
"rent":6,
"rent_house_1":30,
"rent_house_2":90,
"rent_house_3":270,
"rent_house_4":400,
"rent_hotel":550,
"tax":0,
"monopoly_group_elements":[6, 9]
},
9:{
"class":"Street",
"name":"Connecticut Avenue",
"monopoly":"Light Blue",
"monopoly_size":3,
"price":120,
"build_cost":50,
"rent":8,
"rent_house_1":40,
"rent_house_2":100,
"rent_house_3":300,
"rent_house_4":450,
"rent_hotel":600,
"tax":0,
"monopoly_group_elements":[6, 8]
},
10:{
"class":"Idle",
"name":"Jail",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
11:{
"class":"Street",
"name":"St. Charles Place",
"monopoly":"Pink",
"monopoly_size":3,
"price":140,
"build_cost":100,
"rent":10,
"rent_house_1":50,
"rent_house_2":150,
"rent_house_3":450,
"rent_house_4":625,
"rent_hotel":750,
"tax":0,
"monopoly_group_elements":[13, 14]
},
12:{
"class":"Utility",
"name":"Electric Company",
"monopoly":"Utility",
"monopoly_size":2,
"price":150,
"build_cost":0,
"rent":4,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0,
"monopoly_group_elements":[28]
},
13:{
"class":"Street",
"name":"States Avenue",
"monopoly":"Pink",
"monopoly_size":3,
"price":140,
"build_cost":100,
"rent":10,
"rent_house_1":50,
"rent_house_2":150,
"rent_house_3":450,
"rent_house_4":625,
"rent_hotel":750,
"tax":0,
"monopoly_group_elements":[11, 14]
},
14:{
"class":"Street",
"name":"Virginia Avenue",
"monopoly":"Pink",
"monopoly_size":3,
"price":160,
"build_cost":100,
"rent":12,
"rent_house_1":60,
"rent_house_2":180,
"rent_house_3":500,
"rent_house_4":700,
"rent_hotel":900,
"tax":0,
"monopoly_group_elements":[11, 13]
},
15:{
"class":"Railroad",
"name":"Pennsylvania Railroad",
"monopoly":"Railroad",
"monopoly_size":4,
"price":200,
"build_cost":0,
"rent":25,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0,
"monopoly_group_elements":[5, 25, 35]
},
16:{
"class":"Street",
"name":"St. James Place",
"monopoly":"Orange",
"monopoly_size":3,
"price":180,
"build_cost":100,
"rent":14,
"rent_house_1":70,
"rent_house_2":200,
"rent_house_3":550,
"rent_house_4":750,
"rent_hotel":950,
"tax":0,
"monopoly_group_elements":[18, 19]
},
17:{
"class":"Chest",
"name":"Community Chest",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
18:{
"class":"Street",
"name":"Tennessee Avenue",
"monopoly":"Orange",
"monopoly_size":3,
"price":180,
"build_cost":100,
"rent":14,
"rent_house_1":70,
"rent_house_2":200,
"rent_house_3":550,
"rent_house_4":750,
"rent_hotel":950,
"tax":0,
"monopoly_group_elements":[16, 19]
},
19:{
"class":"Street",
"name":"New York Avenue",
"monopoly":"Orange",
"monopoly_size":3,
"price":200,
"build_cost":100,
"rent":16,
"rent_house_1":80,
"rent_house_2":220,
"rent_house_3":600,
"rent_house_4":800,
"rent_hotel":1000,
"tax":0,
"monopoly_group_elements":[16, 18]
},
20:{
"class":"Idle",
"name":"Free Parking",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
21:{
"class":"Street",
"name":"Kentucky Avenue",
"monopoly":"Red",
"monopoly_size":3,
"price":220,
"build_cost":150,
"rent":18,
"rent_house_1":90,
"rent_house_2":250,
"rent_house_3":700,
"rent_house_4":875,
"rent_hotel":1050,
"tax":0,
"monopoly_group_elements":[23, 24]
},
22:{
"class":"Chance",
"name":"Chance",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
23:{
"class":"Street",
"name":"Indiana Avenue",
"monopoly":"Red",
"monopoly_size":3,
"price":220,
"build_cost":150,
"rent":18,
"rent_house_1":90,
"rent_house_2":250,
"rent_house_3":700,
"rent_house_4":875,
"rent_hotel":1050,
"tax":0,
"monopoly_group_elements":[21, 24]
},
24:{
"class":"Street",
"name":"Illinois Avenue",
"monopoly":"Red",
"monopoly_size":3,
"price":240,
"build_cost":150,
"rent":20,
"rent_house_1":100,
"rent_house_2":300,
"rent_house_3":750,
"rent_house_4":925,
"rent_hotel":1100,
"tax":0,
"monopoly_group_elements":[21, 23]
},
25:{
"class":"Railroad",
"name":"B. & O. Railroad",
"monopoly":"Railroad",
"monopoly_size":4,
"price":200,
"build_cost":0,
"rent":25,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0,
"monopoly_group_elements":[5, 15, 35]
},
26:{
"class":"Street",
"name":"Atlantic Avenue",
"monopoly":"Yellow",
"monopoly_size":3,
"price":260,
"build_cost":150,
"rent":22,
"rent_house_1":110,
"rent_house_2":330,
"rent_house_3":800,
"rent_house_4":975,
"rent_hotel":1150,
"tax":0,
"monopoly_group_elements":[27, 29]
},
27:{
"class":"Street",
"name":"Ventnor Avenue",
"monopoly":"Yellow",
"monopoly_size":3,
"price":260,
"build_cost":150,
"rent":22,
"rent_house_1":110,
"rent_house_2":330,
"rent_house_3":800,
"rent_house_4":975,
"rent_hotel":1150,
"tax":0,
"monopoly_group_elements":[26, 29]
},
28:{
"class":"Utility",
"name":"Water Works",
"monopoly":"Utility",
"monopoly_size":2,
"price":150,
"build_cost":0,
"rent":4,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0,
"monopoly_group_elements":[12]
},
29:{
"class":"Street",
"name":"Marvin Gardens",
"monopoly":"Yellow",
"monopoly_size":3,
"price":280,
"build_cost":150,
"rent":24,
"rent_house_1":120,
"rent_house_2":360,
"rent_house_3":850,
"rent_house_4":1025,
"rent_hotel":1200,
"tax":0,
"monopoly_group_elements":[26, 27]
},
30:{
"class":"GoToJail",
"name":"Go To Jail",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
31:{
"class":"Street",
"name":"Pacific Avenue",
"monopoly":"Green",
"monopoly_size":3,
"price":300,
"build_cost":200,
"rent":26,
"rent_house_1":130,
"rent_house_2":390,
"rent_house_3":900,
"rent_house_4":1100,
"rent_hotel":1275,
"tax":0,
"monopoly_group_elements":[32, 34]
},
32:{
"class":"Street",
"name":"North Carolina Avenue",
"monopoly":"Green",
"monopoly_size":3,
"price":300,
"build_cost":200,
"rent":26,
"rent_house_1":130,
"rent_house_2":390,
"rent_house_3":900,
"rent_house_4":1100,
"rent_hotel":1275,
"tax":0,
"monopoly_group_elements":[31, 34]
},
33:{
"class":"Chest",
"name":"Community Chest",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
34:{
"class":"Street",
"name":"Pennsylvania Avenue",
"monopoly":"Green",
"monopoly_size":3,
"price":320,
"build_cost":200,
"rent":28,
"rent_house_1":150,
"rent_house_2":450,
"rent_house_3":1000,
"rent_house_4":1200,
"rent_hotel":1400,
"tax":0,
"monopoly_group_elements":[31, 32]
},
35:{
"class":"Railroad",
"name":"Short Line",
"monopoly":"Railroad",
"monopoly_size":4,
"price":200,
"build_cost":0,
"rent":25,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0,
"monopoly_group_elements":[5, 15, 25]
},
36:{
"class":"Chance",
"name":"Chance",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":0
},
37:{
"class":"Street",
"name":"Park Place",
"monopoly":"Dark Blue",
"monopoly_size":2,
"price":350,
"build_cost":200,
"rent":35,
"rent_house_1":175,
"rent_house_2":500,
"rent_house_3":1100,
"rent_house_4":1300,
"rent_hotel":1500,
"tax":0,
"monopoly_group_elements":[39]
},
38:{
"class":"Tax",
"name":"Luxury Tax",
"monopoly":"None",
"monopoly_size":0,
"price":0,
"build_cost":0,
"rent":0,
"rent_house_1":0,
"rent_house_2":0,
"rent_house_3":0,
"rent_house_4":0,
"rent_hotel":0,
"tax":100
},
39:{
"class":"Street",
"name":"Boardwalk",
"monopoly":"Dark Blue",
"monopoly_size":2,
"price":400,
"build_cost":200,
"rent":50,
"rent_house_1":200,
"rent_house_2":600,
"rent_house_3":1400,
"rent_house_4":1700,
"rent_hotel":2000,
"tax":0,
"monopoly_group_elements":[37]
}
}

space_to_property_map = {
1:0,
3:1,
5:2,
6:3,
8:4,
9:5,
11:6,
12:7,
13:8,
14:9,
15:10,
16:11,
18:12,
19:13,
21:14,
23:15,
24:16,
25:17,
26:18,
27:19,
28:20,
29:21,
31:22,
32:23,
34:24,
35:25,
37:26,
39:27
}

property_to_space_map = {
0:1,
1:3,
2:5,
3:6,
4:8,
5:9,
6:11,
7:12,
8:13,
9:14,
10:15,
11:16,
12:18,
13:19,
14:21,
15:23,
16:24,
17:25,
18:26,
19:27,
20:28,
21:29,
22:31,
23:32,
24:34,
25:35,
26:37,
27:39
}

communityChestCards = [
  {
    "id": 0,
    "content": "Advance to Go (Collect $200)",
    "type": 3,
    "position": 1,
    "money": 0,
    "money2": 0
  },
  {
    "id": 1,
    "content": "Bank error in your favor, collect $200",
    "type": 1,
    "position": 0,
    "money": 200,
    "money2": 0
  },
  {
    "id": 2,
    "content": "Doctor's fees, Pay $50",
    "type": 1,
    "position": 0,
    "money": -50,
    "money2": 0
  },
  {
    "id": 3,
    "content": "From sale of stock you get $50",
    "type": 1,
    "position": 0,
    "money": 50,
    "money2": 0
  },
  {
    "id": 4,
    "content": "Get out of jail free, this card may be kept until needed",
    "type": 4,
    "position": 0,
    "money": 0,
    "money2": 0
  },
  {
    "id": 5,
    "content": "Go to jail, go directly to jail – Do not pass Go, do not collect $200",
    "type": 3,
    "position": -1,
    "money": 0,
    "money2": 0
  },
  {
    "id": 6,
    "content": "Grand Opera Night. Collect $50 from every player for opening night seats.",
    "type": 2,
    "position": 0,
    "money": 50,
    "money2": 0
  },
  {
    "id": 7,
    "content": "Holiday Fund matures - Receive $100",
    "type": 1,
    "position": 0,
    "money": 100,
    "money2": 0
  },
  {
    "id": 8,
    "content": "Income Tax refund. Collect $20",
    "type": 1,
    "position": 0,
    "money": 20,
    "money2": 0
  },
  {
    "id": 9,
    "content": "Life Insurance Matures - Collect $100",
    "type": 1,
    "position": 0,
    "money": 100,
    "money2": 0
  },
  {
    "id": 10,
    "content": "Pay Hospital Fees of $50",
    "type": 1,
    "position": 0,
    "money": -50,
    "money2": 0
  },
  {
    "id": 11,
    "content": "Pay School Fees of $50",
    "type": 1,
    "position": 0,
    "money": -50,
    "money2": 0
  },
  {
    "id": 12,
    "content": "Receive $25 Consultancy Fee",
    "type": 1,
    "position": 0,
    "money": 25,
    "money2": 0
  },
  {
    "id": 13,
    "content": "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.",
    "type": 5,
    "position": 0,
    "money": -40,
    "money2": -115
  },
  {
    "id": 14,
    "content": "You have won second prize in a beauty contest– collect $10",
    "type": 1,
    "position": 0,
    "money": 10,
    "money2": 0
  },
  {
    "id": 15,
    "content": "You inherit $100",
    "type": 1,
    "position": 0,
    "money": 100,
    "money2": 0
  }
]

chanceCards = [
  {
    "id": 0,
    "content": "Advance to Go (Collect $200)",
    "type": 3,
    "position": 1,
    "money": 0,
    "money2": 0
  },
  {
    "id": 1,
    "content": "Advance to Illinois Ave. If you pass Go, collect $200.",
    "type": 3,
    "position": 25,
    "money": 0,
    "money2": 0
  },
  {
    "id": 2,
    "content": "Advance to St. Charles Place. If you pass Go, collect $200",
    "type": 3,
    "position": 12,
    "money": 0,
    "money2": 0
  },
  {
    "id": 3,
    "content": "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 times the amount thrown.",
    "type": 7,
    "position": 0,
    "money": 0,
    "money2": 0
  },
  {
    "id": 4,
    "content": "Advance token to the nearest Railroad and pay owner twice the rental to which he/she {he} is otherwise entitled. If Railroad is unowned, you may buy it from the Bank",
    "type": 6,
    "position": 0,
    "money": 0,
    "money2": 0
  },
  {
    "id": 5,
    "content": "Advance token to the nearest Railroad and pay owner twice the rental to which he/she {he} is otherwise entitled. If Railroad is unowned, you may buy it from the Bank",
    "type": 6,
    "position": 0,
    "money": 0,
    "money2": 0
  },
  {
    "id": 6,
    "content": "Bank pays you dividend of $50",
    "type": 1,
    "position": 0,
    "money": 50,
    "money2": 0
  },
  {
    "id": 7,
    "content": "Get out of Jail free, this card may be kept until needed, or traded",
    "type": 4,
    "position": 0,
    "money": 0,
    "money2": 0
  },
  {
    "id": 8,
    "content": "Go Back 3 Spaces",
    "type": 8,
    "position": 0,
    "money": 0,
    "money2": 0
  },
  {
    "id": 9,
    "content": "Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200.",
    "type": 3,
    "position": -1,
    "money": 0,
    "money2": 0
  },
  {
    "id": 10,
    "content": "Make general repairs on all your property: For each house pay $25, For each hotel {pay} $100.",
    "type": 5,
    "position": 0,
    "money": -25,
    "money2": -100
  },
  {
    "id": 11,
    "content": "Pay poor tax of $15",
    "type": 1,
    "position": 0,
    "money": 15,
    "money2": 0
  },
  {
    "id": 12,
    "content": "Take a trip to Reading Railroad.",
    "type": 3,
    "position": 6,
    "money": 0,
    "money2": 0
  },
  {
    "id": 13,
    "content": "Advance to Boardwalk",
    "type": 3,
    "position": 40,
    "money": 0,
    "money2": 0
  },
  {
    "id": 14,
    "content": "You have been elected chairman of the board, pay each player $50",
    "type": 2,
    "position": 0,
    "money": -50,
    "money2": 0
  },
  {
    "id": 15,
    "content": "Your building loan matures, collect $150",
    "type": 1,
    "position": 0,
    "money": 150,
    "money2": 0
  }
]

state_history = []
