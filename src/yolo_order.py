import rospy
import numpy as np
import cv2
import torch
import tf
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

bridge = CvBridge()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/rom/catkin_ws/src/CR5_Project/weights/best.pt')
model.conf = 0.6

#model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/rom/catkin_ws/src/CR5_Project/weights/best.pt')
#model.conf = 0.7

# Initialize the tf broadcaster
tf_broadcaster = tf.TransformBroadcaster()

def image_callback(msg):
    global start_detect

    #color_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    #cv2.imshow('depth_image', color_image)
    #key = cv2.waitKey(1)

    if start_detect == 1 :
        print("run detect loop")
        start_detect = 0

        # Convert ROS message to OpenCV image
        color_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        # Run object detection on color_image
        results = model(color_image)
        boxs = results.pandas().xyxy[0].values
        dectshow(color_image, boxs)
        i = 0
        z_compare = 1.0
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

                obj_center_old_x = x1 + (x2 - x1) // 2
                obj_center_old_y = y1 + (y2 - y1) // 2
                obj_center_old = [obj_center_old_x, obj_center_old_y]
                obj_depth = get_mid_pos(obj_center_old)

                # Convert pixel coordinates to meters
                W = 48  # object width in centimeters
                H = 36  # object height in centimeters
                width = color_image.shape[1]  # image width in pixels
                height = color_image.shape[0]  # image height in pixels
                x_m = (center_x_new * (W / width))/100
                y_m = (center_y_new * (H / height))/100
                z_m = obj_depth/1000

                
                object_frame = "Yolo_Object "
                object_frame = object_frame + f"{i}"
                object_frame = "obj_arduino"
                # Publish the transform
                if z_compare > z_m :
                    z_compare = z_m
                    tf_broadcaster.sendTransform((x_m, -y_m, z_m), tf.transformations.quaternion_from_euler(0, 0, 0), rospy.Time.now(), object_frame, "camera_color_optical_frame")
                i += 1
    else :
        pass


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

        obj_center_old_x = x1 + (x2 - x1) // 2
        obj_center_old_y = y1 + (y2 - y1) // 2
        obj_center_old = [obj_center_old_x, obj_center_old_y]
        obj_depth = get_mid_pos(obj_center_old)

        label = f"{box[-1]}"
        label = label + f" x: {center_x_new}, y: {center_y_new}, z: {obj_depth}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        color = (255, 255, 255)
        
        # Show coordinates of center point relative to the new origin
        cv2.putText(img, label, (x1+2, y1-7), font, font_scale, color, thickness)

    ros_image = bridge.cv2_to_imgmsg(img, encoding="rgb8")  # Convert OpenCV image to ROS Image message
    pub_img.publish(ros_image)  # Publish ROS Image message to topic
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2.imshow('CR5_Realsense (yolov5_detect)', img)

def get_mid_pos(center):
    global depth_global
    print(center)
    depth_data = depth_global
    width = 410
    heigh = 300
    percent_w = width/640
    percent_h = heigh/480
    radius = 5

    #print(percent_w,percent_w)

    X = center[0] * percent_w
    Y = center[1] * percent_h

    distance_list = []

    dist = depth_data[int(Y), int(X)]
    print(int(X),int(Y))
    
    for i in range(int(Y)-radius, int(Y)+radius+1):
        for j in range(int(X)-radius, int(X)+radius+1):
            dist = depth_data[i, j]
            if dist:
                distance_list.append(dist)

    distance_list = np.array(distance_list)
    mean_dist = np.mean(distance_list)
 
    return int(mean_dist)

def depth_callback(msg):
    global depth_global
    depth_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    # Define crop parameters
    crop_left = 100
    crop_right = 130
    crop_top = 90
    crop_bottom = 90

    # Crop depth image
    depth_cropped = depth_image[crop_top:-crop_bottom, crop_left:-crop_right]
    #depth_cropped = depth_image

    depth_global = depth_cropped
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_cropped, alpha=0.30), cv2.COLORMAP_JET)

    depth_colormap = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2RGB)
    ros_image = bridge.cv2_to_imgmsg(depth_colormap, encoding="rgb8")  # Convert OpenCV image to ROS Image message
    pub_depth_img.publish(ros_image)  # Publish ROS Image message to topic
    #cv2.imshow('depth_image', depth_colormap)
    #key = cv2.waitKey(1)

def detect_order(msg):
    global start_detect
    start_detect = 1

    rospy.loginfo("I heard %s", msg.data)
    
if __name__ == "__main__":

    global start_detect
    start_detect = 0
    print("Ready to detect")
    rospy.init_node('yolo_listener', anonymous=True)
    # Publish to rostopic
    pub_img = rospy.Publisher("/main/yolo_detect_image", Image, queue_size=10)
    pub_depth_img = rospy.Publisher("/main/color_depth_image", Image, queue_size=10)

    # Subscribe to rostopic
    rospy.Subscriber("/main/yolo_order", String, detect_order)
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)
    rospy.Subscriber("/camera/depth/image_rect_raw", Image, depth_callback)
    
    rospy.spin()