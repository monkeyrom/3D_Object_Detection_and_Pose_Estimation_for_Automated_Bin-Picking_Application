import rospy
import numpy as np
import cv2
import torch
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

rospy.init_node('yolov5_detect')
bridge = CvBridge()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/rom/catkin_ws/src/CR5_Project/weights/best5.pt')
model.conf = 0.5

def image_callback(msg):
    # Convert ROS message to OpenCV image
    color_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

    # Run object detection on color_image
    results = model(color_image)
    boxs = results.pandas().xyxy[0].values
    dectshow(color_image, boxs)

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
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        color = (255, 255, 255)
        cv2.putText(img, label, (x1, y1), font, font_scale, color, thickness)

        # Show coordinates of center point relative to the new origin
        cv2.putText(img, f"x: {center_x_new}, y: {center_y_new}", (x1, y1 + 30), font, 0.5, color, thickness)

    cv2.imshow('CR5_Realsense (yolov5_detect)', img)



if __name__ == "__main__":

    # Subscribe to rostopic "image_raw"
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)
    
    rospy.spin()
