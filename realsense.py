import pyrealsense2 as rs2
import matplotlib.pyplot as plt
import numpy as np
import cv2

pipe = rs2.pipeline()
config = rs2.config()
config.enable_stream(rs2.stream.color,640,360,rs2.format.bgr8,30)
config.enable_stream(rs2.stream.depth,640,360,rs2.format.z16,30)

pipe.start(config)

try:
    
    while True:
        frames = pipe.wait_for_frames()
        depth = frames.get_depth_frame()
        color = frames.get_color_frame()
        if depth is None or color is None:
            continue
        #print(depth.get_distance(100,200))
        depth_image = np.asarray(depth.get_data())
        color_image = np.asarray(color.get_data())
        #gray_img = cv2.cvtColor(color_image,cv2.COLOR_BGR2GRAY)
        depth_color = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=0.03),cv2.COLORMAP_JET)

        cv2.namedWindow("Demo",cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Demo",depth_color)

        cv2.namedWindow("color_image",cv2.WINDOW_AUTOSIZE)
        cv2.imshow("color_image",color_image)
        
        cv2.waitKey(1)        
    
    exit(0)
    
except Exception as e:
    print(e)
    pass

finally:
    pipe.stop()
    cv2.destroyAllWindows()
