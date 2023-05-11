import rospy
from std_msgs.msg import String
from time import sleep
import tf
import math
from CR5_Project.msg import ObjectMsg
from tf.transformations import euler_from_quaternion

def home():
    cmd = "home"
    pub_cmd.publish(cmd)
    rospy.loginfo("Moving to Home Pose...")

def Point5():
    cmd = "Point5"
    pub_cmd.publish(cmd)
    print("Moving to Point 5...")

def robot_home_pose(home):
    #print('home checking...')
    try :
        listener.waitForTransform('base_link', 'Link6', rospy.Time(), rospy.Duration(0.2))
    except :
        return -1
    
    if listener.canTransform('base_link', 'Link6', rospy.Time()) :
        (trans,rot) = listener.lookupTransform("base_link", "Link6", rospy.Time())
        x = round(trans[0]*1000)
        y = round(trans[1]*1000)
        z = round(trans[2]*1000)
        #print("robot pose at [", x,y,z,"]")
        if abs(abs(x) - 143) <= 5 and abs(abs(y) - 580)  <= 5 and abs(abs(z) - 405) <= 5 :
            home = 1
        else :
            #print('waiting robot to home position')
            print('.')
            home = 0      #change to 0,1 for pass home checking
            sleep(0.2)
    else :
        home = -1

    if rospy.is_shutdown():
        print('Stop home Checking')
        return 0
    
    return home

def robot_check_pose(x_order,y_order,z_order):
    print('pose checking ...')
    pose = 0
    while pose == 0 :
        listener.waitForTransform('base_link', 'Link6', rospy.Time(), rospy.Duration(0.2))
        if listener.canTransform('base_link', 'Link6', rospy.Time()) :
            (trans,rot) = listener.lookupTransform('base_link', 'Link6', rospy.Time())
            x = round(trans[0]*1000)
            y = round(trans[1]*1000)
            z = round(trans[2]*1000)
            #print("command pose at [", x_order,y_order,z_order,"]")
            #print("robot pose at [", x,y,z,"]")
            if abs(abs(x) - abs(x_order)) <= 4 and abs(abs(y) - abs(y_order))  <= 4 and abs(abs(z) - abs(z_order)) <= 4 :
                pose = 1
            else :
                #print('waiting robot to the position')
                print('.')
                pose = 0        #change to 0,1 for pass pose checking
        else :
            print("Error : robot not found")
            pose = -1

        if rospy.is_shutdown():
            print('Stop Pose Checking')
            return 0
        
        sleep(0.2)
    
    return pose

def yolo_detect():
    process = "Yolo detect at %s" % rospy.get_time()
    cmd = "runYolo"
    rospy.loginfo(process)
    pub_order.publish(cmd)

def check_object():
    obj = 0
    source_frameid = 'base_link'
    try :
        listener.waitForTransform('obj_arduino', source_frameid, rospy.Time(), rospy.Duration(0.2))
        if listener.canTransform('obj_arduino', source_frameid, rospy.Time()) == 1 :
            obj = 1
    except :
        pass

    try :
        listener.waitForTransform('obj_raspi', source_frameid, rospy.Time(), rospy.Duration(0.2))
        if listener.canTransform('obj_raspi', source_frameid, rospy.Time()) and obj == 0:
            obj = 2
        if listener.canTransform('obj_raspi', source_frameid, rospy.Time()) and obj == 1:
            obj = 3
    except :
        pass

    else :
        print("cannot Transform object reffer to robot baselink")

    return obj

def move_close (focus_obj):
    if focus_obj == 1 :
        source_frameid = 'base_link'
        target_frameid = 'obj_arduino'
        listener.waitForTransform(target_frameid, source_frameid, rospy.Time(), rospy.Duration(0.2))
        if listener.canTransform(target_frameid, source_frameid, rospy.Time()) :
            (trans,rot) = listener.lookupTransform(source_frameid, target_frameid, rospy.Time())
            x = round(trans[0]*1000) - 30
            y = round(trans[1]*1000) + 50
            z = round(trans[2]*1000) + 200
            
        else :
            print("Error : object lost")
            return

    elif focus_obj == 2 :
        source_frameid = 'base_link'
        target_frameid = 'obj_raspi'
        listener.waitForTransform(source_frameid, target_frameid, rospy.Time(), rospy.Duration(0.2))
        if listener.canTransform(source_frameid, target_frameid, rospy.Time()) :
            (trans,rot) = listener.lookupTransform(source_frameid, target_frameid, rospy.Time())
            x = round(trans[0]*1000)
            y = round(trans[1]*1000) + 50
            z = round(trans[2]*1000) + 200
        else :
            print("Error : object lost")
            return

    target = ObjectMsg()
    target.x = x
    target.y = y
    target.z = z
    target.rx = 180
    target.ry = 0
    target.rz = 180
    rospy.loginfo(target)
    pub_target.publish(target)

    return (x,y,z)

def pick_phase1 (focus_obj):

    if focus_obj == 1 :
        x2,y2,z2,rx2,ry2,rz2 = 0,0,-100,0,0,0
        x3,y3,z3,rx3,ry3,rz3 = 0,0,-100,0,0,0
        source_frameid = 'base_link'
        camera_frameid = 'camera_link'
        target_frameid1 = 'object_6'
        target_frameid2 = 'object_6_b'
        target_frameid3 = 'object_6_c'
        try :
            listener.waitForTransform(camera_frameid, source_frameid, rospy.Time(), rospy.Duration(0.2))
            listener.waitForTransform(target_frameid1, source_frameid, rospy.Time(), rospy.Duration(0.2))
        except :
            pass
        try :
            listener.waitForTransform(target_frameid2, source_frameid, rospy.Time(), rospy.Duration(0.2))
        except :
            pass
        try :
            listener.waitForTransform(target_frameid3, source_frameid, rospy.Time(), rospy.Duration(0.2))
        except :
            pass

        if listener.canTransform(target_frameid1, source_frameid, rospy.Time()):
            echo_transform = listener.lookupTransform(source_frameid, target_frameid1, rospy.Time(0))
            echo_cam = listener.lookupTransform(target_frameid1, camera_frameid, rospy.Time(0))

            yaw, pitch, roll = euler_from_quaternion(echo_cam[1])
            v = echo_transform[0]

            x = int(v[0] * 1000)
            y = int(v[1] * 1000)
            z = int(v[2] * 1000)
            rx = int(roll * 180.0 / math.pi)
            ry = int(pitch * 180.0 / math.pi)
            rz = int(yaw * 180.0 / math.pi)

            x_cal = x
            y_cal = y
            z_cal = z + 54 if z + 54 >= 25 else 25
            rx_cal = ry + 180
            ry_cal = -(rx - 180)
            rz_cal = rz + 180

            if listener.canTransform(target_frameid2, source_frameid, rospy.Time()):
                echo_transform = listener.lookupTransform(source_frameid, target_frameid2, rospy.Time(0))
                echo_cam = listener.lookupTransform(target_frameid2, camera_frameid, rospy.Time(0))

                yaw, pitch, roll = euler_from_quaternion(echo_cam[1])
                v = echo_transform[0]

                x2 = int(v[0] * 1000)
                y2 = int(v[1] * 1000)
                z2 = int(v[2] * 1000)
                rx2 = int(roll * 180.0 / math.pi)
                ry2 = int(pitch * 180.0 / math.pi)
                rz2 = int(yaw * 180.0 / math.pi)

            if listener.canTransform(target_frameid3, source_frameid, rospy.Time()):
                echo_transform = listener.lookupTransform(source_frameid, target_frameid3, rospy.Time(0))
                echo_cam = listener.lookupTransform(target_frameid3, camera_frameid, rospy.Time(0))

                yaw, pitch, roll = euler_from_quaternion(echo_cam[1])
                v = echo_transform[0]

                x3 = int(v[0] * 1000)
                y3 = int(v[1] * 1000)
                z3 = int(v[2] * 1000)
                rx3 = int(roll * 180.0 / math.pi)
                ry3 = int(pitch * 180.0 / math.pi)
                rz3 = int(yaw * 180.0 / math.pi)

            if z2 > z and z2 > z3 :
                x_cal = x2
                y_cal = y2
                z_cal = z2 + 54 if z + 54 >= 25 else 25
                rx_cal = ry2 + 180
                ry_cal = -(rx2 - 180)
                rz_cal = rz2 + 180

            if z3 > z and z3 > z2 :
                x_cal = x3
                y_cal = y3
                z_cal = z3 + 54 if z + 54 >= 25 else 25
                rx_cal = ry3 + 180
                ry_cal = -(rx3 - 180)
                rz_cal = rz3 + 180

            target = ObjectMsg()
            target.x = x_cal
            target.y = y_cal
            target.z = z_cal + 25
            target.rx = 180
            target.ry = 0
            target.rz = 180
            rospy.loginfo(target)
            pub_target.publish(target)

            return (x_cal,y_cal,z_cal,rx_cal,ry_cal,rz_cal)

        else :
            print("Error : object lost")
            return -1

    elif focus_obj == 2 :
        source_frameid = 'base_link'
        target_frameid = 'obj_raspi'
        listener.waitForTransform(target_frameid, source_frameid, rospy.Time(), rospy.Duration(0.2))
        if listener.canTransform(target_frameid, source_frameid, rospy.Time()):
            (trans, rot) = listener.lookupTransform(source_frameid, target_frameid, rospy.Time())
            x = round(trans[0] * 1000)
            y = round(trans[1] * 1000)
            z = round(trans[2] * 1000)
            roll, pitch, yaw = tf.transformations.euler_from_quaternion(rot)
            rx = round(pitch * 180.0 / math.pi)
            ry = round(yaw * 180.0 / math.pi)
            rz = round(roll * 180.0 / math.pi)
            z_off = z + 54 if z + 54 >= 25 else 25

            rx = rx + 180
            ry = ry - 180
            rz = rz + 180

            target = ObjectMsg()
            target.x = x
            target.y = y
            target.z = z_off + 20
            target.rx = 180
            target.ry = 0
            target.rz = 180
            rospy.loginfo(target)
            pub_target.publish(target)

            return (x,y,z_off,rx,ry,rz)

        else :
            print("Error : object lost")
            return

def pick_phase2 (x,y,z,rx,ry,rz):
    target = ObjectMsg()
    target.x = x
    target.y = y
    target.z = z-3
    target.rx = rx 
    target.ry = ry 
    target.rz = rz 
    rospy.loginfo(target)
    pub_target.publish(target)
    return (x,y,z,rx,ry,rz)

def pick_phase3 (x,y,z,rx,ry,rz):
    target = ObjectMsg()
    target.x = x
    target.y = y
    target.z = z+80
    target.rx = rx 
    target.ry = ry
    target.rz = rz 
    rospy.loginfo(target)
    pub_target.publish(target)
    return (x,y,z)

def sunction_cup(set):
    if set == 1 :
        msg = "SetVac"
        pub_cmd.publish(msg)
        print("Set Robot Tool0 (Vacuum)...\n")
    elif set == 0 :
        msg = "ResetVac"
        pub_cmd.publish(msg)
        print("Set Robot Tool0 (Vacuum)...\n")
    return 0

def start_order():
    # Initial parameter
    step = 0
    focus_obj = 0
    while True :
        home_check = robot_home_pose(0)
        if step == 0 and home_check == -1 :         # Check Robot and not found
            print("Error : no robot found")
            break
        elif step == 0 and home_check == 0 :        # Check Robot and Robot not at home position
            step = 0
        elif step == 0 and home_check == 1 :        # Check Robot and Robot at home position
            yolo_detect()                           # publish to yolo node to detect
            sleep(0.5)                              # sleep 500 milisec
            if check_object() == 1 :                # echo tf found Arduino
                print("found obj_arduino")
                step = 1
                focus_obj = 1
            elif check_object() == 2 :              # echo tf found Raspi
                print("found obj_raspi")
                step = 1
                focus_obj = 2
            elif check_object() == 3 :              # echo tf found Arduino and Raspi
                print("found both obj_arduino and obj_raspi")
                step = 1
                focus_obj = 1
            else :
                print("no object found")            # echo tf not found object
                step = 0
        
        elif step == 1 :                              # move close to the object
            obj_target = move_close(focus_obj)
            x_order = obj_target[0]
            y_order = obj_target[1]
            z_order = obj_target[2]
            pose_check = robot_check_pose(x_order,y_order,z_order)
            print ("robot close to object")
            sleep(0.5)                              # sleep 200 milisec
            if pose_check == 1 :                    # Robot at position (close to object)
                step = 2
            if pose_check == -1 :
                break
            if pose_check == 0 :
                break
        
        elif step == 2 :                                # Robot close to object echo tf again and going to pick
            obj_target1 = pick_phase1(focus_obj)        # echo object position and move to 3 cm above object
            if obj_target1 == -1:                       # Object lost
                home()
                robot_home_pose(0)
                sleep(0.1)                              # sleep 200 milisec
                step = 0
                return
            else :
                x = obj_target1[0]
                y = obj_target1[1]
                z = obj_target1[2]
                rx = obj_target1[3]
                ry = obj_target1[4]
                rz = obj_target1[5]
                pose_check = robot_check_pose(obj_target1[0],obj_target1[1],obj_target1[2]+30)  # Check Robot position (3 cm above object)
                if pose_check == 1 :                                                            # Robot at the position (3 cm above object)
                    obj_target2 = pick_phase2(x,y,z,rx,ry,rz)                                   # move to object
                    sunction_cup(1)                                                             # Set sunction cup on
                    pose_check = robot_check_pose(obj_target2[0],obj_target2[1],obj_target2[2]) # Check Robot position (at object)
                    print ("robot picking object")
                    if pose_check == 1 :
                        print ('Picked object')
                        obj_target3 = pick_phase3(x,y,z,rx,ry,rz)
                        pose_check = robot_check_pose(obj_target3[0],obj_target3[1],obj_target3[2])
                        step = 3
                    if pose_check == -1 :
                        break
                    if pose_check == 0 :
                        break    
                if pose_check == -1 :
                    break
        
        elif step == 3 :                                    # go to inventory
            Point5()                                        # move robot to inventory
            pose_check = robot_check_pose(-210,-580,150)      # check robot at inventory
            sunction_cup(0)                                 # Set sunction cup off    
            sleep(0.3)                                      # sleep 300 milisec
            step = 4    

        elif step == 4 :
            home()
            robot_home_pose(0)
            sleep(0.2)                                      # sleep 200 milisec
            step = 0
                    
        if rospy.is_shutdown():
            print('Shutdown main loop')
            break

def start_service():
    print("Started rosrun CR5_Project main_control")
    print("\n================")
    print("    SUMMARY")
    print("================")
    print("\nThis program use for controlling CR5 Robot, still in developing stage.")
    print("The purpose of this project is to ...")
    print("\n================")
    print(" SERVICE LISTS")
    print("================")
    print("* Home           (Moving robot to home position)")
    print("* Pose           (Moving robot to x,y,z input)")
    print("* EnableRobot")
    print("* DisableRobot")
    print("* ClearError")
    print("* Sleep          (Moving robot to sleep position)")
    print("* Point0         (Set all robot joints to 0)")
    print("* Point1         (Moving robot to point 1)")    
    print("* PickingLoop    (Starting picking loop)\n")

    while True:
        service = input("Please type your service: ")
        if service == "Pose":
            print("Input position to publish")
            position_x = float(input("position.x: "))
            position_y = float(input("position.y: "))
            position_z = float(input("position.z: "))
            msg.x = position_x
            msg.y = position_y
            msg.z = position_z
            msg.rx = 180
            msg.ry = 0
            msg.rz = 180
            pub_target.publish(msg)
        elif service == "Home":
            msg = "home"
            pub_cmd.publish(msg)
            print("Robot moving to Home Pose...\n")
        elif service == "Sleep":
            msg = "sleep"
            pub_cmd.publish(msg)
            print("Robot moving to Sleep Pose...\n")
        elif service == "ClearError":
            msg = "ClearError"
            pub_cmd.publish(msg)
            print("Published Clear Error ...\n")
        elif service == "DisableRobot":
            msg = "DisableRobot"
            pub_cmd.publish(msg)
            print("Published Disable Robot...\n")
        elif service == "EnableRobot":
            msg = "EnableRobot"
            pub_cmd.publish(msg)
            print("Published Enable Robot...\n")
        elif service == "Point0":
            msg = "Point0"
            pub_cmd.publish(msg)
            print("Set all robot joints to 0...\n")
        elif service == "Point1":
            msg = "Point1"
            pub_cmd.publish(msg)
            print("Moving to Point 1...\n")
        elif service == "Point5":
            msg = "Point5"
            pub_cmd.publish(msg)
            print("Moving to Point 5...\n")
        elif service == "SetVac":
            msg = "SetVac"
            pub_cmd.publish(msg)
            print("Set Robot Tool0 (Vacuum)...\n")
        elif service == "ResetVac":
            msg = "ResetVac"
            pub_cmd.publish(msg)
            print("Reset Robot Tool0 (Vacuum)...\n")
        elif service == "PickingLoop":
            print("Starting picking loop...\n")
            start_order()
        else :
            print("ERROR: command not found \n")

        if rospy.is_shutdown():
            print("Stop Service")
            break
    return 0

if __name__ == "__main__":
    
    rospy.init_node('main_order', anonymous=True)
    listener = tf.TransformListener()
    pub_order = rospy.Publisher('main/yolo_order', String, queue_size=10)
    pub_target = rospy.Publisher('main/target_order', ObjectMsg, queue_size=10)
    pub_cmd = rospy.Publisher('main/cmd_talker', String, queue_size=10)
    try:
        start_service()
    except rospy.ROSInterruptException:
        pass