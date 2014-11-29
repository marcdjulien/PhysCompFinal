import threading
import cv2
from Constants import *

class VideoAnalyzer(threading.Thread):
    def __init__(self, synth):
        super(VideoAnalyzer, self).__init__()
        self.synth = synth
        self.capture = cv2.VideoCapture(0)

    def run(self):
        # Check camera
        if not self.capture.isOpened():
            print "No camera"
        # Begin main loop
        else:
            print "Starting Camera"
            while True:
                frames = self.get_frames()
                #cv2.imshow('Framer', frames[1])
                #cv2.imshow('Frameg', frames[2])
                #cv2.imshow('Frameb', frames[3])
                #cv2.imshow('Framey', frames[4])
                shapes = self.extract_shapes(frames)
                frames[0] = self.draw_shapes(frames[0], shapes)
                self.synth.shape2board(shapes)

                cv2.imshow('Frame', frames[0])

                # update synth board
                if(cv2.waitKey(20)&0xFF == ord('q')):
                    break
            self.capture.release()
            cv2.destroyAllWindows()

    def get_frames(self):
        ret, frame1 = self.capture.read()
        frame1 = cv2.blur(frame1, (11,11))
        #frame1 = cv2.resize(frame1, (frame1.shape[1]/4,frame1.shape[0]/4), interpolation = cv2.INTER_CUBIC)
        frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        frame_red = cv2.inRange(frame2, LOWER_RED, HIGHER_RED)
        frame_red = frame_red | cv2.inRange(frame2, LOWER_RED2, HIGHER_RED2)
        frame_blue = cv2.inRange(frame2, LOWER_BLUE, HIGHER_BLUE)
        frame_green = cv2.inRange(frame2, LOWER_GREEN, HIGHER_GREEN)
        frame_yellow = cv2.inRange(frame2, LOWER_YELLOW, HIGHER_YELLOW)
        return [frame1, frame_red, frame_green, frame_blue, frame_yellow]

    def draw_shapes(self, frame, shapes):
        for s in shapes:
            if(s[0] == CIRCLE):
                cv2.circle(frame,
                           (int(s[2]*WORKSPACE_SIZE[0]), int(s[3]*WORKSPACE_SIZE[1])),
                           int(s[4]*WORKSPACE_SIZE[2]),
                           (255,255,0),
                           2)

        return frame

    def find_circles(self, frame, color):
        FACTOR = 0.5
        minDist = frame.shape[1]*FACTOR
        minDiam = int(frame.shape[1]*0.1)
        minRadius = minDiam/2;
        maxDiam = int(frame.shape[1]*0.9)
        maxRadius = maxDiam/2;
        dp = 2.0
        c = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 
                             dp=dp, minDist=minDist, minRadius=minRadius, maxRadius=maxRadius)
        if c == None:
            return []
        struct = []
        for i in c[0,:]:
            struct.append([CIRCLE, color, 
                           i[0]/WORKSPACE_SIZE[0], 
                           i[1]/WORKSPACE_SIZE[1],
                           i[2]/WORKSPACE_SIZE[2]])
        return struct

    def find_squares(self, frame, color):
        FACTOR = 0.5
        minDist = frame.shape[1]*FACTOR
        minDiam = int(frame.shape[1]*0.1)
        minRadius = minDiam/2;
        maxDiam = int(frame.shape[1]*0.9)
        maxRadius = maxDiam/2;
        dp = 5
        c = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 
                             dp=dp, minDist=minDist, minRadius=minRadius, maxRadius=maxRadius)
        if c == None:
            return []
        struct = []
        for i in c[0,:]:
            struct.append([SQUARE, color, 
                           i[0]/WORKSPACE_SIZE[0], 
                           i[1]/WORKSPACE_SIZE[1],
                           i[2]/WORKSPACE_SIZE[2]])
        return struct
    def extract_shapes(self, frames):
        shapes = []
        # Red Circles Frame
        shapes.extend(self.find_circles(frames[1], RED))
        # Green __ Frame
        shapes.extend(self.find_squares(frames[2], GREEN))
        # BLue __ Frame
        shapes.extend(self.find_squares(frames[3], BLUE))
        # Yellow __ Frame
        shapes.extend(self.find_circles(frames[4], YELLOW))
        return shapes