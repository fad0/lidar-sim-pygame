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
#print(randint(0, 9))

scr_center = [SCR_WIDTH/2 - 1, SCR_HEIGHT/2 - 1]

file_name = input("Input file name: ")

fp_data = np.loadtxt(file_name)

origin = input("Is the floorplan file based on (0, 0) center? (y or n) : ")
if origin == 'y' or origin == 'Y':
    print("Translating fp data")
    fp_data = translate_array(fp_data, scr_center)

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

    pygame.draw.lines(screen, WHITE, True, fp_data, 1)
#    pygame.draw.lines(screen, WHITE, True, new_data, 1)

# --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
    
