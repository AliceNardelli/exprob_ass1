#!/usr/bin/env python

import sys
import rospy
import actionlib
import exprob_ass1.msg
import math
import time

_as = None


def action_clbk(req):
  
    theta=math.atan(abs(req.actual_y-req.goal_y)/abs(req.actual_x-req.goal_x)) 
    rospy.loginfo('I am going to the '+ req.destination)
    distance=math.sqrt(pow(req.actual_y-req.goal_y, 2)+pow(req.actual_x-req.goal_x, 2))
    counter=distance 
    _fb = exprob_ass1.msg.MoveFeedback()
    _fb.feed_x= req.actual_x
    _fb.feed_y= req.actual_y
    _as.publish_feedback(_fb)
           
    while distance>0:
		   distance=distance-1
		   rospy.sleep(1)
		   if distance>0:
			   if req.actual_y-req.goal_y>0:
				   _fb.feed_y=_fb.feed_y-math.sin(theta)
			   else:
				   _fb.feed_y=_fb.feed_y+math.sin(theta)
			   if req.actual_x-req.goal_x>0:
				   _fb.feed_x=_fb.feed_x-math.cos(theta)
			   else:
				   _fb.feed_x=_fb.feed_x+math.cos(theta)
		 
		   else:
			   _fb.feed_x=req.goal_x
			   _fb.feed_y=req.goal_y
			   
		   _as.publish_feedback(_fb)
		   
    rospy.loginfo('I am arrived to the '+req.destination)
    _as.set_succeeded() 

if __name__ == '__main__':

       rospy.init_node('talker', anonymous=True)
       _as = actionlib.SimpleActionServer('move_action_server', exprob_ass1.msg.MoveAction,execute_cb=action_clbk, auto_start=False) 
       _as.start()  
       rospy.spin()
