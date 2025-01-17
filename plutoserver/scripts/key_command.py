#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import Char,Int16

import sys, select, termios, tty

msg = """
Control Your Drone!
---------------------------
Moving around:
   u    i    o
   j    k    l
   n    m    ,


a : Arm drone
d : Dis-arm drone
r : stop smoothly
w : increase height
s : increase height

CTRL-C to quit
"""

"""
Function Name: getKey
Input: None
Output: keyboard charecter pressed
Logic: Determine the keyboard key pressed
Example call: getkey()
"""
def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        sys.stdin.flush()
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('simple_drone_teleop_key')
    pub = rospy.Publisher('/input_key',Int16, queue_size=1) #publish the key pressed on topic /imput_key
    rate=rospy.Rate(100) # ncreased the rate 
    msg_pub=0 # by default valuse should be 0
    keyboard_control={  #dictionary containing the key pressed abd value associated with it
                      'i': 10,
                      'k': 20,
                      'j': 30,
                      'l': 40,
                      'd':0, 
                      'w':50,
                      's':60,
                      'a':70,
                      'r':80,
                      't':90,
                      'p':100,
                      'm':110,
                      'n':120,
                      '+' : 15,
                      '1' : 25,
                      '2' : 30,
                      '3' : 35,
                      '4' : 45}

    control_to_change_value=('u','o',',','z','c') #tuple containing the key that change the value

    try:
        pass
        while not rospy.is_shutdown():
          key = getKey()                          # get the key from keyboard
          #print key
          if (key == '\x03'):                     # to handle ctrl+c 
            break
          if key in keyboard_control.keys():
            msg_pub=keyboard_control[key]         #Map the key with dictionary for valid value
            #print msg_pub
            pub.publish(msg_pub)                  # publish the corresponding value of key
          else:
            msg_pub=80                            #If key is not pressed published the reset value to hover at point
            pub.publish(msg_pub)
          if key in control_to_change_value:      #Other than main control (Optional)
            print "control_value"
            rate.sleep()
    except Exception as e:
        print e
    finally:
        print key
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
