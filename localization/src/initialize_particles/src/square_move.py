#! /usr/bin/env python

import rospy
import time
from std_srvs.srv import Empty, EmptyRequest
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped

class HuskyController():

    def __init__(self):
        self._pub_vel = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
        self._sub_amcl_pose = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_pose_cb)
        self._pose = PoseWithCovarianceStamped()
        self._twist = Twist()
        self._rate = rospy.Rate(10)
        rospy.loginfo('Waiting for service /global_localization')
        rospy.wait_for_service('/global_localization')
        self._disperse_particles_service = rospy.ServiceProxy('/global_localization', Empty)
        rospy.loginfo('Robot initialized')

    def disperse_particles(self):
        empty_req = EmptyRequest()
        self._disperse_particles_service(empty_req)
     
    def amcl_pose_cb(self, msg):
        self._pose = msg
    
    def move(self, linear, angular):
        self._twist.linear.x = linear
        self._twist.angular.z = angular
        self._pub_vel.publish(self._twist)
    
    def move_forward(self, _time, speed=1.0):
        self._twist.linear.x = speed
        self._twist.angular.z = 0.0
        _t = time.time()
        while time.time() - _t < _time:
            self._pub_vel.publish(self._twist)
            self._rate.sleep()

    def stop(self):
        self.move(0, 0)
    
    def rotate90(self):
        self._twist.angular.z = 0.8
        self._twist.linear.x = 0.0
        _t = time.time()
        while time.time() - _t < 3.:
            self._pub_vel.publish(self._twist)
            self._rate.sleep()
        self.stop()
    
    def move_square(self):
        for i in range(4):
            self.move_forward(5, 0.5)
            rospy.sleep(.8)
            self.rotate90()
        self.stop()

    def get_particles_covariance(self):
        cov_x = self._pose.pose.covariance[0]
        cov_y = self._pose.pose.covariance[7]
        cov_z = self._pose.pose.covariance[35]
        rospy.loginfo("## Cov X: " + str(cov_x) + " ## Cov Y: " + str(cov_y) + " ## Cov Z: " + str(cov_z))
        covariance = (cov_x+cov_y+cov_z)/3
        return covariance
    
if __name__ == '__main__':
    rospy.init_node('husky_localize')
    husky = HuskyController()
    rospy.loginfo('Dispersing the particles throughout the map')
    husky.disperse_particles()
    time.sleep(3)
    rospy.loginfo('Initial Covariance:: ' + str(husky.get_particles_covariance()))
    husky.move_square()
    # If this covariance is less than 0.65, this means that the robot has localized itself correctly.
    rospy.loginfo('Final Covariance:: ' + str(husky.get_particles_covariance()))