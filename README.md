# <center>CR5_Project</center>

Dobot CR5 with Intel Realsense D435i for object detection and pose estimation (bin-picking application).

This project is present the robot arm application especially bin-picking base on Dobot CR5 using ROS which detect an object and 6d pose estimation with intel realsense d435i depth camera by detection [find-object](https://introlab.github.io/find-object/) app.

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

[here](https://github.com/monkeyrom/realsense-ros)
  
- #### Option 1: Install librealsense2 debian package from Intel servers

  - Jetson users - use the [Jetson Installation Guide](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md)
  - Otherwise, install from [Linux Debian Installation Guide](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md#installing-the-packages)
    - In this case treat yourself as a developer: make sure to follow the instructions to also install librealsense2-dev and librealsense2-dkms packages
  
- #### Option 2: Install librealsense2 (without graphical tools and examples) debian package from ROS servers:
  - [Configure](http://wiki.ros.org/Installation/Ubuntu/Sources) your Ubuntu repositories
  - Install all realsense ROS packages by ```sudo apt install ros-<ROS_DISTRO>-librealsense2*```
    - For example, for Humble distro: ```sudo apt install ros-humble-librealsense2*```

- #### Option 3: Build from source
  - Download the latest [Intel&reg; RealSense&trade; SDK 2.0](https://github.com/IntelRealSense/librealsense/releases/tag/v2.53.1)
  - Follow the instructions under [Linux Installation](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md)
  
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

![rviz display](./rviz.png)

### find object GUI

![find-object](./findobject.png)

## 2.  Add object image for detection

* Using find object gui for adding image
  - > edit
  - > add object from scene
  - > take picture
  - > crop object

![find-object with object](./findobject2.png)

### tf synchronize

![rviz display tf](./rviz2.png)

## 3.  Run a terminal for controlling robot

```sh
    rosrun CR5_Project service_call.launch
```

* this command will run 2 nodes and spawn new terminal for commanding
  - service_call
  - main_control

### new terminal for input command
![new terminal](./maincontrol.png)

## Real Robotic Arm

### Dobot CR5 
![Dobot CR5](./dobot1.jpg)

### Intel Realsense D435i
![Intel Realsense D435i](./dobot2.jpg)

# References
- **CR_ROS**: https://github.com/Dobot-Arm/CR_ROS
- **find-object**: https://github.com/introlab/find-object
