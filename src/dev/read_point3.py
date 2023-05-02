#!/usr/bin/env python
import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
import struct

def listen():
    rospy.init_node('listen', anonymous=True)
    rospy.Subscriber('/camera/depth/color/points', PointCloud2, callback_kinect, queue_size=10000)

def callback_kinect(data):
    # set the pixel coordinates
    x, y = 100, 100
    
    # read the point cloud data at the pixel coordinates (x, y)
    gen = pc2.read_points(data, skip_nans=True, field_names=("x", "y", "z"), uvs=[(x, y)])
    try:
        # extract the z coordinate of the first point
        z = next(gen)[2]
        rospy.loginfo("Depth at pixel (x={}, y={}): {:.2f}m".format(x, y, z))
    except (StopIteration, ValueError, struct.error) as e:
        rospy.loginfo("No point at pixel (x={}, y={}). Error: {}".format(x, y, str(e)))

if __name__ == '__main__':
    try:
        listen()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
