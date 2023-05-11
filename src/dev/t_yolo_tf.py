import rospy
import numpy as np
import cv2
import torch
import tf
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

rospy.init_node('yolov5_detect')
bridge = CvBridge()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/rom/catkin_ws/src/CR5_Project/weights/best5.pt')
model.conf = 0.5

# Initialize the tf broadcaster
tf_broadcaster = tf.TransformBroadcaster()

def image_callback(msg):
    # Convert ROS message to OpenCV image
    color_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

    # Run object detection on color_image
    results = model(color_image)
    boxs = results.pandas().xyxy[0].values
    dectshow(color_image, boxs)

    # Get the object pose from the first box
    if len(boxs) > 0:
        x1, y1, x2, y2 = map(int, boxs[0][:4])
        center_x = x1 + (x2 - x1) // 2
        center_y = y1 + (y2 - y1) // 2

        # Calculate the object's position relative to the image center
        height, width = color_image.shape[:2]
        center_x_new = center_x - width // 2
        center_y_new = height // 2 - center_y

        # Create a translation matrix for the object's position
        trans_matrix = tf.transformations.translation_matrix((center_x_new, center_y_new, 0))

        # Create a rotation matrix for the object's orientation
        rot_matrix = tf.transformations.quaternion_matrix(tf.transformations.quaternion_from_euler(0, 0, 0))

        # Calculate the transform matrix for the object's pose
        obj_matrix = np.dot(trans_matrix, rot_matrix)

        # Publish the transform
        tf_broadcaster.sendTransform((center_x_new, center_y_new, 0), tf.transformations.quaternion_from_euler(0, 0, 0), rospy.Time.now(), "object_frame", "camera_color_optical_frame")

    #cv2.imshow('CR5_Realsense (yolov5_detect)', color_image)
    key = cv2.waitKey(1)

def dectshow(org_img, boxs):
    img = org_img.copy()

    for box in boxs:
        x1, y1, x2, y2 = map(int, box[:4])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        label = f"{box[-1]}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        color = (255, 255, 255)
        cv2.putText(img, label, (x1, y1), font, font_scale, color, thickness)

    cv2.imshow('CR5_Realsense (yolov5_detect)', img)

if __name__ == "__main__":

    # Subscribe to rostopic "image_raw"
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)

    rospy.spin()
