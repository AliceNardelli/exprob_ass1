#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from armor_msgs.srv import ArmorDirective
from exprob_ass1.srv import RandomRoom , CheckCorrect, Announcement, PerceiveHints, AnnouncementRequest
from exprob_ass1.msg import MoveAction, MoveGoal
import actionlib
import actionlib_msgs

# INSTALLATION
# - create ROS package in your workspace:
#          $ catkin_create_pkg smach_tutorial std_msgs rospy
# - move this file to the 'smach_tutorial/scr' folder and give running permissions to it with
#          $ chmod +x state_machine.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun smach_tutorial state_machine.py
# - install the visualiser using
#          $ sudo apt-get install ros-kinetic-smach-viewer
# - run the visualiser with
#          $ rosrun smach_viewer smach_viewer.py





def ontology_interaction(
    command,
    primary_command_spec,
    secondary_command_spec,
     arg):
     
     global client_armor
     rospy.wait_for_service('armor_interface_srv')
     
     msg = ArmorDirective()
     msg.client_name = 'tutorial'
     msg.reference_name = 'ontoTest'
     msg.command = command
     msg.primary_command_spec = primary_command_spec
     msg.secondary_command_spec = secondary_command_spec
     msg.args = arg
     resp = client_armor(msg)
     
     return resp


def menage_response(st):
            
            st = st.replace("<http://www.emarolab.it/cluedo-ontology#", "")
            print(st)
            st = st.replace(">", "")
            print(st)
            return st


class Inside_Room(smach.State):
    def __init__(self):
    	smach.State.__init__(self,
                             outcomes=['exit_from_room'],
                             input_keys=['room_in'],
                             output_keys=['room_out'])

    def execute(self, userdata):
        global client_move, client_rnd_room, client_check_correct, client_announce, client_perceive_hints
        time.sleep(1)
        actual_room = rospy.get_param(userdata.room_in)
        rospy.loginfo('I am inside ' + actual_room[0])
        rospy.wait_for_service('perceive_hints_service')
        perceived_hint = client_perceive_hints()
        
        if perceived_hint.perceived == 1:
            r1 = ontology_interaction('ADD', 'OBJECTPROP', 'IND', [perceived_hint.description, perceived_hint.hypotesis, perceived_hint.value])
            
            if perceived_hint.description=='where':
               resp=ontology_interaction('ADD','IND','CLASS',[perceived_hint.value,'PLACE'])
            elif perceived_hint.description=='what':
               resp=ontology_interaction('ADD','IND','CLASS',[perceived_hint.value,'WEAPON'])
            else:
               resp=ontology_interaction('ADD','IND','CLASS',[perceived_hint.value,'PERSON'])
            r2 = ontology_interaction('REASON', '', '', [])
        client_move.wait_for_server()
        goal_msg = MoveGoal()
        goal_msg.destination = 'Corridor'
        goal_msg.actual_x = int(actual_room[1])
        goal_msg.actual_y = int(actual_room[2])
        goal_msg.goal_x = 0
        goal_msg.goal_x = 0
        #client_move.send_goal(goal_msg)
        #client_move.wait_for_result()
        userdata.room_out = 'room0'
        rospy.loginfo('I am exit' + actual_room[0])

        return 'exit_from_room'


class Oracle_Room(smach.State):
    def __init__(self):
        # initialisation function, it should not wait
        smach.State.__init__(self,
                             outcomes=['correct', 'not_correct'],
                             input_keys=['room_in'],
                             output_keys=['room_out'])

    def execute(self, userdata):
        global client_move, client_rnd_room, client_check_correct, client_announce, client_perceive_hints

        # function called when exiting from the node, it can be blacking
        time.sleep(1)

        rospy.loginfo('I am inside Oracle Room')
        rospy.wait_for_service('announce_service')
        current_hypotesis = rospy.get_param('current_hypotesis')
        msg = AnnouncementRequest()
        msg.who = current_hypotesis[1]
        msg.where = current_hypotesis[2]
        msg.what = current_hypotesis[3]
        a = client_announce(msg)
        rospy.wait_for_service('check_correct_service')
        resp = client_check_correct(current_hypotesis[0])
        if resp.correct==1:
             return 'correct'
        client_move.wait_for_server()
        goal_msg = MoveGoal()
        goal_msg.destination = 'Corridor'
        goal_msg.actual_x = 10
        goal_msg.actual_y = 10
        goal_msg.goal_x = 0
        goal_msg.goal_x = 0
        #client_move.send_goal(goal_msg)
        #client_move.wait_for_result()
        userdata.room_out = 'room0'
        r1=ontology_interaction('REMOVE','IND','',[current_hypotesis[0]])
        r2=ontology_interaction('REASON','','',[])
        rospy.loginfo('I am exit from Oracle Room')

        return 'not_correct'


# define state Locked
class Out_Room(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['go_to_oracle', 'move_to_a_room'],
                             input_keys=['room_in'],
                             output_keys=['room_out']

                             )

        self.rate = rospy.Rate(200)  # Loop at 200 Hz

    def execute(self, userdata):
        global client_move, client_rnd_room, client_check_correct, client_announce, client_perceive_hints
        while not rospy.is_shutdown():
            time.sleep(1)
            # ask for complete hypotesis
            resp_c = ontology_interaction('QUERY', 'IND', 'CLASS', ['COMPLETED'])
            print(resp_c)
            print(len(resp_c.armor_response.queried_objects))
            # ask for incostintent hypotesis
            resp_i = ontology_interaction('QUERY', 'IND', 'CLASS', ['INCONSISTENT'])
            print(resp_i)
            print(len(resp_i.armor_response.queried_objects))

            # if the length is equal means that there is not consistent
            # hypotesis to check
            if len(
    resp_i.armor_response.queried_objects) == len(
        resp_c.armor_response.queried_objects):
			   # extract randomly a room
               rospy.wait_for_service('random_room_service')
               random_room_resp = client_rnd_room()
               random_room = random_room_resp.random_room
               # getting room
               room = rospy.get_param(random_room)
               print(room)
               print(random_room)
               client_move.wait_for_server()
               goal_msg =MoveGoal()
               goal_msg.destination = room[0]
               goal_msg.actual_x = 0
               goal_msg.actual_y = 0
               goal_msg.goal_x = int(room[1])
               goal_msg.goal_x = int(room[2])
               #client_move.send_goal(goal_msg)
               #client_move.wait_for_result()
               userdata.room_out = random_room
               return 'move_to_a_room'
            else:
                complete = []
                print(resp_c.armor_response.queried_objects[0])
                print(resp_c.armor_response.queried_objects[0])
                for i in range(len(resp_c.armor_response.queried_objects)):
                     print(resp_c.armor_response.queried_objects[i])
                     st = menage_response(resp_c.armor_response.queried_objects[i])
                     complete.append(st)
                     print(st)
                     print(complete)
                if len(resp_i.armor_response.queried_objects)>0:
                  for i in range(len(resp_i.armor_response.queried_objects)):
                       st = menage_response(resp_i.armor_response.queried_objects[i])
                       complete.remove(st)
                       print(complete)
			   
			   # query about the hypotesis 
                print(complete)
                consistent_who=ontology_interaction('QUERY','OBJECTPROP','IND',['who',complete[0]])
                
                who=menage_response(consistent_who.armor_response.queried_objects[0])
                consistent_where=ontology_interaction('QUERY','OBJECTPROP','IND',['where',complete[0]])
                where=menage_response(consistent_where.armor_response.queried_objects[0])
                consistent_what=ontology_interaction('QUERY','OBJECTPROP','IND',['what',complete[0]])
                what=menage_response(consistent_what.armor_response.queried_objects[0])
			   
                # store the consisten hypotesis in the parameter server
                rospy.set_param('current_hypotesis',[complete[0],who,where,what])
				# getting room
                room=rospy.get_param('room10')
                client_move.wait_for_server()
                goal_msg = MoveGoal()
                goal_msg.destination=room[0]
                goal_msg.actual_x=0
                goal_msg.actual_y=0
                goal_msg.goal_x=int(room[1])
                goal_msg.goal_x=int(room[2])
                #client_move.send_goal(goal_msg)
                #client_move.wait_for_result()
                userdata.room_out='room10'
                return 'go_to_oracle'
					 
               
                
		    
            self.rate.sleep
            

        
def main():
    global client_move, client_rnd_room, client_check_correct, client_announce, client_perceive_hints, client_armor
    rospy.init_node('FSM')
    client_armor = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)    
    client_move= actionlib.SimpleActionClient('move_action_server', MoveAction)
    client_rnd_room=rospy.ServiceProxy('random_room_service', RandomRoom)
    client_check_correct=rospy.ServiceProxy('check_correct_service', CheckCorrect)
    client_announce=rospy.ServiceProxy('announce_service', Announcement)
    client_perceive_hints=rospy.ServiceProxy('perceive_hints_service', PerceiveHints)
    # load ontology

    
    ontology=rospy.get_param('ontology')
    ontology_path=rospy.get_param('ontology_path')
   
    resp1=ontology_interaction('LOAD','FILE','',[ontology_path, ontology, 'true', 'PELLET', 'true'])
    # declare state machine
    sm = smach.StateMachine(outcomes=['game_finished'])
    sm.userdata.actual_room = 'room0'
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('OUT_ROOM', Out_Room(), 
                               transitions={'go_to_oracle':'ORACLE_ROOM',
                                            'move_to_a_room':'INSIDE_ROOM'
                                           },
                               remapping={'room_in':'actual_room', 
                                          'room_out':'actual_room'})
                                          
        smach.StateMachine.add('INSIDE_ROOM', Inside_Room(), 
                               transitions={'exit_from_room':'OUT_ROOM'},
                               remapping={'room_in':'actual_room', 
                                          'room_out':'actual_room'}
                               )
                              
        smach.StateMachine.add('ORACLE_ROOM', Oracle_Room(), 
                               transitions={'not_correct':'OUT_ROOM', 
                                            'correct':'game_finished'},
                               remapping={'room_in':'actual_room', 
                                          'room_out':'actual_room'}
                               )


    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
