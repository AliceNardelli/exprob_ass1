#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from armor_msgs.srv import ArmorDirective
import exprob_ass1.srv
import exprob_ass1.msg

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

client_armor=None
client_move=None
client_rnd_room=None
client_check_correct=None
client_announce=None
client_perceive_hints=None

def ontology_interaction(command,primary_command_spec,secondary_command_spec,arg):
	 global client_armor
	 msg = ArmorDirective()
	 msg.client_name = 'tutorial'
	 msg.reference_name = 'ontoTest'
	 msg.command = command
	 msg.primary_command_spec = primary_command_spec
	 msg.secondary_command_spec = secondary_command_spec
	 msg.args=arg
	 resp=client_armor(msg)
	 return resp
	 
def menage_response(resp):			
		    st = st.replace("<http://www.emarolab.it/cluedo-ontology#", "")
			st = st.replace(">", "")
			return st

class Inside_Room(smach.State):
    def __init__(self):
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['exit_from_room'],
                             input_keys=['room_in'],
                             output_keys=['room_out'])
        
    def execute(self, userdata):
        # function called when exiting from the node, it can be blacking
        time.sleep(5)
        actual_room=rospy.get_param(userdata.room_in)
        rospy.loginfo('I am inside '+actual_room[0])
        #find a way to state that you are inside a certain room
        rospy.wait_for_service('perceive_hints_service')
        perceived_hint=client_perceive_hints()
        if perceived_hint.perceived==1:
			#add perceived obj
			resp1=ontology_interface('ADD','OBJECTPROP','IND',[perceived_hint.description,perceived_hint.hypotesis,perceived_hint.value])
			#make inference
			resp2=ontology_interface('REASON','','',[])
        client_move.wait_for_server()
        goal_msg = exprob_ass1.msg.MoveGoal()
        goal_msg.destination='Corridor'
        goal_msg.actual_x=actual_room[1]
        goal_msg.actual_y=actual_room[2]
        goal_msg.goal_x=0
        goal_msg.goal_x=0
        client_move.send_goal(goal_msg)
        client_move.wait_for_result()
        userdata.room_out='room0'
        rospy.loginfo('I am exit'+actual_room[0])		
			
        
        return 'exit_from_room'
        
class Oracle_Room(smach.State):
    def __init__(self):
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['correct','no_correct'],
                             input_keys=['room_in'],
                             output_keys=['room_out'])
        
    def execute(self, userdata):
        # function called when exiting from the node, it can be blacking
        time.sleep(5)
        
        rospy.loginfo('I am inside Oracle Room')
        rospy.wait_for_service('announce_service')
        current_hypotesis=rospy.param_get('current_hypotesis')
        msg=AnnouncementRequest()
        msg.who=current_hypotesis[1]
        msg.where=current_hypotesis[2]
        msg.what=current_hypotesis[3]
        a=client_announce(msg)
        rospy.wait_for_service('check_correct_service')
        correct=client_check_correct(current_hypotesis[3])
        if correct:
			return 'correct'
        client_move.wait_for_server()
        goal_msg = exprob_ass1.msg.MoveGoal()
        goal_msg.destination='Corridor'
        goal_msg.actual_x=10
        goal_msg.actual_y=10
        goal_msg.goal_x=0
        goal_msg.goal_x=0
        client_move.send_goal(goal_msg)
        client_move.wait_for_result()
        userdata.room_out='room0'
        rospy.loginfo('I am exit'+actual_room[0])		
			
        
        return 'no_correct'
    

# define state Locked
class Out_Room(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['go_to_oracle','move_to_a_room'],
                             input_keys=['room_in'],
                             output_keys=['room_out']
               
                             )
        
        self.rate = rospy.Rate(200)  # Loop at 200 Hz

    def execute(self, userdata):
        
        while not rospy.is_shutdown():  
            time.sleep(1)
            #ask for complete hypotesis
            resp_c=add_ontology('QUERY','IND','CLASS',['COMPLETED'])
            #ask for incostintent hypotesis
            resp_i=add_ontology('QUERY','IND','CLASS',['INCONSISTENT'])
            #if the length is equal means that there is not consistent hypotesis to check
            if len(resp_i.armor_response.queried_objects)==len(resp_c.armor_response.queried_objects):
			   #extract randomly a room
               rospy.wait_for_service('random_room_service')
               random_room_resp=client_rnd_room()
               random_room=random_room_resp.random_room
               #getting room
               room=rospy.param_get(random_room)
               client_move.wait_for_server()
               goal_msg = exprob_ass1.msg.MoveGoal()
               goal_msg.destination=room[0]
               goal_msg.actual_x=0
               goal_msg.actual_y=0
               goal_msg.goal_x=room[1]
               goal_msg.goal_x=room[2]
               client_move.send_goal(goal_msg)
               client_move.wait_for_result()
               userdata.room_out=random_room
               return 'search_hints'
            else:
				complete=[]
				for i in range (0 , len(resp_c.armor_response.queried_objects)-1):
				     st=menage_response(resp_c.armor_response.queried_objects[i])
				     complete.append(st)
				for i in range (0 , len(resp_i.armor_response.queried_objects)-1):
					 st=menage_response(resp_i.armor_response.queried_objects[i])
				     complete.remove(st)
			   
			   #query about the hypotesis 
               consitent_who=add_ontology('QUERY','OBJECTPROP','IND',['who',complete[0])
               who=menage_response(resp_c.armor_response.queried_objects)
               consitent_where=add_ontology('QUERY','OBJECTPROP','IND',['where',complete[0])
               where=menage_response(resp_c.armor_response.queried_objects)
               consitent_what=add_ontology('QUERY','OBJECTPROP','IND',['what',complete[0])
               what=menage_response(resp_c.armor_response.queried_objects)
			   
               #store the consisten hypotesis in the parameter server

			   rospy.param_set('current_hypotesis',[complete[0],who,where,what])
				#getting room
               room=rospy.param_get('room10')
               client_move.wait_for_server()
               goal_msg = exprob_ass1.msg.MoveGoal()
               goal_msg.destination=room[0]
               goal_msg.actual_x=0
               goal_msg.actual_y=0
               goal_msg.goal_x=room[1]
               goal_msg.goal_x=room[2]
               client_move.send_goal(goal_msg)
               client_move.wait_for_result()
               userdata.room_out='room10'
               return 'go_to_oracle'
					 
               
                
		    
            self.rate.sleep
            

        
def main():
    rospy.init_node('FSM')
    
    
    
	client_armor = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
	client_move= actionlib.SimpleActionClient('move_action_server', exprob_ass1.msg.Moving)
    client_rnd_room=rospy.ServiceProxy('random_room_service', RandomRoom)
    client_check_correct=rospy.ServiceProxy('check_correct_service', CheckCorrect)
    client_announce=rospy.ServiceProxy('announce_service', Announcement)
    client_perceive_hints=rospy.ServiceProxy('perceive_hints_service', PerceiveHints)
    #load ontology
    rospy.wait_for_service('armor_interface_srv')
    resp1=ontology_interaction('LOAD','FILE','',['/root/ros_ws/src/exprob_ass1/cluedo_ontology.owl', 'http://www.emarolab.it/cluedo-ontology', 'true', 'PELLET', 'true'])
    #declare state machine
    sm = smach.StateMachine(outcomes=['game_finished'])
    sm.userdata.actual_room = 'room0'
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('OUT_ROOM', Out_Room(), 
                               transitions={'go_to_oracle':'ORACLE_ROOM',
                                            'search_hints':'INSIDE_ROOM'
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
