from styx_msgs.msg import TrafficLight
import numpy as np
import cv2

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        pass

    def get_classification(self, image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv::Mat): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """
        #set the default state as UNKNOWN
        state = TrafficLight.UNKNOWN

        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        red1 = cv2.inRange(img_hsv, lower_red , upper_red)

        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        red2 = cv2.inRange(img_hsv, lower_red , upper_red)

        red_converted_img = cv2.addWeighted(red1, 1.0, red2, 1.0, 0.0)


        lower_green = np.array([50,50,50])
        upper_green = np.array([70,255,255])
        green_converted_img = cv2.inRange(img_hsv, lower_green, upper_green)


        lower_yellow = np.array([20,50,50])
        upper_yellow = np.array([40,255,255])
        yellow_converted_img = cv2.inRange(img_hsv, lower_yellow, upper_yellow)


        red_blur_img = cv2.GaussianBlur(red_converted_img,(15,15),0)
        green_blur_img = cv2.GaussianBlur(green_converted_img,(15,15),0)
        yellow_blur_img = cv2.GaussianBlur(yellow_converted_img,(15,15),0)


        # Finds circles in a grayscale image using the Hough transform
        # https://docs.opencv.org/2.4/modules/imgproc/doc/feature_detection.html#houghcircles
        red_circles = cv2.HoughCircles(red_blur_img,cv2.HOUGH_GRADIENT,0.5,41, param1=70,param2=30,minRadius=5,maxRadius=150)
        green_circles = cv2.HoughCircles(green_blur_img,cv2.HOUGH_GRADIENT,0.5,41, param1=70,param2=30,minRadius=5,maxRadius=150)
        yellow_circles = cv2.HoughCircles(yellow_blur_img,cv2.HOUGH_GRADIENT,0.5,41, param1=70,param2=30,minRadius=5,maxRadius=150)


        if red_circles is not None:
            state = TrafficLight.RED
        elif green_circles is not None:
            state = TrafficLight.GREEN
        elif yellow_circles is not None:
            state = TrafficLight.YELLOW
        else:
            state = TrafficLight.UNKNOWN

        return state