#! /usr/bin/env python

import rospy
import random
from exprob_ass1.srv import RandomRoom,RandomRoomResponse

def random_room_clbk(req):

    msg=RandomRoomResponse()
    msg.random_room='room'+str(random.randint(1,9))
    
    
    return msg


def main():
    #init node
    rospy.init_node('random_room_service')
    #init service
    srv = rospy.Service('random_room_service', RandomRoom, random_room_clbk)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
      
        rate.sleep()


if __name__ == '__main__':
    main()
