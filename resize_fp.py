"""
 display_fp.py
 
 Dirk Reese
 03/11/2018

 Asks for floorplan file and displays it

"""
 
import pygame
import numpy as np
from random import randint
from twodmath.twodmath import *
from twodmath.constants import *

BOARDER = 10

#print(randint(0, 9))

scr_center = [SCR_WIDTH/2 - 1, SCR_HEIGHT/2 - 1]

filename, ext, fp_data = read_fp_file()

fp_minx = min(fp_data, key = lambda t: t[0])[0]
fp_maxx = max(fp_data, key = lambda t: t[0])[0]
fp_miny = min(fp_data, key = lambda t: t[1])[1]
fp_maxy = max(fp_data, key = lambda t: t[1])[1]

fp_width = fp_maxx - fp_minx
fp_height = fp_maxy - fp_miny

fp_center = [int(fp_minx + fp_width/2), int(fp_miny + fp_height/2)]
scale_xy = [(SCR_WIDTH - BOARDER*2)/fp_width, (SCR_HEIGHT - BOARDER*2)/fp_height]

fp_scale = min(scale_xy)

pfp_data = get_pvect(fp_data, fp_center)

for i in pfp_data:
    i[0] = i[0]*fp_scale

scaled_fp_data = pvect2cvect(pfp_data, scr_center)

scaled_fp_data_00 = translate_array(scaled_fp_data, [(-1)*scr_center[0], (-1)*scr_center[1]])

np.savetxt(filename + "_fullsize_00" + ext, scaled_fp_data_00, fmt='%5.2f')

pygame.init()

# Set the width and height of the screen [width, height]
size = (SCR_WIDTH, SCR_HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Line comparison, log 10 slopes")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# --- Drawing code should go here

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # Set the screen background
    screen.fill(BLACK)

#    for i in range(len(new_data)):
#        pygame.draw.circle(screen, WHITE, new_data[i].astype(int), 1, 0)

    pygame.draw.lines(screen, WHITE, True, scaled_fp_data, 1)
#    pygame.draw.lines(screen, WHITE, True, new_data, 1)

# --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
    
