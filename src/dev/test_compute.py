import rospy
import numpy as np
import tf
import math
from tf.transformations import euler_from_quaternion

def compute_vector_50(x,y,z,ry,rx,rz):
    # Convert the orientation from degrees to radians
    rx = math.radians(rx)
    ry = math.radians(ry)
    rz = math.radians(rz)

    # Define the position and orientation of the object
    object_pos = np.array([x, y, z])  # Object position in world frame
    object_ori = np.array([ry, rx, rz])  # Object orientation in world frame (euler angles)

    # Convert the object orientation from euler angles to a rotation matrix
    Rx = np.array([[1, 0, 0],
                [0, np.cos(object_ori[1]), -np.sin(object_ori[1])],
                [0, np.sin(object_ori[1]), np.cos(object_ori[1])]])
    Ry = np.array([[np.cos(object_ori[0]), 0, np.sin(object_ori[0])],
                [0, 1, 0],
                [-np.sin(object_ori[0]), 0, np.cos(object_ori[0])]])
    Rz = np.array([[np.cos(object_ori[2]), -np.sin(object_ori[2]), 0],
                [np.sin(object_ori[2]), np.cos(object_ori[2]), 0],
                [0, 0, 1]])
    object_rot = Rz.dot(Ry.dot(Rx))

    # Define the desired position of the robot relative to the object frame
    p_o_desired = np.array([0, 0, -50])  # 100mm above the object in the object frame

    # Transform the position vector from the object frame to the world frame
    p_w_desired = object_rot.dot(p_o_desired) + object_pos

    #print(p_w_desired)
    return (p_w_desired[0],p_w_desired[1],p_w_desired[2])

def compute_vector_100(x,y,z,ry,rx,rz):
    # Convert the orientation from degrees to radians
    rx = math.radians(rx)
    ry = math.radians(ry)
    rz = math.radians(rz)

    # Define the position and orientation of the object
    object_pos = np.array([x, y, z])  # Object position in world frame
    object_ori = np.array([ry, rx, rz])  # Object orientation in world frame (euler angles)

    # Convert the object orientation from euler angles to a rotation matrix
    Rx = np.array([[1, 0, 0],
                [0, np.cos(object_ori[1]), -np.sin(object_ori[1])],
                [0, np.sin(object_ori[1]), np.cos(object_ori[1])]])
    Ry = np.array([[np.cos(object_ori[0]), 0, np.sin(object_ori[0])],
                [0, 1, 0],
                [-np.sin(object_ori[0]), 0, np.cos(object_ori[0])]])
    Rz = np.array([[np.cos(object_ori[2]), -np.sin(object_ori[2]), 0],
                [np.sin(object_ori[2]), np.cos(object_ori[2]), 0],
                [0, 0, 1]])
    object_rot = Rz.dot(Ry.dot(Rx))

    # Define the desired position of the robot relative to the object frame
    p_o_desired = np.array([0, 0, -100])  # 100mm above the object in the object frame

    # Transform the position vector from the object frame to the world frame
    p_w_desired = object_rot.dot(p_o_desired) + object_pos

    #print(p_w_desired)
    return (p_w_desired[0],p_w_desired[1],p_w_desired[2])

def compute_vector_150(x,y,z,ry,rx,rz):
    # Convert the orientation from degrees to radians
    rx = math.radians(rx)
    ry = math.radians(ry)
    rz = math.radians(rz)

    # Define the position and orientation of the object
    object_pos = np.array([x, y, z])  # Object position in world frame
    object_ori = np.array([ry, rx, rz])  # Object orientation in world frame (euler angles)

    # Convert the object orientation from euler angles to a rotation matrix
    Rx = np.array([[1, 0, 0],
                [0, np.cos(object_ori[1]), -np.sin(object_ori[1])],
                [0, np.sin(object_ori[1]), np.cos(object_ori[1])]])
    Ry = np.array([[np.cos(object_ori[0]), 0, np.sin(object_ori[0])],
                [0, 1, 0],
                [-np.sin(object_ori[0]), 0, np.cos(object_ori[0])]])
    Rz = np.array([[np.cos(object_ori[2]), -np.sin(object_ori[2]), 0],
                [np.sin(object_ori[2]), np.cos(object_ori[2]), 0],
                [0, 0, 1]])
    object_rot = Rz.dot(Ry.dot(Rx))

    # Define the desired position of the robot relative to the object frame
    p_o_desired = np.array([0, 0, -150])  # 100mm above the object in the object frame

    # Transform the position vector from the object frame to the world frame
    p_w_desired = object_rot.dot(p_o_desired) + object_pos

    #print(p_w_desired)
    return (p_w_desired[0],p_w_desired[1],p_w_desired[2])

if __name__ == "__main__":
    source_frameid = 'base_link'
    camera_frameid = 'camera_link'
    target_frameid1 = 'object_6'
    rospy.init_node('main_order', anonymous=True)
    listener = tf.TransformListener()
    listener.waitForTransform(target_frameid1, source_frameid, rospy.Time(), rospy.Duration(1))

    print("found 1 object")

    echo_transform = listener.lookupTransform(source_frameid, target_frameid1, rospy.Time(0))
    echo_cam = listener.lookupTransform(target_frameid1, camera_frameid, rospy.Time(0))
    yaw, pitch, roll = euler_from_quaternion(echo_cam[1])
    v = echo_transform[0]

    x = int(v[0] * 1000)
    y = int(v[1] * 1000)
    z = int(v[2] * 1000)
    rx = int(roll * 180.0 / math.pi)
    ry = int(pitch * 180.0 / math.pi)
    rz = int(yaw * 180.0 / math.pi)

    x_cal = x
    y_cal = y
    z_cal = z
    rx_cal = ry
    ry_cal = rx
    rz_cal = rz

    rx_robo = rx_cal + 180
    ry_robo = -(ry_cal - 180)
    rz_robo = rz_cal + 180

    print("Object : ",x_cal,y_cal,z_cal,rx,ry,rz)
    robo_compute1 = compute_vector_50(x_cal,y_cal,z_cal,rx,ry,rz)
    robo_compute2 = compute_vector_100(x_cal,y_cal,z_cal,rx,ry,rz)
    robo_compute3 = compute_vector_150(x_cal,y_cal,z_cal,rx,ry,rz)

    '''if robo_compute[2] >= 33 :
        robo_compute[2] = robo_compute[2]
    if robo_compute[2] < 33 :
        robo_compute[2] = 33'''

    print("Robot : ",round(robo_compute1[0]),round(robo_compute1[1]),round(robo_compute1[2]),rx_robo,ry_robo,rz_robo)
    print("Robot : ",round(robo_compute2[0]),round(robo_compute2[1]),round(robo_compute2[2]),rx_robo,ry_robo,rz_robo)
    print("Robot : ",round(robo_compute3[0]),round(robo_compute3[1]),round(robo_compute3[2]),rx_robo,ry_robo,rz_robo)