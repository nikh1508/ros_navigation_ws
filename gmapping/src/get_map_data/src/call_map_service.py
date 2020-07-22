#! /usr/bin/env python

import rospy
from nav_msgs.srv import GetMap, GetMapRequest

rospy.init_node('get_map_data')

rospy.loginfo('Waiting for /static_map service')
rospy.wait_for_service('/static_map')
rospy.loginfo('Static Map service found')

get_static_map = rospy.ServiceProxy('/static_map', GetMap)
req_msg = GetMapRequest()

result = get_static_map(req_msg)
print '\nMap Info:'
print 'Dimension[W x H]:', result.map.info.width, 'x', result.map.info.height
print 'Resolution:', result.map.info.resolution