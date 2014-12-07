from Viewer import Viewer
from VideoAnalyzer import VideoAnalyzer
from Constants import *
import time, pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'      # Set the window in the center

vw = Viewer()
va = VideoAnalyzer(vw)

vw.start()
va.start()