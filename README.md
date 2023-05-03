# <center>Bin-Picking Project</center>

### Abstract
Robotic arms have gained popularity in various industries due to their accuracy and efficiency in completing tasks. In this study, we propose a novel method for automatic bin-picking using the Dobot CR5 robotic arm, combining the state-of-the-art YOLOv5 CNN model for object detection and the FAST and BRISK feature detection and matching methods for object pose estimation. The system utilizes the Intel RealSense D435i camera to capture depth and colour images, which are used as input data for object detection and pose estimation. The YOLOv5 CNN model enables real-time object detection, while the FAST and BRISK methods estimate the pose of the object, allowing the robotic arm to pick the object at the correct position and orientation. The proposed method demonstrates promising results and shows the potential for revolutionizing the field of robotics, particularly in the context of industrial automation, by improving efficiency and accuracy in object manipulation tasks.

Keywords: *robotic arm, bin-picking, object detection, object pose estimation, CNN*


## Requirement

- ubuntu 20.04
- ROS noetic

# Building

### Use git to clone the source code
```sh
cd $HOME/catkin_ws/src
git clone https://github.com/Dobot-Arm/CR_ROS.git
git clone https://github.com/introlab/find-object.git
git clone https://github.com/monkeyrom/CR5_Project.git
cd $HOME/catkin_ws
```
### Installing Realsense-ROS

You need to install realsense-ros to using realsense2_camera package. The step to installing realsense-ros have shown [here](https://github.com/monkeyrom/realsense-ros).

### building
```sh
catkin_make
```
### set the dobot type
```sh
echo "export DOBOT_TYPE=cr5" >> ~/.bashrc
source ~/.bashrc
source $HOME/catkin_ws/devel/setup.bash
```

## 1.  Launch Project

* Connect the robotic arm with following command, and default robot_ip is 192.168.1.6 

```sh
    roslaunch CR5_Project CR5_with_realsense.launch
```

* this command will launch 
  - dobot_bringup
  - realsense camera pointcloud
  - find object 2d
  - tf synchronisation

### rviz display

![rviz display](./pic/rviz.png)

### find object GUI

## 2.  Add object image for detection

* Using find object gui for adding image
  - > edit
  - > add object from scene
  - > take picture
  - > crop object

### tf synchronize

## 3.  Run a terminal for running yolo node

```sh
    rosrun CR5_Project yolo_order.py
```

## 4.  Run a terminal for controlling robot

```sh
    rosrun CR5_Project service_call
```

* this command will run 2 nodes and spawn new terminal for commanding
  - service_call
  - node_order

### new terminal for input command

## Real Robotic Arm

### Dobot CR5 

### Intel Realsense D435i
![Intel Realsense D435i](./pic/dobot2.jpg)

# References
- **CR_ROS**: https://github.com/Dobot-Arm/CR_ROS
- **Intel Realsense**: https://github.com/IntelRealSense/librealsense
- **find-object**: https://github.com/introlab/find-object
- **YOLOv5** : https://github.com/ultralytics/yolov5
