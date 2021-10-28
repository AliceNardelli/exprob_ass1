
# Experimental Robotics Laboratory Course
##Assignment 1

## Brief introduction
The aim of this assignment is to design a software behavioural architecture which simulates an autonomous Cluedo game. The robot which is the player wants to find who is the murder, where he killed the victime and which weapon has been used. According to that it goes around to an appartement looking for hints, makes hypotesis about the murder and reasons about these. Once it finds a complete hypotesis (which contains a person, a place and a weapon) it goes to the oracle room and asks if the hypotesis is correct. If hypotesis is not correct robot goes on looking for hints otherwise game finishes.





rosrun armor execute it.emarolab.armor.ARMORMainService

rosparam load my_params.yaml
catkin_make --only-pkg-with-deps exprob_ass1
autopep8 --in-place --aggressive --aggressive <filename>


rndm room generator
look around server
move action


The apartment is arranged as a matrix according to the figure so each room is associated to a point (x,y), movement is on a straigth line at costant velocity. This choise to simulate a little bit movent instead of only wait

perception with srv:
    look around action which call subscribes one hint to a publisher which read hints from rosparam, difficult to manage no percetion case. Good idea since typically we subscribes to an hint
    divide the look around action behaviour and perception srv. No much sense.
The possibility of not perceive an hint is always 1/4. Logically it is possible also to randomize this aspect


2.1.1	Miss Scarlett
2.1.2	Colonel Mustard
2.1.3	Mrs. White
2.1.4	Reverend / Mr. Green
2.1.5	Mrs. Peacock
2.1.6	Professor Plum

Revolver.
Dagger.
Lead Pipe.
Rope.
Candlestick.
Wrench.
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

2.1.1	Miss Scarlett
2.1.2	Colonel Mustard
2.1.3	Mrs. White
2.1.4	Reverend / Mr. Green
2.1.5	Mrs. Peacock
2.1.6	Professor Plum

Revolver.
Dagger.
Lead Pipe.
Rope.
Candlestick.
Wrench.

Ballroom
Billiard Room
Conservatory
Dining Room
Hall
Kitchen
Lounge
Library
Study


hint1: ['HP6','who','White']
hint2: ['HP6','what','Candlestick']
hint3: ['HP6','where','Study']
hint4: ['HP7','who','Scarlett']
hint5: ['HP7','who','Green']
hint6: ['HP7','what','Rope']
hint7: ['HP9','who','Green']
hint8: ['HP9','what','Lead Pipe']
hint9: ['HP9','where',Conservatory']
hint10: ['HP10','where','Kitchen']
hint11: ['HP10','where','Lounge']
hint12: ['HP10','what','Wrench']

hint1: ['HP1','where','Hall']   
hint2: ['HP1','who','Plum']
hint3: ['HP1','what','Rope']
hint4: ['HP2','what','Wrench']
hint5: ['HP2','wha','Dagger']
hint6: ['HP2','where','Library']
hint7: ['HP3','where','Conservatory']   
hint8: ['HP3','who','Green']
hint10: ['HP4','what','Lead Pipe']
hint11: ['HP4','who','Peacock']
hint12: ['HP4','where','Lounge']
hint13: ['HP5','where','Dining Room']
hint14: ['HP5','what','Rope']
hint15: ['HP6','who','White']
hint16: ['HP6','what','Candlestick']
hint17: ['HP6','where','Study']
hint18: ['HP7','who','Scarlett']
hint19: ['HP7','who','Green']
hint20: ['HP7','what','Rope']
hint21: ['HP8','who',Peacock']
hint22: ['HP8','what','Wrench']
hint23: ['HP9','who','Green']
hint24: ['HP9','what','Lead Pipe']
hint25: ['HP9','where',Conservatory']
hint26: ['HP10','where','Kitchen']
hint27: ['HP10','where','Lounge']
hint28: ['HP10','what','Wrench']






