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
    i = 0
    # Get the object pose from the first box
    if len(boxs) > 0:
        for box in boxs:
            print(boxs)
            x1, y1, x2, y2 = map(int, box[:4])
            img = color_image.copy()
            height, width = img.shape[:2]
            center_x, center_y = width // 2, height // 2  # Calculate center point of image

            center_x_new = x1 + (x2 - x1) // 2 - center_x
            center_y_new = center_y - y1 - (y2 - y1) // 2

            # Convert pixel coordinates to meters
            W = 48  # object width in centimeters
            H = 36  # object height in centimeters
            width = color_image.shape[1]  # image width in pixels
            height = color_image.shape[0]  # image height in pixels
            x_m = (center_x_new * (W / width))/100
            y_m = (center_y_new * (H / height))/100
            z_m = 0.45
            object_frame = "Yolo_Object "
            object_frame = object_frame + f"{i}"
            # Publish the transform
            tf_broadcaster.sendTransform((x_m, -y_m, z_m), tf.transformations.quaternion_from_euler(0, 0, 0), rospy.Time.now(), object_frame, "camera_color_optical_frame")
            i += 1

    #cv2.imshow('CR5_Realsense (yolov5_detect)', color_image)
    key = cv2.waitKey(1)

def dectshow(org_img, boxs):
    img = org_img.copy()
    height, width = img.shape[:2]
    center_x, center_y = width // 2, height // 2  # Calculate center point of image

    for box in boxs:
        x1, y1, x2, y2 = map(int, box[:4])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate coordinates of center point of box relative to the new origin
        center_x_new = x1 + (x2 - x1) // 2 - center_x
        center_y_new = center_y - y1 - (y2 - y1) // 2
        
        label = f"{box[-1]}"
        label = label + f"x: {center_x_new}, y: {center_y_new}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 2
        color = (255, 255, 255)

        # Show coordinates of center point relative to the new origin
        cv2.putText(img, label, (x1, y1+10), font, font_scale, color, thickness)

    cv2.imshow('CR5_Realsense (yolov5_detect)', img)

if __name__ == "__main__":

    # Subscribe to rostopic "image_raw"
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)

    rospy.spin()
