#include "ros/ros.h"
#include "std_msgs/String.h"
#include "CR5_Project/ObjectMsg.h"
#include <sstream>
#include <iostream>

#include <unistd.h>
#include <cstdio>
#include "tf/transform_listener.h"
#include "tf/tf.h"
#include <string>
#include <boost/bind.hpp>
#include <boost/thread.hpp>

using namespace tf;
using namespace ros;
using namespace std;

#define _USE_MATH_DEFINES

class echoListener
{
  public:

    tf::TransformListener tf;

    //constructor with name
    echoListener()
    {

    };

    ~echoListener()
    {

  };

  private:

};

int checkpose (int x, int y, int z)
{	
	echoListener echoListener;

  	std::string source_frameid = std::string("base_link");
  	std::string target_eef = std::string("Link6");
	bool check = false;

	while (check == false) {
		echoListener.tf.waitForTransform(source_frameid, target_eef, ros::Time(), ros::Duration(0.2));
		tf::StampedTransform echo_transform;
    	echoListener.tf.lookupTransform(source_frameid, target_eef, ros::Time(), echo_transform);

        //double yaw, pitch, roll;
        //echo_transform.getBasis().getRPY(roll, pitch, yaw);
        //tf::Quaternion q = echo_transform.getRotation();
        tf::Vector3 v = echo_transform.getOrigin();
		int actual_x,actual_y,actual_z ;
		actual_x = v.getX()*1000;
		actual_y = v.getY()*1000;
		actual_z = v.getZ()*1000;
		//std::cout << "Checking: [" << actual_x << ", " << actual_y << ", " << actual_z << "]" << std::endl;

		if (abs(abs(actual_x) - abs(x))<= 5 && abs(abs(actual_y) - abs(y))<= 5 && abs(actual_z - z)<= 5) 
		{check = true;}
		usleep(100000);
	}
  return 0;
}

int checkpose_rpy (int x, int y, int z, int rx, int ry, int rz)
{	
	echoListener echoListener;

  	std::string source_frameid = std::string("base_link");
  	std::string target_eef = std::string("Link6");
	bool check = false;

	while (check == false) {
		echoListener.tf.waitForTransform(source_frameid, target_eef, ros::Time(), ros::Duration(0.2));
		tf::StampedTransform echo_transform;
    	echoListener.tf.lookupTransform(source_frameid, target_eef, ros::Time(), echo_transform);

        double yaw, pitch, roll;
        echo_transform.getBasis().getRPY(roll, pitch, yaw);
        tf::Quaternion q = echo_transform.getRotation();
        tf::Vector3 v = echo_transform.getOrigin();
		int actual_x,actual_y,actual_z,actual_rx,actual_ry,actual_rz ;
		actual_x = v.getX()*1000;
		actual_y = v.getY()*1000;
		actual_z = v.getZ()*1000;
		actual_rx = roll*180.0/M_PI;
		actual_ry = pitch*180.0/M_PI;
		actual_rz = yaw*180.0/M_PI;

		std::cout << "Checking: [" << actual_x << ", " << actual_y << ", " << actual_z << ", " << actual_rx << ", " << actual_ry << ", " << actual_rz << "]" << std::endl;
		if (abs(abs(actual_x) - abs(x))<= 5 && abs(abs(actual_y) - abs(y))<= 5 && abs(actual_z - z)<= 5 && abs(abs(actual_rx) - abs(rx))<= 5 && abs(abs(actual_ry) - abs(ry))<= 5 && abs(actual_rz - rz)<= 5) 
		{check = true;}
		usleep(100000);
	}
  return 0;
}

int checkpose_focus (int x, int y, int z)
{	
	int at_goal;
	echoListener echoListener;
  	std::string source_frameid = std::string("base_link");
  	std::string target_eef = std::string("Link6");

	echoListener.tf.waitForTransform(source_frameid, target_eef, ros::Time(), ros::Duration(0.2));
	tf::StampedTransform echo_transform;
	echoListener.tf.lookupTransform(source_frameid, target_eef, ros::Time(), echo_transform);
	tf::Vector3 v = echo_transform.getOrigin();
	int actual_x,actual_y,actual_z ;

	actual_x = v.getX()*1000;
	actual_y = v.getY()*1000;
	actual_z = v.getZ()*1000;

	if (abs(abs(actual_x) - abs(x))<= 5 && abs(abs(actual_y) - abs(y))<= 5 && abs(actual_z - z)<= 5) 
	{at_goal = 1;}
	else {at_goal = 0;}

	return at_goal;
}

int checkpose_object (int x, int y, int z, int object_id)
{	
	int object_stay;
	echoListener echoListener;
	std::string source_frameid = std::string("base_link");
  	std::string target_frameid = std::string("object_1");
  	std::string target_frameid2 = std::string("object_2");
	std::string target_frameid3 = std::string("object_3");
	std::string target_frameid4 = std::string("object_4");
	std::string target_frameid5 = std::string("object_5");

	std::string final_target;

	if (object_id == 1) {final_target = target_frameid;}
	if (object_id == 2) {final_target = target_frameid2;}
	if (object_id == 3) {final_target = target_frameid3;}
	if (object_id == 4) {final_target = target_frameid4;}
	if (object_id == 5) {final_target = target_frameid5;}

	ros::NodeHandle n;
	ros::Publisher chatter_pub2 = n.advertise<std_msgs::String>("Cmd_Talker", 100);
	std_msgs::String msg;

	if (echoListener.tf.waitForTransform(source_frameid, final_target, ros::Time(), ros::Duration(0.8)) == 1)  
	{
		tf::StampedTransform echo_transform;
		echoListener.tf.lookupTransform(source_frameid, final_target, ros::Time(), echo_transform);
		tf::Vector3 v = echo_transform.getOrigin();
		int actual_x,actual_y,actual_z ;

		actual_x = v.getX()*1000;
		actual_y = v.getY()*1000;
		actual_z = v.getZ()*1000;

		if (abs(abs(actual_x)-abs(x)) >= 20 || abs(abs(actual_y)-abs(y)) >= 20 || abs(abs(actual_z)-abs(z)) >= 20) 
		{	
			//ROS_INFO("Delta X : [%0.3f] Delta Y : [%0.3f] Delta Y : [%0.3f]", abs(abs(actual_x)-abs(x)), abs(abs(actual_y)-abs(y)), abs(abs(actual_z)-abs(z)));
			std::stringstream cmd;
			ROS_INFO("Object move");
			cmd << "object_not_stay";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			object_stay = 1;
		}
		else
		{
			object_stay = 0;
			//ROS_INFO("Delta X : [%0.3f] Delta Y : [%0.3f] Delta Y : [%0.3f]", abs(abs(actual_x)-abs(x)), abs(abs(actual_y)-abs(y)), abs(abs(actual_z)-abs(z)));
		}
	}
	else
	{	
		std::stringstream cmd;
		ROS_INFO("Checking object again");
		cmd << "object_not_stay";
		msg.data = cmd.str();
		chatter_pub2.publish(msg);

		if (echoListener.tf.waitForTransform(source_frameid, target_frameid, ros::Time(), ros::Duration(1.5)) == 1)  
		{
			object_stay = 1;
		}
		else
		{
		ROS_INFO("Object not found");
		object_stay = -1;
		}
	}
	return object_stay;
}

int checkpose_object_focus (int x, int y, int z, int object_id)
{	
	int object_stay;
	echoListener echoListener;
	std::string source_frameid = std::string("base_link");
  	std::string target_frameid = std::string("object_1");
  	std::string target_frameid2 = std::string("object_2");
	std::string target_frameid3 = std::string("object_3");
	std::string target_frameid4 = std::string("object_4");
	std::string target_frameid5 = std::string("object_5");

	std::string final_target;

	if (object_id == 1) {final_target = target_frameid;}
	if (object_id == 2) {final_target = target_frameid2;}
	if (object_id == 3) {final_target = target_frameid3;}
	if (object_id == 4) {final_target = target_frameid4;}
	if (object_id == 5) {final_target = target_frameid5;}

	ros::NodeHandle n;
	ros::Publisher chatter_pub2 = n.advertise<std_msgs::String>("Cmd_Talker", 100);
	std_msgs::String msg;

	if (echoListener.tf.waitForTransform(source_frameid, final_target, ros::Time(), ros::Duration(0.3)) == 1)  
	{
		tf::StampedTransform echo_transform;
		echoListener.tf.lookupTransform(source_frameid, final_target, ros::Time(), echo_transform);
		tf::Vector3 v = echo_transform.getOrigin();
		int actual_x,actual_y,actual_z ;

		actual_x = v.getX()*1000;
		actual_y = v.getY()*1000;
		actual_z = v.getZ()*1000;

		if (abs(abs(actual_x)-abs(x)) <= 20 || abs(abs(actual_y)-abs(y)) <= 20 || abs(abs(actual_z)-abs(z))<= 20) 
		{
			object_stay = 0;
		}
		else
		{
			std::stringstream cmd;
			std::cout << "Object move" << std::endl;
			cmd << "object_not_stay";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			object_stay = 1;
		}
	}
	else
	{	
		std::stringstream cmd;
		std::cout << "Object move" << std::endl;
		cmd << "object_not_stay";
		msg.data = cmd.str();
		chatter_pub2.publish(msg);

		if (echoListener.tf.waitForTransform(source_frameid, target_frameid, ros::Time(), ros::Duration(1.0)) == 1)  
		{
			object_stay = 1;
		}
		else
		{
		std::cout << "Object not found" << std::endl;
		object_stay = -1;
		}
	}
	return object_stay;
}

int picking_object (int object_id, int box_count)
{
	ros::NodeHandle n;
	ros::Publisher chatter_pub1 = n.advertise<CR5_Project::ObjectMsg>("Object_Position", 100);
	ros::Publisher chatter_pub2 = n.advertise<std_msgs::String>("Cmd_Talker", 100);

	echoListener echoListener;
	std::string source_frameid = std::string("base_link");
	std::string camera_frameid = std::string("camera_link");
  	std::string target_frameid = std::string("object_1");
  	std::string target_frameid2 = std::string("object_2");
	std::string target_frameid3 = std::string("object_3");
	std::string target_frameid4 = std::string("object_4");
	std::string target_frameid5 = std::string("object_5");
  	std::string target_eef = std::string("Link6");

	std::string final_target;

	if (object_id == 1) {final_target = target_frameid;}
	if (object_id == 2) {final_target = target_frameid2;}
	if (object_id == 3) {final_target = target_frameid3;}
	if (object_id == 4) {final_target = target_frameid4;}
	if (object_id == 5) {final_target = target_frameid5;}
	
	CR5_Project::ObjectMsg msg;
	int carry = 0;
	int checking = 0;
	int place = 0;
	int box = box_count;
	int box_stack;
					
	while (place == 0)
	{
		if (carry == 0 && echoListener.tf.waitForTransform(source_frameid, final_target, ros::Time(), ros::Duration(0.2)) == 1)
		{
			tf::StampedTransform echo_transform;
			echoListener.tf.lookupTransform(source_frameid, final_target, ros::Time(), echo_transform);
			tf::Vector3 v = echo_transform.getOrigin();

			int goal_x = v.getX()*1000;
			int goal_y = v.getY()*1000;
			int goal_z = v.getZ()*1000;
			int goal_rx = 180;
			int goal_ry = 0;
			int goal_rz = 180;
													
			int goal_x_cal = goal_x;
			int goal_y_cal = goal_y + 50;
			int goal_z_cal = 390;
								
			msg.x = goal_x_cal;
			msg.y = goal_y_cal;
			msg.z = goal_z_cal;
			msg.rx = goal_rx;
			msg.ry = goal_ry;
			msg.rz = goal_rz;

			ROS_INFO("Moving to x:[%0.3f], y:[%0.3f], z:[%0.3f]", msg.x, msg.y, msg.z);
			chatter_pub1.publish(msg);
							
			while(checkpose_focus(goal_x_cal,goal_y_cal,goal_z_cal) == 0 && checking == 0)
			{
				int object_state = checkpose_object(goal_x,goal_y,goal_z,object_id);
				
				//object state 0 = object stay
				//object state 1 = object move
				//object state -1 = object lost

				if (object_state == 1)
				{
					checking = 1; 
					sleep(1);
				}
				else if (object_state == 0)
				{
					ROS_INFO(" ~ ");
					//usleep(100000);
				}
				else if (object_state == -1)
				{
					ROS_INFO("Return to Home Pose ");
					std_msgs::String msg;
					std::stringstream cmd;
					cmd << "object_not_stay";
					msg.data = cmd.str();
					chatter_pub2.publish(msg);

					std::stringstream cmd2;
					cmd2 << "home";
					msg.data = cmd2.str();
					chatter_pub2.publish(msg);
					checkpose (143,-580,405);
					checking = 1;
					carry = 0;
					sleep(2);
				}
			}

			if (checkpose_focus(goal_x_cal,goal_y_cal,goal_z_cal) == 1)
			{
				carry = 1;
				usleep(100000);
			}
			checking = 0;
		}
		
		if (carry == 0 && echoListener.tf.waitForTransform(source_frameid, final_target, ros::Time(), ros::Duration(0.2)) == 0)
		{
			place = 1;
			box_stack == 0;
		}
		
		if (carry == 1)
		{
			tf::StampedTransform echo_transform;
			echoListener.tf.lookupTransform(source_frameid, final_target, ros::Time(), echo_transform);
			tf::Vector3 v = echo_transform.getOrigin();

			int goal_x = v.getX()*1000;
			int goal_y = v.getY()*1000;
			int goal_z = v.getZ()*1000;
			int goal_rx = 180;
			int goal_ry = 0;
			int goal_rz = 180;
													
			int goal_x_cal = goal_x;
			int goal_y_cal = goal_y + 50;
			int goal_z_cal = goal_z + 280;
								
			msg.x = goal_x_cal;
			msg.y = goal_y_cal;
			msg.z = goal_z_cal;
			msg.rx = goal_rx;
			msg.ry = goal_ry;
			msg.rz = goal_rz;

			ROS_INFO("Moving to x:[%0.3f], y:[%0.3f], z:[%0.3f]", msg.x, msg.y, msg.z);
			chatter_pub1.publish(msg);
							
			while(checkpose_focus(goal_x_cal,goal_y_cal,goal_z_cal) == 0 && checking == 0)
			{
				int object_state = checkpose_object(goal_x,goal_y,goal_z,object_id);
				
				//object state 0 = object stay
				//object state 1 = object move
				//object state -1 = object lost

				if (object_state == 1){checking = 1; sleep(1);}
				else if (object_state == 0){
					ROS_INFO(" ~ ");
					//usleep(100000);
					}
				else if (object_state == -1)
				{
					ROS_INFO("Return to Home Pose ");
					std_msgs::String msg;
					std::stringstream cmd;
					cmd << "object_not_stay";
					msg.data = cmd.str();
					chatter_pub2.publish(msg);

					std::stringstream cmd2;
					cmd2 << "home";
					msg.data = cmd2.str();
					chatter_pub2.publish(msg);
					checkpose (143,-580,405);
					checking = 1;
					carry = 0;
					sleep(2);
				}
			}
			if (checkpose_focus(goal_x_cal,goal_y_cal,goal_z_cal) == 1)
			{
				carry = 2;
				usleep(500000);
			}
			checking = 0;
		}

		if (carry == 2){
			
			tf::StampedTransform echo_transform;
			tf::StampedTransform echo_cam;
			echoListener.tf.lookupTransform(source_frameid, final_target, ros::Time(), echo_transform);
			echoListener.tf.lookupTransform(camera_frameid, final_target, ros::Time(), echo_cam);
			double yaw, pitch, roll;
			echo_cam.getBasis().getRPY(roll, pitch, yaw);
			tf::Vector3 v = echo_transform.getOrigin();

			int goal_x = v.getX()*1000;
			int goal_y = v.getY()*1000;
			int goal_z = v.getZ()*1000;
			int goal_roll = roll*180.0/M_PI;
			int goal_pitch = pitch*180.0/M_PI;
			int goal_yall = yaw*180.0/M_PI;

			int goal_x_cal = goal_x;
			int goal_y_cal = goal_y;
			int goal_z_cal = goal_z + 54;
			int goal_rx_cal = goal_pitch + 180;
			int goal_ry_cal = goal_yall - 180;
			int goal_rz_cal = goal_roll + 180;
						
			if (goal_z_cal < 15) {goal_z_cal = 15;}
			else if (goal_z_cal >= 15){goal_z_cal = goal_z_cal;}

			msg.x = goal_x_cal;
			msg.y = goal_y_cal;
			msg.z = goal_z_cal;
			msg.rx = goal_rx_cal;
			msg.ry = goal_ry_cal;
			msg.rz = goal_rz_cal;

			ROS_INFO("Picking Object at x:[%f], y:[%f], z:[%f], rx:[%f], ry:[%f], rz:[%f]", msg.x, msg.y, msg.z, msg.rx, msg.ry, msg.rz);
			chatter_pub1.publish(msg);
			
			usleep(1000000);
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "SetVac";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Picked object");

			checkpose(goal_x_cal,goal_y_cal,goal_z_cal);

			carry = 3;
		}

		if (carry == 3)
		{
			usleep(100000);

			carry = 4;
		}

		if (carry == 4)
		{
			std_msgs::String msg;
			std::stringstream cmd;
			cmd << "home";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);			
			checkpose(143,-580,405);

			carry = 5;
		}

		if (carry == 5)
		{
			int goal_x;
			int goal_y;
			int goal_z;
			int z_height;
			goal_x = -180;

			if (object_id == 1){goal_y = -710;}
			if (object_id == 2){goal_y = -710;}
			if (object_id == 3){goal_y = -540;}
			if (object_id == 4){goal_y = -540;}
			if (object_id == 5){goal_y = -540;}

			goal_z = -70 + (box);
			if (goal_z < 50){goal_z = 50;}
			else if (goal_z >= 50){goal_z = goal_z;}

			int goal_x_cal = goal_x;
			int goal_y_cal = goal_y;
			int goal_z_cal = goal_z;
			int goal_rx_cal = 180;
			int goal_ry_cal = 0;
			int goal_rz_cal = 180;

			msg.x = goal_x_cal;
			msg.y = goal_y_cal;
			msg.z = goal_z_cal;
			msg.rx = goal_rx_cal;
			msg.ry = goal_ry_cal;
			msg.rz = goal_rz_cal;

			ROS_INFO("Placing Object at x:[%f], y:[%f], z:[%f], rx:[%f], ry:[%f], rz:[%f]", msg.x, msg.y, msg.z, msg.rx, msg.ry, msg.rz);
			chatter_pub1.publish(msg);
			checkpose(goal_x_cal,goal_y_cal,goal_z_cal);

			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "ResetVac";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Placed object");
			usleep(200000);

			carry = 6;
		}
		
		if (carry == 6)
		{
			int goal_x;
			int goal_y;
			goal_x = -180;

			if (object_id == 1){goal_y = -710;}
			if (object_id == 2){goal_y = -710;}
			if (object_id == 3){goal_y = -540;}
			if (object_id == 4){goal_y = -540;}
			if (object_id == 5){goal_y = -540;}

			int goal_x_cal = goal_x;
			int goal_y_cal = goal_y;
			int goal_z_cal = 200;
			int goal_rx_cal = 180;
			int goal_ry_cal = 0;
			int goal_rz_cal = 180;

			msg.x = goal_x_cal;
			msg.y = goal_y_cal;
			msg.z = goal_z_cal;
			msg.rx = goal_rx_cal;
			msg.ry = goal_ry_cal;
			msg.rz = goal_rz_cal;

			chatter_pub1.publish(msg);
			checkpose(goal_x_cal,goal_y_cal,goal_z_cal);
			usleep(200000);

			carry = 7;
		}

		if (carry == 7)
		{	
			ROS_INFO("Go Home");

			std_msgs::String msg;
			std::stringstream cmd;
			cmd << "home";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);			
			checkpose(143,-580,405);
			usleep(200000);

			carry = 0;
			place = 1;
			box_stack = box;
		}
	}

	ROS_INFO("Picking done");
	return box_stack;
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "talker");

	ros::NodeHandle n;

  	ros::Publisher chatter_pub1 = n.advertise<CR5_Project::ObjectMsg>("Object_Position", 100);
  	ros::Publisher chatter_pub2 = n.advertise<std_msgs::String>("Cmd_Talker", 100);

  	ros::Rate loop_rate(10);
  
  	float position_x,position_y,position_z;

// Starting
	std::cout << "Started rosrun CR5_Project main_control";
	std::cout << "\n \nSUMMARY";
	std::cout << "\n========";
	std::cout << "\n \nThis program use for controlling CR5 Robot, still in development stage.";
	std::cout << "\nCan also work with Realsense camera D435i.";
	std::cout << "\n \nCOMMANDS INPUT";
	std::cout << "\n========";
	std::cout << "\n* Home";
	std::cout << "\n* Pose";
	std::cout << "\n* EnableRobot";
	std::cout << "\n* DisableRobot";
	std::cout << "\n* ClearError";
	std::cout << "\n* Point0";
	std::cout << "\n* Point1";
	std::cout << "\n* Picking";
	std::cout << "\n* PickMe";

  	//Instantiate a local listener
  	echoListener echoListener;
		
	std::cout << "\n \nInitializing echoListenter for Transform (tf).\n \n";
		
  	std::string source_frameid = std::string("base_link");
	std::string camera_frameid = std::string("camera_link");
  	std::string target_frameid = std::string("object_1");
  	std::string target_frameid2 = std::string("object_2");
	std::string target_frameid3 = std::string("object_3");
	std::string target_frameid4 = std::string("object_4");
	std::string target_frameid5 = std::string("object_5");
  	std::string target_eef = std::string("Link6");
		
	ROS_INFO("source_frameid = \"base_link\"");
	ROS_INFO("target_eef = \"Link6\"");
	ROS_INFO("camera_frameid = \"camera_link\"");
	ROS_INFO("target_framid = \"object_1\"");
	ROS_INFO("target_framid2 = \"object_2\"");
	ROS_INFO("target_framid3 = \"object_3\"");
	ROS_INFO("target_framid4 = \"object_4\"");
	ROS_INFO("target_framid5 = \"object_5\"\n");
	ROS_INFO("Initializing new console terminal for using ros service.");
	ROS_INFO("Enable Robot");

  	while (ros::ok())
    {	
		ros::Rate rate(1);

		//----------Simple command-------------//

      	CR5_Project::ObjectMsg msg;
		std::string cmd;
		std::cout << "\nUser input command: ";
		std::cin >> cmd;

		if (cmd == "Pose"){
			std::cout << "Input position to publish" << std::endl << "position.x :";
      		std::cin >> position_x;
      		std::cout << "position.y :";
      		std::cin >> position_y;
      		std::cout << "position.z :";
      		std::cin >> position_z;

			msg.x = position_x;
			msg.y = position_y;
			msg.z = position_z;
			msg.rx = 180;
			msg.ry = 0;
			msg.rz = 180;

      		chatter_pub1.publish(msg);
		}
      	else if (cmd == "Home"){
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "home";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Moving to Home Pose");
		}
		else if (cmd == "Sleep"){
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "sleep";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Moving to Sleep Pose");
		}
		else if (cmd == "ClearError"){
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "ClearError";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Published Clear Error");
		}
		else if (cmd == "DisableRobot"){
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "DisableRobot";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Published Disable Robot");
		}
		else if (cmd == "EnableRobot")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "EnableRobot";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Published Enable Robot");
		}
		else if (cmd == "Point0")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "Point0";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Moving to Point 0");
		}
		else if (cmd == "Point1")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "Point1";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Moving to Point 1");
		}
		else if (cmd == "Point1_R")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "Point1_R";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Moving to Point 1_R");
		}
		else if (cmd == "Point2")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "Point2";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Moving to Point 2");
		}
		else if (cmd == "SetVac")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "SetVac";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Set Robot Tool0 (Vacuum)");
		}
		else if (cmd == "ResetVac")
		{
			std_msgs::String msg;
			std::stringstream cmd;
    		cmd << "ResetVac";
			msg.data = cmd.str();
			chatter_pub2.publish(msg);
			ROS_INFO("Reset Robot Tool0 (Vacuum)");
		}
		else if (cmd == "Picking")
		{
			if (echoListener.tf.waitForTransform(source_frameid, target_frameid, ros::Time(), ros::Duration(0.2)) == 1)
			{
				picking_object(1,1);
			}
			else if (echoListener.tf.waitForTransform(source_frameid, target_frameid2, ros::Time(), ros::Duration(0.2)) == 1)
			{
				picking_object(2,1);
			}
			else if (echoListener.tf.waitForTransform(source_frameid, target_frameid3, ros::Time(), ros::Duration(0.2)) == 1)
			{
				picking_object(3,1);
			}
			else if (echoListener.tf.waitForTransform(source_frameid, target_frameid4, ros::Time(), ros::Duration(0.2)) == 1)
			{
				picking_object(4,1);
			}
			else if (echoListener.tf.waitForTransform(source_frameid, target_frameid5, ros::Time(), ros::Duration(0.2)) == 1)
			{
				picking_object(5,1);
			}
		}
		else if (cmd == "PickMe")
		{	
			int box1 = 0;
			int box2 = 0;
			int box3 = 0;
			int box4 = 0;
			int box5 = 0;
			int box_stack;

			while (ros::ok) 
			{
				if (echoListener.tf.waitForTransform(source_frameid, target_frameid, ros::Time(), ros::Duration(0.2)) == 1)
				{
					box1 += 25;
					box_stack = picking_object(1, box1);
					box1 = box1 - 25 + box_stack;
				}
				else if (echoListener.tf.waitForTransform(source_frameid, target_frameid2, ros::Time(), ros::Duration(0.2)) == 1)
				{
					box1 += 25;
					box_stack = picking_object(2, box1);
					box1 = box1 - 25 + box_stack;
				}
				else if (echoListener.tf.waitForTransform(source_frameid, target_frameid3, ros::Time(), ros::Duration(0.2)) == 1)
				{
					box2 += 30;
					box_stack = picking_object(3, box2);
					box2 = box2 - 30 + box_stack;
				}
				else if (echoListener.tf.waitForTransform(source_frameid, target_frameid4, ros::Time(), ros::Duration(0.2)) == 1)
				{
					box2 += 25;
					box_stack = picking_object(4, box2);
					box2 = box2 - 25 + box_stack;
				}
				else if (echoListener.tf.waitForTransform(source_frameid, target_frameid5, ros::Time(), ros::Duration(0.2)) == 1)
				{
					box2 += 50;
					box_stack = picking_object(5, box2);
					box2 = box2 - 50 + box_stack;
				}
			}
		}

		else {std::cout << "\n----- command not found ----- \n";}
	}

	ros::spinOnce();
	loop_rate.sleep();
  	return 0;
}
