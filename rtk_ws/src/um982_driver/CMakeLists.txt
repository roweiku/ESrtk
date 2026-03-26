cmake_minimum_required(VERSION 3.0.2)
project(um982_driver)

find_package(catkin REQUIRED COMPONENTS
  rospy
  tf
  sensor_msgs
  nav_msgs
)

catkin_package()

# 安装 Python 脚本
install(PROGRAMS
  scripts/um982_driver.py
  scripts/UM982.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)