#! /usr/bin/env python

import rospy
import random
from exprob_ass1.srv import Announcement,AnnouncementResponse

def announce_clbk(req):
    rospy.loginfo('Announce to Oracle: ')
    rospy.loginfo(req.who +' with the ' + req.what +' in the ' +req.where)
    return True


def main():
    #init node
    rospy.init_node('announce_service')
    #init service
    srv = rospy.Service('announce_service', Announcement, announce_clbk)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
      
        rate.sleep()


if __name__ == '__main__':
    main()
