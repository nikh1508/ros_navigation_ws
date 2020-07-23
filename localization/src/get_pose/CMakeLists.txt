cmake_minimum_required(VERSION 3.0.2)
project(get_pose)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  message_generation
)

add_service_files(
  FILES
  GetPose.srv
)

generate_messages(
  DEPENDENCIES
  geometry_msgs  # Or other packages containing msgs
)

catkin_package(
 CATKIN_DEPENDS rospy
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

