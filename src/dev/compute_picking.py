import numpy as np

def compute_vector():
    # Define the position and orientation of the object
    object_pos = np.array([143, -580, -30])  # Object position in world frame
    object_ori = np.array([0, 0, 20])  # Object orientation in world frame (euler angles)

    # Convert the object orientation from euler angles to a rotation matrix
    Rx = np.array([[1, 0, 0],
                [0, np.cos(object_ori[0]), -np.sin(object_ori[0])],
                [0, np.sin(object_ori[0]), np.cos(object_ori[0])]])
    Ry = np.array([[np.cos(object_ori[1]), 0, np.sin(object_ori[1])],
                [0, 1, 0],
                [-np.sin(object_ori[1]), 0, np.cos(object_ori[1])]])
    Rz = np.array([[np.cos(object_ori[2]), -np.sin(object_ori[2]), 0],
                [np.sin(object_ori[2]), np.cos(object_ori[2]), 0],
                [0, 0, 1]])
    object_rot = Rz.dot(Ry.dot(Rx))

    # Define the desired position of the robot relative to the object frame
    p_o_desired = np.array([0, 0, 30])  # 30mm above the object in the object frame

    # Transform the position vector from the object frame to the world frame
    p_w_desired = object_rot.dot(p_o_desired) + object_pos

    print(p_w_desired)
