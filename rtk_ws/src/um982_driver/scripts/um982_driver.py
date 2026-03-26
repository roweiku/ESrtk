#!/usr/bin/env python3
import sys
import math

import rospy
# from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler, euler_from_quaternion


from UM982 import UM982Serial


class UM982DriverROS1:

    # def _ros_log_debug(self, log_data):
    #     self.get_logger().debug(str(log_data))

    # def _ros_log_info(self, log_data):
    #     self.get_logger().info(str(log_data))

    # def _ros_log_warn(self, log_data):
    #     self.get_logger().warn(str(log_data))

    # def _ros_log_error(self, log_data):
    #     self.get_logger().error(str(log_data))


    def __init__(self):
        rospy.init_node('um982_serial_driver', anonymous=True)
        # ROS1 参数获取
        port = rospy.get_param('~port', '/dev/ttyUSB0')
        baud = rospy.get_param('~baud', 921600)
        
        self._ros_log_debug = rospy.logdebug
        self._ros_log_info = rospy.loginfo
        self._ros_log_warn = rospy.logwarn
        self._ros_log_error = rospy.logerr

        # Step2：打开串口
        try:
            self.um982serial = UM982Serial(port, baud)
            self._ros_log_info(f'serial {port} open successfully!')
        except:
            self._ros_log_error(f'serial {port} do not open!')
            sys.exit(0)
        # Step3：新建一个线程用于处理串口数据
        self.um982serial.start()
        # Step4：ROS相关
        self.fix_pub = rospy.Publisher('/gps/fix', NavSatFix, queue_size=10)
        self.utm_pub = rospy.Publisher('/gps/utmpos', Odometry, queue_size=10)
        self.utmfix_pub = rospy.Publisher('/gps/utmfix', NavSatFix, queue_size=10)
        self.pub_rate = rospy.Rate(20)  # 20Hz

    def pub_task(self):
        bestpos_hgt, bestpos_lat, bestpos_lon, bestpos_hgtstd, bestpos_latstd, bestpos_lonstd = self.um982serial.fix
        utm_x, utm_y = self.um982serial.utmpos
        vel_east, vel_north, vel_ver, vel_east_std, vel_north_std, vel_ver_std = self.um982serial.vel
        heading, pitch, roll = self.um982serial.orientation
        this_time = rospy.Time.now()

        # Step 1: Publish GPS Fix Data
        fix_msg = NavSatFix()
        fix_msg.header.stamp = this_time
        fix_msg.header.frame_id = 'gps'
        fix_msg.latitude = bestpos_lat
        fix_msg.longitude = bestpos_lon
        fix_msg.altitude = bestpos_hgt
        fix_msg.position_covariance[0] = float(bestpos_latstd)**2
        fix_msg.position_covariance[4] = float(bestpos_lonstd)**2
        fix_msg.position_covariance[8] = float(bestpos_hgtstd)**2
        fix_msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN
        self.fix_pub.publish(fix_msg)

        # Step 2: Publish UTM Position Data
        odom_msg = Odometry()
        odom_msg.header.stamp = this_time
        odom_msg.header.frame_id = 'earth'
        odom_msg.child_frame_id  = 'base_link'
        odom_msg.pose.pose.position.x = utm_x
        odom_msg.pose.pose.position.y = utm_y
        odom_msg.pose.pose.position.z = bestpos_hgt
        quaternion = quaternion_from_euler(math.radians(roll), math.radians(pitch), math.radians(heading))
        odom_msg.pose.pose.orientation.x = quaternion[0]
        odom_msg.pose.pose.orientation.y = quaternion[1]
        odom_msg.pose.pose.orientation.z = quaternion[2]
        odom_msg.pose.pose.orientation.w = quaternion[3]
        odom_msg.pose.covariance         = [0.0] * 36
        odom_msg.pose.covariance[0]      = float(bestpos_latstd)**2
        odom_msg.pose.covariance[7]      = float(bestpos_lonstd)**2
        odom_msg.pose.covariance[14]     = float(bestpos_hgtstd)**2
        odom_msg.pose.covariance[21]     = 0.1
        odom_msg.pose.covariance[28]     = 0.1
        odom_msg.pose.covariance[35]     = 0.1
        odom_msg.twist.twist.linear.x    = vel_east
        odom_msg.twist.twist.linear.y    = vel_north
        odom_msg.twist.twist.linear.z    = vel_ver
        odom_msg.twist.covariance        = [0.0] * 36
        odom_msg.twist.covariance[0]     = float(vel_east_std)**2
        odom_msg.twist.covariance[7]     = float(vel_north_std)**2
        odom_msg.twist.covariance[14]    = float(vel_ver_std)**2
        self.utm_pub.publish(odom_msg)

        # Step 3: Publish UTM Fix Data
        utmfix_msg = NavSatFix()
        utmfix_msg.header.stamp = this_time
        utmfix_msg.header.frame_id = 'utm'
        utmfix_msg.latitude = 10
        utmfix_msg.longitude = 10
        utmfix_msg.altitude = bestpos_hgt
        utmfix_msg.position_covariance[0] = 0
        utmfix_msg.position_covariance[4] = 0
        utmfix_msg.position_covariance[8] = 0
        utmfix_msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN
        self.utmfix_pub.publish(utmfix_msg)

        # Test
        _, _, yaw = euler_from_quaternion(quaternion)
        print(heading)

    def run(self):
        # 替换运行方法
        # if rclpy.ok():
        #     rclpy.spin(self)
        while not rospy.is_shutdown():
            self.pub_task()
            self.pub_rate.sleep()
            
    def stop(self):
        self.um982serial.stop()



import time
import signal

# 替换信号处理和主程序
def signal_handler(sig, frame):
    um982_driver.stop()
    # 不需要rclpy.shutdown()
    rospy.signal_shutdown("Ctrl+C pressed")
    sys.exit(0)

if __name__ == "__main__":
    # 不需要rclpy.init()
    um982_driver = UM982DriverROS1()
    rospy.on_shutdown(um982_driver.stop)  # 注册关闭回调
    signal.signal(signal.SIGINT, signal_handler)
    um982_driver.run()