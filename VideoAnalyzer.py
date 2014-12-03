import threading
import cv2
from Constants import *

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

class VideoAnalyzer(threading.Thread):
    def __init__(self, synth):
        super(VideoAnalyzer, self).__init__()
        # Attach connection to synth
        self.synth = synth
        # Open Webcam 
        self.camera = cv2.VideoCapture(1)

    def run(self):
        # Check camera
        if not self.camera.isOpened():
            print "No camera"
        else: # Begin main loop
            print "Starting Camera"
            while True:
                # Get Frames for each color
                frames = self.get_frames()

                #
                gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
                r,gray = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
                frames[5] = gray

                # Show each frame in a window
                #cv2.imshow('Framer', frames[1])
                #cv2.imshow('Frameg', frames[2])
                #cv2.imshow('Frameb', frames[3])
                #cv2.imshow('Framey', frames[4])
                cv2.imshow('Framew', frames[5])
                
                # Get list of shapes found
                shapes = self.extract_shapes(frames)
                # Update synth board
                self.synth.shape2board(shapes)
                
                # Draw and Show shapes in image for debugging
                frames[0] = self.draw_shapes(frames[0], shapes)
                cv2.imshow('Frame', frames[0])                

                # Check if key 'q' is pressed, if so exit
                if(cv2.waitKey(20)&0xFF == ord('q')):
                    break
            
            # Done with loop, release camera and close windows
            self.camera.release()
            cv2.destroyAllWindows()


    """
    get_frames:
    Returns a list of binary images masked by each color
    """
    def get_frames(self):
        # Read frame from camera
        ret, frame1 = self.camera.read()
        # Blur image to remove noise
        frame1 = cv2.blur(frame1, (3,3))
        # Convert to HSV color space for color detection
        frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        # Change to binary image based on color
        frame_red = cv2.inRange(frame2, LOWER_RED, HIGHER_RED)
        frame_red = frame_red | cv2.inRange(frame2, LOWER_RED2, HIGHER_RED2)
        frame_blue = cv2.inRange(frame2, LOWER_BLUE, HIGHER_BLUE)
        frame_green = cv2.inRange(frame2, LOWER_GREEN, HIGHER_GREEN)
        frame_yellow = cv2.inRange(frame2, LOWER_YELLOW, HIGHER_YELLOW)
        frame_white = cv2.inRange(frame2, LOWER_WHITE, HIGHER_WHITE)
        return [frame1, frame_red, frame_green, frame_blue, frame_yellow, frame_white]

    """
    draw_shapes:
    Draws the shapes found on an image

    params:
    frame: the image to draw the shapes on
    shapes: the list of shapes to draw

    return:
    a new image with the shapes drawn
    """
    def draw_shapes(self, frame, shapes):
        for s in shapes:
            # Draw circle on frame
            if(s[0] == CIRCLE):
                x = int(s[2]*WORKSPACE_SIZE[0])
                y = int(s[3]*WORKSPACE_SIZE[1])
                r = int(s[4]*WORKSPACE_SIZE[2])
                thickness = 2
                cv2.circle(frame, (x, y), r, GREEN_RGB, thickness)
            elif s[0] in [SQUARE, TRIANGLE, STAR]:
                cnt = s[2]
                cnt[:, 0] = cnt[:, 0]*WORKSPACE_SIZE[0]
                cnt[:, 1] = cnt[:, 1]*WORKSPACE_SIZE[1]
                cnt = cnt.astype(int)
                thickness = 2
                cv2.drawContours(frame, [cnt], 0, RED_RGB, thickness)

        return frame

    """
    find_circles:
    Finds circles in an image and returns a list of them

    params:
    frame: the image to find shapes in
    color: the color that this shape will be identified as in the shapes list

    return:
    a list of shapes of the circles where each element is of the form 
    [CIRCLE, color, x, y, radius]
    """
    def find_circles(self, frame, color):
        # Circle should be atleast 1/10 of the screen apart
        minDist = frame.shape[1]*0.1
        # Circles should be 1/16 of the screen
        minDiam = int(frame.shape[1]*(1.0/16.0))
        minRadius = minDiam/2;
        # Circles should be as big as 1/8 of the screen
        maxDiam = int(frame.shape[1]*(1.0/8.0))
        maxRadius = maxDiam/2;
        # Accumulator matric resolution
        #dp = 1.35
        dp = 1.7
        # Get (radius, x, y) of circles
        c = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 
                             dp=dp, 
                             minDist=minDist, 
                             #minRadius=minRadius, 
                             #maxRadius=maxRadius
                             )
        if c == None:
            return []
        struct = []
        # Convert to the format that the other functions/synth needs
        # Normalize the values to 0-1 (easier to work with)
        for i in c[0,:]:
            if i[2] > WORKSPACE_SIZE[0]*0.25:
                continue
            struct.append([CIRCLE, color, 
                           i[0]/WORKSPACE_SIZE[0], 
                           i[1]/WORKSPACE_SIZE[1],
                           i[2]/WORKSPACE_SIZE[2]])
        return struct

    # Adapted from opencv example squares.py
    """
    find_squares:
    Returns a list of squares found in the image

    params:
    frame: the image to find the squares in
    color: the color that squares will be identified as in the list of shapes

    return:
    a list of squares found where each element will be of the form
    [SQUARE, color, points]
    """
    def find_squares(self, frame, color):
        minArea = 10*10 # Minimum area required for sqaure
        maxArea = WORKSPACE_SIZE[0]*WORKSPACE_SIZE[1]*0.25 # Maximum area of square
        squares = [] # list of squares that will be returns
        # Find contour in binary image
        frame, contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # Iterate through each contour and add the ones that appear to be
        # legitimate squares
        for cnt in contours:
            # Get contour points
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)

            if (len(cnt) == 4 and # Squares should have 4 points
               minArea < cv2.contourArea(cnt) and  # Make sure the size is appropriate
               cv2.contourArea(cnt) < maxArea and 
               cv2.isContourConvex(cnt)):
                cnt = cnt.reshape(-1, 2)
                # Normalize points between 0-1
                cnt = cnt.astype(float) # Convert to float
                cnt[:, 0] = cnt[:, 0]/WORKSPACE_SIZE[0]
                cnt[:, 1] = cnt[:, 1]/WORKSPACE_SIZE[1]
                # Add to list
                squares.append([SQUARE, color, cnt])
        return squares

    """
    find_triangles:
    Returns a list of triangles found in the image

    params:
    frame: the image to find the triangles in
    color: the color that triangles will be identified as in the list of shapes

    return:
    a list of triangles found where each element will be of the form
    [TRIANGLE, color, points]
    """
    def find_triangles(self, frame, color):
        minArea = 0.5*30*30
        maxArea = WORKSPACE_SIZE[0]*WORKSPACE_SIZE[1]*0.25
        triangles = []
        frame, contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if (len(cnt) == 3 and 
               minArea < cv2.contourArea(cnt) and 
               cv2.contourArea(cnt) < maxArea and 
               cv2.isContourConvex(cnt)):
                cnt = cnt.reshape(-1, 2)
                cnt = cnt.astype(float)
                cnt[:, 0] = cnt[:, 0]/WORKSPACE_SIZE[0]
                cnt[:, 1] = cnt[:, 1]/WORKSPACE_SIZE[1]
                triangles.append([TRIANGLE, color, cnt])
        return triangles

    """
    find_stars:
    Returns a list of stars found in the image

    params:
    frame: the image to find the stars in
    color: the color that stars will be identified as in the list of shapes

    return:
    a list of stars found where each element will be of the form
    [STAR, color, points]
    """
    def find_stars(self, frame, color):
        minArea = 50
        maxArea = WORKSPACE_SIZE[0]*WORKSPACE_SIZE[1]*0.25
        stars = []
        frame, contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if (len(cnt) == 10 and 
               minArea < cv2.contourArea(cnt) and 
               cv2.contourArea(cnt) < maxArea):
                cnt = cnt.reshape(-1, 2)
                # Normalize
                cnt = cnt.astype(float)
                cnt[:, 0] = cnt[:, 0]/WORKSPACE_SIZE[0]
                cnt[:, 1] = cnt[:, 1]/WORKSPACE_SIZE[1]
                stars.append([STAR, color, cnt])
        return stars

    def extract_shapes(self, frames):
        # list of shapes that will be returns
        shapes = []
        # Red Circles Frame
        shapes.extend(self.find_circles(frames[5], RED))
        # Green __ Frame
        shapes.extend(self.find_squares(frames[5], GREEN))
        # BLue __ Frame
        shapes.extend(self.find_triangles(frames[5], BLUE))
        # Yellow __ Frame
        shapes.extend(self.find_stars(frames[5], YELLOW))
        return shapes