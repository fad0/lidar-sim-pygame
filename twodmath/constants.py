'''
   All global constants for robot
'''

FRAMERATE = 60
# Define some colors
WHITE =  (255, 255, 255)
BLACK =  (  0,   0,   0)
RED    = (255,   0,   0)
GREEN =  (  0, 255,   0)
BLUE = (  0,   0, 255)
YELLOW = (255, 255,   0)
PURPLE = (255,   0, 255)
CYAN = (  0, 250, 255)
COLORS = [ WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

# Define Screen width and height
SCR_WIDTH = 1200
SCR_HEIGHT = 700

# Floorplan scale
FPSCALE = 1

# Define sample point tolerances
SLOPE_ERR_TOLERANCE = 0.15
MIN_GROUP_SIZE = 2

ORIGIN = [0, 0]
ORIGIN_OFFSET = [350, 350]

# Number of averaged slope samples
AVG_SAMPLE_LENGTH = 10
# Slope error tolerance for slope averages
ASLOPE_ERR_TOLERANCE = 0.05
# Min run length of averaged slopes within ASLOPE_ERR_TOLERANCE
MIN_WEIGHT = 4
# Max allowed sp separation for slope averaging
# This actually should be dependent on distance from the bot (r-polar)
MAX_SP_SEPARATION = 20
# minimum running average slope for acceptable m stability
# for angles close to 0 because small variation may not 
# meet ASLOPE_ERR_TOLERANCE requirement
MAVG_MIN = 0.015
