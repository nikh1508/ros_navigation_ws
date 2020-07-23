#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from get_pose.srv import GetPose, GetPoseResponse

amcl_pose = None

def amcl_pose_cb(msg):
    global amcl_pose
    amcl_pose = msg.pose.pose

def service_cb(req):
    response = GetPoseResponse()
    if amcl_pose is not None:
        response.pose = amcl_pose
        response.success = True

    else:
        response.success = False
    return response

rospy.init_node('get_pose_service')
sub_amcl_pose = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, amcl_pose_cb)
my_service = rospy.Service('/get_pose', GetPose , service_cb) # create the Service called my_service with the defined callback
rospy.loginfo('/get_pose service started...')
rospy.spin()