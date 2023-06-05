# <center>Bin-Picking Project</center>

### Abstract
Robotic arms have gained popularity in various industries due to their accuracy and efficiency in completing tasks. In this study, we propose a method for automating bin-picking tasks using the Dobot CR5 robotic arm, combining the state-of-the-art YOLOv5 CNN model for object detection with traditional feature detector, descriptor, and matching techniques. Specifically, we employ the FAST and BRISK algorithms for robust and efficient feature detector, descriptor, and matching. By integrating these techniques and utilizing a depth sensor camera to capture depth and color images, our system achieves real-time object detection and precise pose estimation, enabling the robotic arm to accurately pick objects. This integration of small-scale camera technology with advanced algorithms contributes to the advancement of industrial robotics, opening up new possibilities for automating challenging tasks and enhancing overall operational efficiency.

#### Keywords: 
*robotic arm, bin-picking, YOLOv5 CNN model, depth sensor camera, object detection and pose estimation*



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
```
### Installing Realsense-ROS

You need to install realsense-ros to using realsense2_camera package. The step to installing realsense-ros have shown [here](https://github.com/monkeyrom/realsense-ros).

### building
```sh
cd $HOME/catkin_ws/src/Bin-Picking
catkin build
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

* this command will run node
  - yolo_listener
  
## 4.  Run a terminal for controlling robot

```sh
    rosrun CR5_Project service_call
```

* this command will run 2 nodes and spawn new terminal for commanding
  - listener
  - main_order

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
