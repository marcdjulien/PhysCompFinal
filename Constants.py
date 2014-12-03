import numpy as np
NOTE_TO_NUM = {"c":  4,
					 "c#": 5,
					 "d":  6,
					 "d#": 7,
					 "e":  8,
					 "f":  9,
					 "f#": 10,
					 "g":  11, 
					 "g#": 12,
					 "a":  1,
					 "a#": 2,
					 "b":  3}

NUM_TO_NOTE = {4:"c", 
					5:"c#",
					6: "d", 
					7:"d#",
					8: "e", 
					9: "f", 
					10:"f#", 
					11: "g",   
					12:"g#", 
					1: "a", 
					2:"a#",
					3: "b"}
BLANK = 0
SQUARE = 1
CIRCLE = 2
TRIANGLE = 3
STAR = 4

RED = 0
GREEN = 1
BLUE = 2
YELLOW = 3

STEPS = 8
NOTES = 12 

NOTE_ON = 0x90
NOTE_OFF = 0x80
MIDI_DEVICE_PERIOD = 0.01
MIDI_DEVICE_NAME = "LoopBe Internal MIDI"

NOTE_PERIOD = 0.3
SEQ_PERIOD = 0.5

VIEWER_FPS = 60
VIEWER_SIZE= [1000, 700]
WORKSPACE_SIZE = (640.0, 480.0, np.hypot(640, 480))
BLACK_RGB    = (   0,   0,   0)
WHITE_RGB    = ( 255, 255, 255)
BLUE_RGB     = (   0,   0, 255)
GREEN_RGB    = (   0, 255,   0)
RED_RGB      = ( 255,   0,   0)
ORANGE_RGB   = (255,  102,   0)
YELLOW_RGB   = (255,  255,   0)

BOARD_X = 10
BOARD_Y = 10
UNIT_W = (VIEWER_SIZE[0]-(BOARD_X*2))/STEPS
UNIT_H = (VIEWER_SIZE[1]-(BOARD_Y*2))/STEPS
MIN_BOX = 100
ROW_WIDTH = ((VIEWER_SIZE[1]/2)-(MIN_BOX/2))/STEPS

LOWER_BLUE    = np.array([180*(160/360.0),   200, 0], dtype=np.uint8)
HIGHER_BLUE   = np.array([180*(260.0/360.0), 255, 255], dtype=np.uint8)
LOWER_RED     = np.array([180*(0.0/360.0),   100, 0], dtype=np.uint8)
HIGHER_RED    = np.array([180*(30.0/360.0),  255, 255], dtype=np.uint8)
LOWER_RED2    = np.array([180*(330.0/360.0), 100, 0], dtype=np.uint8)
HIGHER_RED2   = np.array([180*(360.0/360.0), 255, 255], dtype=np.uint8)
LOWER_YELLOW  = np.array([180*(35.0/360.0),  100, 0], dtype=np.uint8)
HIGHER_YELLOW = np.array([180*(75.0/360.0),  255, 255], dtype=np.uint8)
LOWER_GREEN   = np.array([180*(80.0/360.0),  100, 0], dtype=np.uint8)
HIGHER_GREEN  = np.array([180*(140.0/360.0), 255, 255], dtype=np.uint8)
LOWER_WHITE   = np.array([180*(000.0/360.0),  0, 0], dtype=np.uint8)
HIGHER_WHITE  = np.array([180*(180.0/360.0), 100, 255], dtype=np.uint8)

PI = np.pi