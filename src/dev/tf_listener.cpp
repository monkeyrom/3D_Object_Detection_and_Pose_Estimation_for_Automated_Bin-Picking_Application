#include <cstdio>
#include "tf/transform_listener.h"
#include "ros/ros.h"

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


int main(int argc, char ** argv)
{
  //Initialize ROS
  ros::init(argc, argv, "tf_echo", ros::init_options::AnonymousName);

  // Allow 2 or 3 command line arguments
  if (argc < 3 || argc > 4)
  {
    printf("Usage: tf_echo source_frame target_frame [echo_rate]\n\n");
    printf("This will echo the transform from the coordinate frame of the source_frame\n");
    printf("to the coordinate frame of the target_frame. \n");
    printf("Note: This is the transform to get data from target_frame into the source_frame.\n");
    printf("Default echo rate is 1 if echo_rate is not given.\n");
    return -1;
  }

  ros::NodeHandle nh;

  double rate_hz;
  if (argc == 4)
  {
    // read rate from command line
    rate_hz = atof(argv[3]);
  }
  else
  {
    // read rate parameter
    ros::NodeHandle p_nh("~");
    p_nh.param("rate", rate_hz, 1.0);
  }
  if (rate_hz <= 0.0)
  {
    std::cerr << "Echo rate must be > 0.0\n";
    return -1;
  }
  ros::Rate rate(1);

  //Instantiate a local listener
  echoListener echoListener;

  std::string source_frameid = std::string("base_link");
  std::string target_frameid = std::string("object_16");

  // Wait for up to one second for the first transforms to become avaiable. 
  echoListener.tf.waitForTransform(source_frameid, target_frameid, ros::Time(), ros::Duration(1.0));

  //Nothing needs to be done except wait for a quit
  //The callbacks withing the listener class
  //will take care of everything
  while(nh.ok())
    {
      try
      {
        tf::StampedTransform echo_transform;
        echoListener.tf.lookupTransform(source_frameid, target_frameid, ros::Time(), echo_transform);
        std::cout.precision(3);
        std::cout.setf(std::ios::fixed,std::ios::floatfield);
        std::cout << "At time " << echo_transform.stamp_.toSec() << std::endl;
        double yaw, pitch, roll;
        echo_transform.getBasis().getRPY(roll, pitch, yaw);
        tf::Quaternion q = echo_transform.getRotation();
        tf::Vector3 v = echo_transform.getOrigin();
        std::cout << "- Translation: [" << v.getX() << ", " << v.getY() << ", " << v.getZ() << "]" << std::endl;

       //print transform
      }
      catch(tf::TransformException& ex)
      {
        std::cout << "Failure at "<< ros::Time::now() << std::endl;
        std::cout << "Exception thrown:" << ex.what()<< std::endl;
        std::cout << "The current list of frames is:" <<std::endl;
        std::cout << echoListener.tf.allFramesAsString()<<std::endl; 
      }
      rate.sleep();
    }
  return 0;
};