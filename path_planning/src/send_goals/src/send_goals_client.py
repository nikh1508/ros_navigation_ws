import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction ,MoveBaseGoal, MoveBaseResult
import sys

rospy.init_node('move_base_client')
client =  actionlib.SimpleActionClient('/move_base', MoveBaseAction)
client.wait_for_server()

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

def feedback_cb(feedback):
    return

poses = (
    ((-1.2965593338,-2.19947767258, 0.0), (0.0, 0.0, 0.665694641257, 0.74622425892)),
    ((-1.2413444519, 1.72821462154, 0.0), (0.0, 0.0, -0.212821245626, 0.977091151024)),
    ((1.64730453491, -0.255764424801, 0.0), (0.0, 0.0, 0.931686294118, -0.36326388391))
)

def send_goal(pose):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = pose[0][0]
    goal.target_pose.pose.position.y = pose[0][1]
    goal.target_pose.pose.position.z = pose[0][2]
    goal.target_pose.pose.orientation.x = pose[1][0]
    goal.target_pose.pose.orientation.y = pose[1][1]
    goal.target_pose.pose.orientation.z = pose[1][2]
    goal.target_pose.pose.orientation.w = pose[1][3]
    client.send_goal(goal, feedback_cb=feedback_cb)

nos_poses = len(poses)
rate = rospy.Rate(5)

i = 0
while True:
    try:
        rospy.loginfo('Sending a new Goal')
        send_goal(poses[i%nos_poses])
        rospy.loginfo('Waiting to reach the goal...')
        client.wait_for_result(rospy.Duration(100))
        rospy.loginfo('Goal Reached')
        rospy.sleep(.5)
        i += 1
    except:
        client.cancel_all_goals()
        rospy.loginfo('Exiting now.')
        sys.exit(0)
