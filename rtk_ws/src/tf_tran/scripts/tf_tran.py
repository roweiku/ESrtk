#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
import tf2_ros
# 2D
import math
import tf_conversions  # 需要安装tf-conversions包
# 2D

class UtmTfBroadcaster:
    def __init__(self):
        rospy.init_node('utm_tf_broadcaster')
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        rospy.Subscriber("/gps/utmpos", Odometry, self.odom_callback)

    def odom_callback(self, msg):
        transform = TransformStamped()
        transform.header.stamp = rospy.Time.now()  # 使用当前时间
        transform.header.frame_id = "earth"        # 父坐标系
        transform.child_frame_id = "base_link"     # 子坐标系
        
        # 2D
        # 复制位置数据
        transform.transform.translation.x = msg.pose.pose.position.x
        transform.transform.translation.y = msg.pose.pose.position.y
        transform.transform.translation.z = 20
        
        # 将3D四元数转换为仅保留2D旋转（绕Z轴的yaw）
        orientation = msg.pose.pose.orientation
        # 提取欧拉角
        roll, pitch, yaw = tf_conversions.transformations.euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w])
        
        # 重新创建仅包含yaw的四元数（将roll和pitch归零）
        quat = tf_conversions.transformations.quaternion_from_euler(0, 0, yaw)
        transform.transform.rotation.x = quat[0]
        transform.transform.rotation.y = quat[1]
        transform.transform.rotation.z = quat[2]
        transform.transform.rotation.w = quat[3]
        # 2D
        
        # 3D
        # 复制姿态数据
        # transform.transform.rotation = msg.pose.pose.orientation
        # 3D
        
        self.tf_broadcaster.sendTransform(transform)

if __name__ == '__main__':
    UtmTfBroadcaster()
    rospy.spin()