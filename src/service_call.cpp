#include "ros/ros.h"
#include "std_msgs/String.h"
#include "CR5_Project/ObjectMsg.h"
#include <sstream>
#include <iostream>

void chatterCallback(const CR5_Project::ObjectMsg::ConstPtr& msg)
{
  ROS_INFO("Recieved Position :\nx: [%0.3f]\ny: [%0.3f]\nz: [%0.3f]\nrx: [%0.1f]\nry: [%0.1f]\nrz: [%0.1f]", msg->x, msg->y, msg->z, msg->rx, msg->ry, msg->rz);
  char cmd[200];
  sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: %0.3f, y: %0.3f, z: %0.3f, a: %0.3f, b: %0.3f, c: %0.3f}\"'", msg->x, msg->y, msg->z, msg->rx, msg->ry, msg->rz);
  system(cmd);
}

void cmdCallback(const std_msgs::String::ConstPtr& msg)
{
  std::string cmd;
  cmd = msg->data.c_str();
 /* if (cmd == "home"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/JointMovJ \"{j1: 90.0, j2: 15.0, j3: 83.0, j4: -8.0, j5: -89.0, j6: 0.0}\"'");
    system(cmd);
  }*/
  if (cmd == "home"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: 143.0, y: -580.0, z: 450.0, a: 180.0, b: 0.0, c: 180.0}\"'");
    system(cmd);
  }
  if (cmd == "sleep"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/JointMovJ \"{j1: 115.0, j2: -30.0, j3: 135.0, j4: -15.0, j5: -90.0, j6: 0.0}\"'");
    system(cmd);
  }
  if (cmd == "ClearError"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/ClearError'");
    system(cmd);
  }
  if (cmd == "DisableRobot"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/DisableRobot'");
    system(cmd);
  }
  if (cmd == "EnableRobot"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/EnableRobot'");
    system(cmd);
  }
  if (cmd == "object_not_stay"){
    char cmd_stop[200];
		sprintf(cmd_stop, "gnome-terminal --tab -e 'rosservice call /dobot_bringup/srv/StopScript'");
		system(cmd_stop);
		sprintf(cmd_stop, "gnome-terminal --tab -e 'rosservice call /dobot_bringup/srv/EnableRobot'");
		system(cmd_stop);
  }
  if (cmd == "Point0"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/JointMovJ \"{j1:0.0, j2:0.0, j3:0.0, j4:0.0, j5:0.0, j6:0.0}\"'");
    system(cmd);
  }
  if (cmd == "Point1"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: 143.0, y: -600.0, z: 170.0, a: 180.0, b: 0.0, c: 180.0}\"'");
    system(cmd);
  }
  if (cmd == "Point2"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: 143.0, y: -600.0, z: 200.0, a: 180.0, b: 0.0, c: 180.0}\"'");
    system(cmd);
  }
  if (cmd == "Point3"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: 20.0, y: -550.0, z: 260.0, a: 180.0, b: 0.0, c: 180.0}\"'");
    system(cmd);
  }
  if (cmd == "Point5"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: -210.0, y: -580.0, z: 150.0, a: 180.0, b: 0.0, c: 180.0}\"'");
    system(cmd);
  }
  if (cmd == "Speed100"){
	  char cmd_spdJ[200];
	  sprintf(cmd_spdJ, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/SpeedJ \"r: 100 \"'");
	  system(cmd_spdJ);
  }
  if (cmd == "Speed50"){
	  char cmd_spdJ[200];
	  sprintf(cmd_spdJ, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/SpeedJ \"r: 50 \"'");
	  system(cmd_spdJ);
  }
  if (cmd == "Acc100"){
	  char cmd_spdJ[200];
	  sprintf(cmd_spdJ, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/AccJ \"r: 100 \"'");
	  system(cmd_spdJ);
  }
  if (cmd == "inventory"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/MovJ \"{x: 264.0, y: -310.0, z: 96.0, a: 180.0, b: 0.0, c: 180.0}\"'");
    system(cmd);
  }
  if (cmd == "inventory2"){
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call bringup/srv/MovJ \"{x: 0.0, y: -285.0, z: 385.0, a: 0.0, b: 0.0, c: 0.0}\"'");
    system(cmd);
    char cmd2[200];
    sprintf(cmd2, "gnome-terminal --tab -e 'rosservice call bringup/srv/MovJ \"{x: 0.0, y: -375.0, z: 330.0, a: -90.0, b: 0.0, c: 0.0}\"'");
    system(cmd2);
  }
	if (cmd == "SetVac"){
    char cmd_magic[200];
	  sprintf(cmd_magic, "gnome-terminal --tab -e 'rosservice call /DobotServer/SetEndEffectorSuctionCup \"enableCtrl: 1 \nsuck: 1 \nisQueued: false\"'");
	  system(cmd_magic);
  }
  if (cmd == "ResetVac"){
    char cmd_magic[200];
	  sprintf(cmd_magic, "gnome-terminal --tab -e 'rosservice call /DobotServer/SetEndEffectorSuctionCup \"enableCtrl: 1 \nsuck: 0 \nisQueued: false\"'");
	  system(cmd_magic);
  }

  else {
    char cmd[200];
    sprintf(cmd, "gnome-terminal --tab -e 'rosservice call bringup/srv/JointMovJ \"{j1: 0.0, j2: 0.0, j3: 0.0, j4: 0.0, j5: 0.0, j6: 0.0}\"'");
    system(cmd);
  }
}

int main(int argc, char **argv)
{ 
  ros::init(argc, argv, "listener");
  
  ros::NodeHandle n;

  ros::Subscriber sub1 = n.subscribe("Object_Position", 10, chatterCallback);
  ros::Subscriber sub1_order = n.subscribe("main/target_order", 10, chatterCallback);
  ros::Subscriber sub2 = n.subscribe("Cmd_Talker", 10, cmdCallback);
  ros::Subscriber sub2_order = n.subscribe("main/cmd_talker", 10, cmdCallback);

// Starting
	std::cout << "Started rosrun CR5_Project service_call";
	std::cout << "\n \nSUMMARY";
	std::cout << "\n========";
	std::cout << "\n \nThis program is for using ros service to CR5 Robot. \nStill in development stage.";
	std::cout << "\n \nCOMMANDS INPUT";
	std::cout << "\n========";

  std::cout << "\nInitializing listener node for subscribe commands.";

  char newtmn[200];
  sprintf(newtmn, "gnome-terminal --geometry=90x24+0+0 --window \ --working-directory=/depot --title='Main Control Terminal' --command=\"rosrun CR5_Project node_order.py\"");
  system(newtmn);

  char cmd[200];
  sprintf(cmd, "gnome-terminal --tab -e 'rosservice call dobot_bringup/srv/EnableRobot'");
  system(cmd);

  ros::spin();

  return 0;
}