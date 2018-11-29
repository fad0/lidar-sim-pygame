"""
File: gen_mavg_bavg.py

Copied from gen_centered_fp.py

For each segment, find slope m and y-intercept b.
Find average slope mavg and average y-int bavg for AVG_SAMPLE_LENGTH.

Dirk Reese
25/11/2018

"""
 
import pygame
import numpy as np
from twodmath.twodmath import *
import os

#####  LOAD CONSTANTS  #####
from twodmath.constants import *
#####  END LOAD CONSTANTS  #####

np.set_printoptions(precision=3)

#### Read in scan file assuming cartesian coordinates #####
filename, ext, fp_data = read_fp_file()
print(" ")


# Find the sFP segment slopes, lengths, and angle variance.
fp_data_m = find_slopes(fp_data)
fp_data_sl = find_seg_len(fp_data)
fp_data_v = find_ang_var(fp_data_m)

print("fp_data_m = ", fp_data_m)
print("fp_data_sl = ", fp_data_sl)
print("fp_data_v = ", fp_data_v)
print(" ")

rot_angle_deg = int(input("Input Bot Rotation in degrees: "))
rotation_angle = np.deg2rad(rot_angle_deg)
print(" ")

bot_x = int(input("Input bot x relative to center of floorplan: "))
bot_y = int(input("Input bot y relative to center of floorplan: "))

##### Read number of samples to be taken #####
samples = int(input("Input number of samples: "))
sample_ang = 2*np.pi/samples   ### 1 degree

# Array of simulated LIDAR sample points.  Determining this array
# is the goal of this program.
#sample_points = []      # Cartesian
psample_points = []     # Polar

# set sample counter to 0
sample_cntr = 0

bot_arrow = [[ 0, 0],
             [15, 0]]

bot_loc = [int(SCR_WIDTH/2 + bot_x - 1), int(SCR_HEIGHT/2 + bot_y - 1)] 
bot_home = [int(SCR_WIDTH/2 - 1), int(SCR_HEIGHT/2 - 1)] 

xfrmd_array = translate_array(fp_data, (bot_home))

xfrmd_bot_arrow = translate_array(bot_arrow, (bot_loc))
xfrmd_bot_arrow = rotate_array(xfrmd_bot_arrow, (bot_loc), (-1)*rotation_angle)

#np.savetxt(filename + "_trans" + ext, translated_arr, fmt='%3.3f')

pygame.init()

# Set the width and height of the screen [width, height]
size = (SCR_WIDTH, SCR_HEIGHT)
screen = pygame.display.set_mode(size)
s = pygame.Surface(size)

# Window Name
pygame.display.set_caption("Simple FP rotation")

# Text setup
font = pygame.font.Font(None, 16)
#input_box = pygame.Rect(100, 100, 140, 32)
color_active = pygame.Color('lightskyblue3')
#color_inactive = pygame.Color('dodgerblue2')
color = color_active
#text = 'Hello World!'
#txt = font.render(text, True, color)
#txt_surface = pygame.transform.rotate(txt, 270)
## Blit the text.
#screen.blit(txt_surface, (599, 349))

#background color
s.fill((30,30,30))

#blit myNewSurface onto the main screen at the position (0, 0)
screen.blit(s, (0, 0))

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# --- display toggles --- #
display_floorplan = True
display_floorplan_num = True
display_lidar = True
display_endpoints = True
display_mavg = True

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
#            print("trans_x = ", trans_x,"   trans_y = ", trans_y)
#            if event.key == pygame.K_PERIOD:
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("event.button = ", event.button)
            # --- Game logic should go here
            pos = pygame.mouse.get_pos()
            rect_x = pos[0]
            rect_y = pos[1]
            print("mouse position = ", rect_x,"  ", rect_y)
            print("bot position = ", rect_x - SCR_WIDTH/2 - 1,"  ", rect_y - SCR_HEIGHT/2 - 1)
            psample_points = []     # Polar
            # set sample counter to 0
            sample_cntr = 0

            bot_loc = [rect_x, rect_y]

            # Translate and Rotate bot arrow

            xfrmd_bot_arrow = translate_array(bot_arrow, (bot_loc))
            xfrmd_bot_arrow = rotate_array(xfrmd_bot_arrow, (bot_loc), (-1)*rotation_angle)
            display_floorplan = True
            display_floorplan_num = False
#            display_lidar = False
#            display_endpoints = False
#            display_mavg = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                display_floorplan = not display_floorplan
            if event.key == pygame.K_n:
                display_floorplan_num = not display_floorplan_num
            if event.key == pygame.K_l:
                display_lidar = not display_lidar
            if event.key == pygame.K_e:
                display_endpoints = not display_endpoints
            if event.key == pygame.K_m:
                display_mavg = not display_mavg

    # Set the screen background
    screen.fill((30,30,30))

    # Draw simple trapezoid room from lines
#    pygame.draw.lines(screen, WHITE, True, fp_data, 3)
#    pygame.draw.lines(screen, BLUE, True, relative_fp_data, 3)
#    pygame.draw.lines(screen, WHITE, True, TRANSLATE_ARRAY, 1)

#    if (len(sample_points) >= samples):
#        for i in range(len(sp_separation)):
#            pygame.draw.line(screen, WHITE, [50 + i*2,  50], [50 + i*2, 50 + sp_separation[i]], 2)
#            pygame.draw.line(screen, WHITE, [50 + i*2, 300], [50 + i*2, 300 + sp_chg_sep[i]], 2)
#            pygame.draw.line(screen, WHITE, [50 + i*2, 50], [50 + i*2, 50 + sp_mavg[i]], 2)
#            pygame.draw.line(screen, WHITE, [50 + i*2, 400], [50 + i*2, 400 + sp_bavg[i]/100], 2)


    #### Draw the FP in GREEN ####
    if display_floorplan == True:
        pygame.draw.lines(screen, GREEN, True, xfrmd_array, 3)
#        for i in range(len(xfrmd_array)):
#            i_mod = (i + 1) % len(xfrmd_array)
#            pygame.draw.line(screen, GREEN, xfrmd_array[i_mod], xfrmd_array[i], 3)
#            print("Redrawing GREEN FP")
#            text = str(i).encode("utf-8").decode("utf-8")
#            txt = font.render(text, True, WHITE)
#            txt_surface = pygame.transform.rotate(txt, 270)
#            # Blit the text.
#            screen.blit(txt_surface, xfrmd_array[i])

    #### Draw the FP in GREEN ####
    if display_floorplan_num == True:
        for i in range(len(xfrmd_array)):
            i_mod = (i + 1) % len(xfrmd_array)
#            pygame.draw.line(screen, GREEN, xfrmd_array[i_mod], xfrmd_array[i], 3)
#            print("Redrawing GREEN FP")
            text = str(i).encode("utf-8").decode("utf-8")
            txt = font.render(text, True, WHITE)
            txt_surface = pygame.transform.rotate(txt, 270)
            # Blit the text.
            screen.blit(txt_surface, xfrmd_array[i])

    if sample_cntr == samples:
        # Draw the simulated LIDAR scan
        if display_endpoints == True:
            dis_ep_cntr=0
            for i in endpoints:
                pygame.draw.line(screen, RED, i[0], i[1], 2)
                text = str(dis_ep_cntr).encode("utf-8").decode("utf-8")
                txt = font.render(text, True, color)
                txt_surface = pygame.transform.rotate(txt, 270)
                # Blit the text.
                screen.blit(txt_surface, i[0])
                dis_ep_cntr += 1

        # Draw the extracted lines from endpoints
        if display_lidar == True:
            for i in sample_points:
                pygame.draw.line(screen, RED, bot_loc, i, 1)

        # Draw mavg extracted segments
        if display_mavg == True:
            dis_mavg_cntr=0
            for i in mavg_seg_ep:
                pygame.draw.line(screen, YELLOW, i[0], i[1], 2)
                text = str(dis_mavg_cntr).encode("utf-8").decode("utf-8")
                txt = font.render(text, True, color)
                txt_surface = pygame.transform.rotate(txt, 270)
                # Blit the text.
                screen.blit(txt_surface, i[0])
                dis_mavg_cntr += 1

    pygame.draw.circle(screen, WHITE, bot_home, 10, 2)
    pygame.draw.line(screen, WHITE, bot_home, [bot_home[0] + 15, bot_home[1]], 3)

    pygame.draw.circle(screen, BLUE, [int(xfrmd_bot_arrow[0][0]), int(xfrmd_bot_arrow[0][1])], 10, 0) 
    pygame.draw.line(screen, BLUE, xfrmd_bot_arrow[0], xfrmd_bot_arrow[1], 3)


    # Copy the screen to s so get_at can get pixal colors
    s = pygame.Surface.copy(screen)
    screen.blit(s, (0, 0))

    # Draw radial lines, simulating LIDAR, to find the wall sample points
    # and append them to sample_points array
    while sample_cntr < samples:
        i=1
        while True:
            theta = sample_ang*sample_cntr
            x_comp = bot_loc[0] + i*np.cos(theta)
            ix_comp = int(x_comp)
            y_comp = bot_loc[1] + i*np.sin(theta)
            iy_comp = int(y_comp)
#            print("x_comp, y_comp = ", x_comp,"  ",y_comp)
            if (s.get_at((ix_comp, iy_comp))[:3] != GREEN):
#                print("s.get_at = ", s.get_at((ix_comp, iy_comp))[:3])
                i += 1
            else:
#                print("s.get_at = ", s.get_at((ix_comp, iy_comp))[:3])
                radius = get_distance(bot_loc, [x_comp, y_comp])
                psample_points.append([radius, theta])
#                print("sample_points = ", sample_points)
                break
        sample_cntr += 1
        if sample_cntr == samples:
            sample_points = pvect2cvect(psample_points, bot_loc)
            np.savetxt(filename + "_" + str(samples) + "sp_cart" + ext, sample_points, fmt='%4f')
            np.savetxt(filename + "_" + str(samples) + "sp_polar" + ext, psample_points, fmt='%6f')

            ##### Find distance between sample points #####

            sp_separation = np.array([])
            for i in range(len(sample_points)):
                i_mod = ((i + 1) % len(sample_points))  #  This enables wrap around
                sp_separation = np.append(sp_separation, get_distance(sample_points[i_mod], sample_points[i]))
            print("sp_separation = ", sp_separation)


            ##### Find the change in distance between sample points #####

            sp_chg_sep = np.array([])
            for i in range(len(sp_separation)):
                i_mod = ((i + 1) % len(sp_separation))  #  This enables wrap around
                sp_chg_sep = np.append(sp_chg_sep, sp_separation[i_mod] - sp_separation[i])
            print("sp_chg_sep = ", sp_chg_sep)


            ##### Calculate slope angles and y-intercepts #####

            m_array = find_slopes(sample_points)

#            b_array = find_y_intercept(sample_points, m_array)

            print("m_array = ", m_array)
            print(" ")
#            print("b_array = ", b_array)


            ##### Find mavg and bavg ####

            sp_xyavg = np.zeros(shape=(len(sample_points), 2))
            sp_mavg = np.empty(len(m_array))
            sp_bavg = np.empty(len(m_array))
            m_ext = np.append(m_array, m_array[:AVG_SAMPLE_LENGTH])
            xy_ext = np.append(sample_points, sample_points[:AVG_SAMPLE_LENGTH], axis=0)
#            print("sample_points = ", sample_points)
#            print("sp_xyavg = ", sp_xyavg)
#            print("xy_ext = ", xy_ext)
#            b_ext = np.append(b_array, b_array[:AVG_SAMPLE_LENGTH])
            for i in range(len(m_array)):
                sp_mavg[i] = np.average(m_ext[i:i + AVG_SAMPLE_LENGTH])
                sp_xyavg[i] = np.average(xy_ext[i:i + AVG_SAMPLE_LENGTH], axis=0)
                sp_bavg[i] = sp_xyavg[i][1] - sp_mavg[i]*sp_xyavg[i][0]
#                print("i = ", i,"   i_mod = ", i_mod)

            print("sp_mavg = ", sp_mavg)
            print(" ")
            print("sp_xyavg = ", sp_xyavg)
            print("sp_bavg = ", sp_bavg)


            stable_sp_mavg = []
            mavg_cntr = 0
            i=0
            while i < len(sp_mavg) :
                index = (i + mavg_cntr + 1) % len(sp_mavg)
                while ((abs(sp_mavg[index] - sp_mavg[i]) <= abs(sp_mavg[i]*ASLOPE_ERR_TOLERANCE)) \
                      and sp_separation[index] <= MAX_SP_SEPARATION) or abs(sp_mavg[index]) < MAVG_MIN:
                    print("sp_separation[",index,"] = ", sp_separation[index])
                    mavg_cntr += 1
                    index = (i + mavg_cntr + 1) % len(sp_mavg)
                    print("i = ", i,"   mavg_cntr = ", mavg_cntr,"  index = ", index)
                if mavg_cntr > MIN_WEIGHT:
                    stable_sp_mavg.append([sp_mavg[i], i, mavg_cntr])
                    if i + mavg_cntr + 1 < len(sp_mavg):
                        i = index
                        mavg_cntr = 0
                    else:
                        i = len(sp_mavg)
                else:
                    mavg_cntr = 0
                    i += 1

            for i in stable_sp_mavg:
                print("stable_sp_mavg = ", i)

            mavg_seg_ep = []
            for i in range(len(stable_sp_mavg)):
                index = stable_sp_mavg[i][1]
                m_span = stable_sp_mavg[i][2]
                m_index = (index + m_span) % len(sp_mavg)
#                mavg_seg_ep.append([sp_xyavg[index], sp_xyavg[m_index]])
                mavg_seg_ep.append([sp_xyavg[index], sample_points[m_index]])
                print("index = ", index,"   m_span = ", m_span,"   m_index = ", m_index,"   sp_xyavg[index] = ",
                      sp_xyavg[index],"   sample_points[m_index] = ", sample_points[m_index])
            for i in mavg_seg_ep:
                print("mavg_seg_ep = ", i)

#            stable_sp_bavg = []
#            bavg_cntr = 0
#            i=0
#            while i < len(sp_bavg) :
#                index = (i + bavg_cntr + 1) % len(sp_bavg)
#                while abs(sp_bavg[index] - sp_bavg[i]) <= abs(sp_bavg[i]*ASLOPE_ERR_TOLERANCE):
#                    bavg_cntr += 1
#                    index = (i + bavg_cntr + 1) % len(sp_bavg)
##                    print("i = ", i,"   bavg_cntr = ", bavg_cntr,"  index = ", index)
#                if bavg_cntr > MIN_WEIGHT:
#                    stable_sp_bavg.append([sp_bavg[i], i, bavg_cntr])
#                    if i + bavg_cntr + 1 < len(sp_bavg):
#                        i = index
#                        bavg_cntr = 0
#                    else:
#                        i = len(sp_bavg)
#                else:
#                    bavg_cntr = 0
#                    i += 1
#
#            for i in stable_sp_bavg:
#                print("stable_sp_bavg = ", i)


#            for i in range(len(sp_mavg)):
#                for j in range(len(sp_mavg)):
#                    index = (i + j) % len(sp_mavg)
#                    if (sp_mavg[i + j] - sp_mavg[i]) <= sp_mavg[i]*ASLOPE_ERR_TOLERANCE:
#                        mavg_cntr += 1
#                    elif mavg_cntr > MIN_WEIGHT:
#                        stable_sp_mavg.append([sp_mavg[i], i, mavg_cntr])
#                        mavg_cntr = 0
#                    else:
#                        mavg_cnt = 0
#
#            for i in stable_sp_mavg:
#                print("stable_sp_mavg = ", i)
#
#            stable_sp_bavg = []
#            bavg_cntr = 0
#            for i in range(len(sp_bavg)):
#                i_mod = (i + 1) % len(sp_bavg)
#                if (sp_bavg[i_mod] - sp_bavg[i]) <= sp_bavg[i]*ASLOPE_ERR_TOLERANCE:
#                   bavg_cntr += 1
#                elif bavg_cntr > MIN_WEIGHT:
#                    stable_sp_bavg.append([sp_bavg[i], i, bavg_cntr])
#                    bavg_cntr = 0
#                else:
#                    bavg_cnt = 0
#
#            for i in stable_sp_bavg:
#                print("stable_sp_bavg = ", i)

            ##### Find change in mavg and bavg #####

            diff_mavg = np.ediff1d(np.append(sp_mavg, sp_mavg[0]))
            diff_bavg = np.ediff1d(np.append(sp_bavg, sp_bavg[0]))

            print("diff_mavg = ", diff_mavg)
            print(" ")
            print("diff_bavg = ", diff_bavg)


            ##### Group adjacent points with similar slope angle #####

            m_group = find_m_groups(m_array)
            print("m_group = ", m_group)

            ##### Find the endpoints of the groups #####

            endpoints = find_lines(m_group, sample_points)

            for i in endpoints:
                print("endpoints = ", i[0],"   ",i[1])
            #    print("endpoints = ", i)

            ##### find and join adjacent lines with vary similar slopes #####

            m_endpoints = find_ep_slopes(endpoints)
            print("m_endpoints = ", m_endpoints)

            m_endpoints = merge_lines(endpoints, m_endpoints)
            for i in endpoints:
                print("endpoints = ", i[0],"   ",i[1])
            print("m_endpoints = ", m_endpoints)

            var_ep = find_ang_var(m_endpoints)
            print("var_ep = ",var_ep)

            sep_array = find_separation(endpoints)
            print("sep_array = ", sep_array)

            len_ep = find_ep_len(endpoints)
            print("len_ep = ", len_ep)

            for i in range(len(sep_array)):
                if sep_array[i] > 20:
                    if i < len(sep_array) - 1:
                        var_ep = np.insert(var_ep, i + 1, -10)
                        len_ep = np.insert(len_ep, i + 1, -10)
                    else:
                        var_ep = np.append(var_ep, -10)
                        len_ep = np.append(len_ep, -10)
            print("adjusted var_ep =", var_ep)
            print("adjusted len_ep =", len_ep)


#            common_var = find_max_common_var(fp_data_v, fp_data_sl, var_ep, len_ep)
#            print("common_var = ", common_var)
#
#    pygame.draw.lines(screen, GREEN, True,
#                      back_tr_bot_arr,
#                      3)
#    pygame.draw.circle(screen, GREEN, [int(bot_x + x_back_trans), int(bot_y + y_back_trans)], 10, 0)

#    pygame.draw.lines(screen, GREEN, True,
#                      back_rotated_arr,
#                      1)

    # Draw the rectangle
#    pygame.draw.rect(screen, WHITE, [rect_x - 9, rect_y - 9, 20, 20])
 
# --- Go ahead and update the screen with what we've drawn.
    pygame.display.update() #or  display.flip()
    pygame.display.flip()

    # --- Limit to FRAMERATE (60) frames per second
    clock.tick(FRAMERATE) 

# Close the window and quit.  
pygame.quit() 
