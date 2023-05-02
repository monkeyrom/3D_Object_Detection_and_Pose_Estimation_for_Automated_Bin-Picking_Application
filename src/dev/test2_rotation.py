import rospy
import tf
import math
from time import sleep
from tf.transformations import euler_from_quaternion

rospy.init_node('main_order', anonymous=True)
echoListener = tf.TransformListener()

source_frameid = 'base_link'
camera_frameid = 'camera_link'
target_frameid = 'object_6'

echoListener.waitForTransform(target_frameid, source_frameid, rospy.Time(), rospy.Duration(0.5))
echoListener.waitForTransform(camera_frameid, source_frameid, rospy.Time(), rospy.Duration(0.5))

echo_transform = echoListener.lookupTransform(source_frameid, target_frameid, rospy.Time(0))
echo_cam = echoListener.lookupTransform(target_frameid, camera_frameid, rospy.Time(0))

yaw, pitch, roll = euler_from_quaternion(echo_cam[1])
v = echo_transform[0]

goal_x = int(v[0] * 1000)
goal_y = int(v[1] * 1000)
goal_z = int(v[2] * 1000)
goal_roll = int(roll * 180.0 / math.pi)
goal_pitch = int(pitch * 180.0 / math.pi)
goal_yall = int(yaw * 180.0 / math.pi)

goal_x_cal = goal_x
goal_y_cal = goal_y
goal_z_cal = goal_z + 54
goal_rx_cal = goal_pitch + 180
goal_ry_cal = -(goal_roll - 180)
goal_rz_cal = goal_yall + 180

print(goal_x_cal," ",goal_y_cal," ",goal_z_cal," ",goal_rx_cal," ",goal_ry_cal," ",goal_rz_cal)

