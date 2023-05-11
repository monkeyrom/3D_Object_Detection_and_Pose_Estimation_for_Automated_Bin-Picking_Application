import rospy
import tf
import math
from time import sleep
import tf.transformations as tr

rospy.init_node('main_order', anonymous=True)
listener = tf.TransformListener()

while True:
    source_frameid = 'base_link'
    target_frameid = 'object_6'

    listener.waitForTransform(target_frameid, source_frameid, rospy.Time(), rospy.Duration(0.5))
    if listener.canTransform(target_frameid, source_frameid, rospy.Time()):
        (trans, rot) = listener.lookupTransform(source_frameid, target_frameid, rospy.Time())

        # convert the rotation vector to a rotation matrix
        rot_matrix = tr.quaternion_matrix(rot)

        # extract the roll-pitch-yaw angles from the rotation matrix
        rpy_angles = tr.euler_from_matrix(rot_matrix, 'rxyz')

        # rpy_angles is a tuple containing the roll, pitch, and yaw angles in radians
        roll, pitch, yaw = rpy_angles

        x = round(trans[0] * 1000)
        y = round(trans[1] * 1000)
        z = round(trans[2] * 1000)
        rx = round(roll )
        ry = round(pitch + 180)
        rz = round(yaw )
        z_off = z + 54 if z + 54 >= 15 else 15

        rx = rx + 180
        ry = ry - 180
        rz = rz + 180

        x = x
        y = y
        z = z_off + 30

        print(x," ",y," ",z," ",rx," ",ry," ",rz)

    sleep(1)
