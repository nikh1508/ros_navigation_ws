#! /usr/bin/env python

import rospy
import rospkg
import os
import sys
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
from record_spots.srv import RSSericeMessage, RSSericeMessageResponse

class RecordSpots():
    def __init__(self, file_name):
        self._sub_pose = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.pose_cb)
        self._amcl_pose = Pose()
        self._rs_service = rospy.Service('/record_spot', RSSericeMessage, self.service_cb)
        self._out_file = file_name
        rospy.loginfo('Output File: ' + self._out_file)
        self._pkg_path = rospkg.RosPack().get_path('record_spots')
        if 'saved_spots' not in os.listdir(self._pkg_path):
            os.makedirs(os.path.join(self._pkg_path, 'saved_spots'))
    
    def pose_cb(self, msg):
        self._amcl_pose = msg.pose.pose
    
    def service_cb(self, req):
        res = RSSericeMessageResponse()
        try:
            with open(os.path.join(self._pkg_path, 'saved_spots', self._out_file), 'a+') as f:
                f.write('\n'+ str(req.label) + ":")

                f.write('\n    position:')
                f.write('\n        x: ' + str(self._amcl_pose.position.x))
                f.write('\n        y: ' + str(self._amcl_pose.position.y))
                f.write('\n        z: ' + str(self._amcl_pose.position.z))
                
                f.write('\n    orientation:')
                f.write('\n        x: ' + str(self._amcl_pose.orientation.x))
                f.write('\n        y: ' + str(self._amcl_pose.orientation.y))
                f.write('\n        z: ' + str(self._amcl_pose.orientation.z))
                f.write('\n')
            res.success = True
            res.message = 'Label: ' + str(req.label) + ' saved.'

        except Exception as e:
            res.success = False
            res.message = 'Error Occured : ' + str(e.message)
        return res
            
if __name__ == '__main__':
    rospy.init_node('rs_service_server')
    if not sys.argv[1].endswith('.yaml'):
        rospy.logerr('Output file name not provided or incorrect usage')
        rospy.signal_shutdown('Incorrect usage')
    record_spots = RecordSpots(sys.argv[1])
    rospy.spin()