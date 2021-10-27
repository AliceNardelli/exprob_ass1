#! /usr/bin/env python

import rospy
import random
from exprob_ass1.srv import PerceiveHints, PerceiveHintsResponse


def perc_clbk(req):
    msg = PerceiveHintsResponse()
    perceived = random.randint(0, 3)
    if perceived == 0:
        msg.perceived = 0
        rospy.loginfo('nothing perceived')
    else:
        no_hints = rospy.get_param("/no_hints")
        rndm_hint = random.randint(1, no_hints)
        perceived_hint = rospy.get_param("/hint" + str(rndm_hint))
            
        msg.perceived = 1
        msg.hypotesis = perceived_hint[0]
        msg.description = perceived_hint[1]
        msg.value = perceived_hint[2]
        rospy.loginfo(msg.hypotesis+':'+msg.description+' '+msg.value )
        #rospy.delete_param("/hint" + str(rndm_hint))    

    return msg


def main():
    # init node
    rospy.init_node('perceive_hints_service')
    # init service
    srv = rospy.Service('perceive_hints_service', PerceiveHints, perc_clbk)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        rate.sleep()


if __name__ == '__main__':
    main()
