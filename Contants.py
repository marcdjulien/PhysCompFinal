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

STEPS = 16

VIEWER_FPS = 60
VIEWER_SIZE= (1000, 700)
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BOARD_X = 10
BOARD_Y = 10
UNIT_W = (VIEWER_SIZE[0]-(BOARD_X*2))/STEPS
UNIT_H = (VIEWER_SIZE[1]-(BOARD_Y*2))/STEPS

LOWER_BLUE = np.array([180*(135.0/360.0),   100, 100], dtype=np.uint8)
HIGHER_BLUE = np.array([180*(270.0/360.0),   255, 255], dtype=np.uint8)
LOWER_RED = np.array([180*(000.0/360.0),   100, 100], dtype=np.uint8)
HIGHER_RED = np.array([180*(30.0/360.0),   255, 255], dtype=np.uint8)
LOWER_YELLOW = np.array([180*/(40.0/360.0),   100, 100], dtype=np.uint8)
HIGHER_YELLOW = np.array([180*(70.0/360.0),   255, 255], dtype=np.uint8)
LOWER_GREEN = np.array([180*(90.0/360.0),   100, 100], dtype=np.uint8)
HIGHER_GREEN = np.array([180*(140.0/360.0),   255, 255], dtype=np.uint8)