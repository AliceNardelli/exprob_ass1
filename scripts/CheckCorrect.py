#! /usr/bin/env python

import rospy
import random
from exprob_ass1.srv import CheckCorrect

def check_correct_clbk(req):
	hypotesis=req.hypotesis
	if hypotesis==rospy.get_param('/correct_hypotesis'):
		
		rospy.loginfo(hypotesis +' hypotesis is correct!! ')
		return 1
	
	rospy.loginfo(hypotesis +' hypotesis is not correct ')
	return 0



def main():
    #init node
    rospy.init_node('check_correct_service')
    #init service
    srv = rospy.Service('check_correct_service', CheckCorrect, check_correct_clbk)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
      
        rate.sleep()


if __name__ == '__main__':
    main()
