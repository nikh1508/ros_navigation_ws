#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyRequest

rospy.init_node('init_particles')
rospy.loginfo('Waiting for service /global_localization')
rospy.wait_for_service('/global_localization')
init_particles = rospy.ServiceProxy('/global_localization', Empty)
rospy.loginfo('Service found')

empty_req = EmptyRequest()
init_particles(empty_req)