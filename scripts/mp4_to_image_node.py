#!/usr/bin/env python3

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import sys

def mp4_to_image_publisher():
    rospy.init_node('mp4_to_image_publisher', anonymous=True)
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        rospy.logerr("Usage: rosrun mp4_to_image mp4_to_image_node.py [-l] <video_file> <image_topic>")
        sys.exit(1)
    
    loop_play = False
    video_file = sys.argv[2]
    pub_topic = sys.argv[-1]
    
    if len(sys.argv) == 4 and sys.argv[1] == "-l":
        loop_play = True

    pub = rospy.Publisher(pub_topic, Image, queue_size=10)
    rate = rospy.Rate(30)  # 30 Hz

    cap = cv2.VideoCapture(video_file)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            if loop_play:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_msg = bridge.cv2_to_imgmsg(frame, encoding="rgb8")
        pub.publish(image_msg)
        rate.sleep()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        mp4_to_image_publisher()
    except rospy.ROSInterruptException:
        pass

