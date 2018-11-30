"""
Defs for 2d graphic manipulation   

Dirk Reese
01/11/2018

"""
import pygame 
import numpy as np
import os

#####  LOAD CONSTANTS  #####
from twodmath.constants import *
#####  END LOAD CONSTANTS  #####

#### Read in scan file assuming cartesian coordinates #####

def read_fp_file():
    while True:
        fp_file = input("Input floorplan data: ")
        if not(os.path.isfile(fp_file)):
            print("Can't find ",fp_file,".  Try again.") 
        else:
            fp_file = os.path.realpath(fp_file)
            filename, ext = os.path.splitext(fp_file)
            fp_data = np.loadtxt(fp_file)
            break
    return(filename, ext, fp_data)


#####  TRANSLATION DEF  #####

def translate_array(inp_list, translation):
    trans_list = np.empty([len(inp_list), 2])
    for i in range(len(inp_list)):
        trans_list[i][0] = inp_list[i][0] + translation[0]
        trans_list[i][1] = inp_list[i][1] + translation[1]
    return trans_list

#####  TRANSLATION DEF END  #####


#####  ROTATION DEF #####

def rotate_array(inp_list, rotation_point, rotation_angle):
    rect_x = rotation_point[0]
    rect_y = rotation_point[1]
    rotate_list = np.empty([len(inp_list), 2])
    rvector     = np.empty([len(inp_list), 2])
    for i in range(len(inp_list)):
        # Check if input_list[i][0] equals rect_x, which will cause div by 0 error.
        # If yes, check input_list[i][1] is above or below rect_y.
        # If above, rvector[i][1] set to -pi/2, if below set to pi/2
        if inp_list[i][0] == rect_x:
            if inp_list[i][1] < rect_y:
                rvec_ang = -1*np.pi/2
            else:
                rvec_ang = np.pi/2
        else:
            rvec_ang = np.arctan((inp_list[i][1] - rect_y)/(inp_list[i][0] - rect_x))

        # Calculate vector magnitude and angle to each point with respect to point of rotation
        rvector[i]    = [np.sqrt((rect_x - inp_list[i][0])**2 + (rect_y - inp_list[i][1])**2),
                      rvec_ang]

        # arctan only give correct angle for x greater than x of rotation, if less than, need to add
        # pi.
        if inp_list[i][0] < rect_x:
            rvector[i][1] += np.pi

        rvector[i][1] += rotation_angle
        rotate_list[i] = [rvector[i][0]*np.cos(rvector[i][1]) + rect_x,
                            rvector[i][0]*np.sin(rvector[i][1]) + rect_y]
    return(rotate_list)

#####  ROTATION DEF END  #####

##### Calculate slope angle #####

def find_slopes(inp_list):
    if len(inp_list) == 2:
        m_array = np.empty(1)
    else:
        m_array = np.empty(len(inp_list))
    for i in range(len(inp_list) - 1):
        #if line is vertical, set slope to pi/2 or -pi/2
        if inp_list[i + 1][0] == inp_list[i][0]:
            if (inp_list[i + 1][1] > inp_list[i][1]):
                m_array[i] = np.pi/2
        #        m_array_deg[i] = 90
            else:
                m_array[i] = (-1)*np.pi/2
        #        m_array_deg[i] = -90
        elif inp_list[i + 1][1] == inp_list[i][1]:
            if inp_list[i + 1][0] > inp_list[i][0]:
                m_array[i] = 0
            else:
                m_array[i] = np.pi
        else:
            m_array[i] = np.arctan((inp_list[i + 1][1] - inp_list[i][1])/ \
                                   (inp_list[i + 1][0] - inp_list[i][0]))
            if (((inp_list[i + 1][1]) > (inp_list[i][1])) and (m_array[i] < 0)):
                m_array[i] = m_array[i] + np.pi
            elif (((inp_list[i + 1][1]) < (inp_list[i][1])) and (m_array[i] > 0)):
                m_array[i] = m_array[i] - np.pi
        #    m_array_deg[i] = np.rad2deg(m_array[i])

    ### Calculate slope between last and first sample point ###
    if len(inp_list) > 2:
        if inp_list[0][0] == inp_list[len(inp_list) - 1][0]:
            if inp_list[0][1] >= inp_list[len(inp_list) - 1][1]:
                m_array[len(inp_list) - 1] = np.pi/2
            #    m_array_deg[len(inp_list) - 1] = 90
            else:
                m_array[len(inp_list) - 1] = (-1)*np.pi/2
            #    m_array_deg[len(inp_list) - 1] = -90
        elif inp_list[0][1] == inp_list[len(inp_list) - 1][1]:
            if inp_list[0][0] >= inp_list[len(inp_list) - 1][0]:
                m_array[len(inp_list) - 1] = 0
            else:
                m_array[len(inp_list) - 1] = np.pi
        else:
            m_array[len(inp_list) - 1] = np.arctan((inp_list[0][1] - inp_list[len(inp_list) - 1][1])/ \
                                   (inp_list[0][0] - inp_list[len(inp_list) - 1][0]))
            if (((inp_list[0][1]) > (inp_list[len(inp_list) - 1][1])) and (m_array[len(inp_list) - 1] < 0)):
                m_array[len(inp_list) - 1] = m_array[len(inp_list) - 1] + np.pi
            elif (((inp_list[0][1]) < (inp_list[len(inp_list) - 1][1])) and (m_array[len(inp_list) - 1] > 0)):
                m_array[len(inp_list) - 1] = m_array[len(inp_list) - 1] - np.pi
            #m_array_deg[len(inp_list) - 1] = np.rad2deg(m_array[len(inp_list) - 1])

    return(m_array)

##### End Calculate slope angle #####

##### Calculate endpoints slope angle #####

def find_ep_slopes(endpoints):
    m_array = np.empty(len(endpoints))
    for i in range(len(endpoints)):
        #if line is vertical, set slope to pi/2 or -pi/2
        if endpoints[i][1][0] == endpoints[i][0][0]:
            if (endpoints[i][1][1] > endpoints[i][0][1]):
                m_array[i] = np.pi/2
        #        m_array_deg[i] = 90
            else:
                m_array[i] = (-1)*np.pi/2
        #        m_array_deg[i] = -90
        elif endpoints[i][1][1] == endpoints[i][0][1]:
            if endpoints[i][1][0] > endpoints[i][0][0]:
                m_array[i] = 0
            else:
                m_array[i] = np.pi
        else:
            m_array[i] = np.arctan((endpoints[i][1][1] - endpoints[i][0][1])/ \
                                   (endpoints[i][1][0] - endpoints[i][0][0]))
            if (((endpoints[i][1][1]) > (endpoints[i][0][1])) and (m_array[i] < 0)):
                m_array[i] = m_array[i] + np.pi
            elif (((endpoints[i][1][1]) < (endpoints[i][0][1])) and (m_array[i] > 0)):
                m_array[i] = m_array[i] - np.pi
        #    m_array_deg[i] = np.rad2deg(m_array[i])

    return(m_array)

##### End Calculate endpoints slope angle #####

##### Find Lines #####

def find_lines(m_group, sp_data):
    endpoints = []
    startpoint = [sp_data[0]]
    group=0
    group_size=0
    for i in range(len(m_group)):
        if (m_group[i] == group) :
            group_size += 1
        elif group_size < MIN_GROUP_SIZE:
    #        endpoints.append([new_data[i], new_data[i]])
            group += 1
            group_size = 0
        else:
            endpoints.append([sp_data[i - group_size - 1], sp_data[i]])
            group += 1
            group_size = 0
    
    return endpoints

##### END Find Lines #####


##### Merge adjacent lines on the same line #####
def merge_lines(endpoints, m_endpoints):
#    for i in range(len(endpoints) - 1):
    i = 0
    while True:
        if abs(m_endpoints[i + 1] - m_endpoints[i]) <= abs(m_endpoints[i]*SLOPE_ERR_TOLERANCE):
            gap_endpoints = [endpoints[i][1],endpoints[i + 1][0]]
            #print("m_endpoints[",i + 1,"] = ", m_endpoints[i + 1])
            #print("m_endpoints[",i,"] = ", m_endpoints[i])
            #print("gap_endpoints = ", gap_endpoints)
            gap_slope = find_slopes(gap_endpoints)
            #print("gap_slope = ", gap_slope)
            if abs(m_endpoints[i] - gap_slope) <= abs(m_endpoints[i]*SLOPE_ERR_TOLERANCE):
            #    print("2 gap_slope ",i," = ", gap_slope)
                endpoints[i][1] = endpoints[i + 1][1]
                del endpoints[i + 1]
                m_endpoints = np.delete(m_endpoints, [i + 1])
        i += 1
        if i > len(endpoints) - 1:
            i = len(endpoints) - 1
        if i >= len(endpoints) - 1:
            print("i = ",i)
            print("len(endpoints) - 1 = ", len(endpoints) - 1)
            print("len(m_endpoints) = ", len(m_endpoints))
            if abs(m_endpoints[0] - m_endpoints[i]) <= abs(m_endpoints[i]*SLOPE_ERR_TOLERANCE):
                gap_endpoints = [endpoints[i][1],endpoints[0][0]]
            #    print("m_endpoints[0] = ", m_endpoints[0])
            #    print("m_endpoints[",i,"] = ", m_endpoints[i])
            #    print("gap_endpoints = ", gap_endpoints)
                gap_slope = find_slopes(gap_endpoints)
            #    print("gap_slope = ", gap_slope)
                if abs(m_endpoints[i] - gap_slope) <= abs(m_endpoints[i]*SLOPE_ERR_TOLERANCE):
            #        print("2 gap_slope ",i," = ", gap_slope)
                    endpoints[i][1] = endpoints[0][1]
                    del endpoints[0]
                    m_endpoints = np.delete(m_endpoints, [0])
            #print("m_endpoints = ", m_endpoints)
            return m_endpoints
            break



##### END Merge adjacent lines on the same line #####


##### Find separation between lines  #####

def find_separation(endpoints):
    sep_array = np.empty(len(endpoints))
    for i in range(len(endpoints) - 1):
        sep_array[i] = np.sqrt((endpoints[i + 1][0][1] - endpoints[i][1][1])**2 + \
                               (endpoints[i + 1][0][0] - endpoints[i][1][0])**2)
    sep_array[len(endpoints) - 1] = np.sqrt((endpoints[0][0][1] - endpoints[len(endpoints) - 1][1][1])**2 + \
                           (endpoints[0][0][0] - endpoints[len(endpoints) - 1][1][0])**2)

    return(sep_array)

##### END Find separation between lines  #####


##### Group adjacent points with similar slope angle #####

def find_m_groups(m_array):
    group=0;
    m_group = np.empty(len(m_array))
    for i in range(len(m_array) - 1):
        # test for patching slopes if slope[i] is positive
        if (m_array[i] >= 0):
            if ((m_array[i + 1] <= (m_array[i]*(1 + SLOPE_ERR_TOLERANCE))) and \
                (m_array[i + 1] >= (m_array[i]*(1 - SLOPE_ERR_TOLERANCE)))):
                 m_group[i] = group
            else:
                m_group[i] = group
                group += 1
        # test for patching slopes if slope[i] is negative
        else:
            if ((m_array[i + 1] > (m_array[i]*(1 + SLOPE_ERR_TOLERANCE))) and \
                (m_array[i + 1] < (m_array[i]*(1 - SLOPE_ERR_TOLERANCE)))):
                 m_group[i] = group
            else:
                m_group[i] = group
                group += 1

    ##### Group last point slope angle with previous, first, or its own group #####

    if (m_array[len(m_array) - 1] >= 0):
        if ((m_array[0] <= (m_array[len(m_array) - 1]*(1 + SLOPE_ERR_TOLERANCE))) and \
            (m_array[0] >= (m_array[len(m_array) - 1]*(1 - SLOPE_ERR_TOLERANCE)))):
            m_group[len(m_array) - 1] = 0
        else:
            m_group[len(m_array) - 1] = group
    else:
        if ((m_array[0] >= (m_array[len(m_array) - 1]*(1 + SLOPE_ERR_TOLERANCE))) and \
            (m_array[0] <= (m_array[len(m_array) - 1]*(1 - SLOPE_ERR_TOLERANCE)))):
            m_group[len(m_array) - 1] = 0
        else:
            m_group[len(m_array) - 1] = group
    return(m_group)

##### End Group adjacent points with similar slope angle #####

##### Calculate Segment Lengths #####
##### This is for floorplan files.  Input is an array of tuples #####

def find_seg_len(inp_list):
    seg_len_array = np.empty(len(inp_list))
    for i in range(len(inp_list) - 1):
        seg_len_array[i] = np.sqrt((inp_list[i + 1][0] - inp_list[i][0])**2 + (inp_list[i + 1][1] - inp_list[i][1])**2)
    seg_len_array[len(inp_list) - 1] = np.sqrt((inp_list[0][0] - inp_list[len(inp_list) - 1][0])**2 \
                                               + (inp_list[0][1] - inp_list[len(inp_list) - 1][1])**2)
    return(seg_len_array)

##### End Calculate Segment Lengths #####


##### Calculate Endpoint Lengths #####
##### This is for sample point files.  Input is an array of paired tuples #####

def find_ep_len(endpoints):
    ep_len_array = np.empty(len(endpoints))
    for i in range(len(endpoints)):
        ep_len_array[i] = np.sqrt((endpoints[i][1][0] - endpoints[i][0][0])**2 + \
                                  (endpoints[i][1][1] - endpoints[i][0][1])**2)
    return(ep_len_array)

##### End Calculate Segment Lengths #####


##### Calculate Segment Angle Variance #####

def find_ang_var(m_array):
    ang_variance = np.empty(len(m_array))
    for i in range(len(m_array)):
    #    print("i = ",i)
        if i == 0:
            ang_variance[i] = m_array[i] - m_array[len(m_array) - 1]

        else:
            ang_variance[i] = m_array[i] - m_array[i - 1]
        if ang_variance[i] < 0:
            ang_variance[i] = ang_variance[i] + np.pi*2
        if ang_variance[i] > np.pi*2:
            ang_variance[i] = ang_variance[i] - np.pi*2
    return(ang_variance)

##### End Calculate Segment Angle Variance #####

##### Calculate Polar Vectors from bot to all FP vertices #####

def get_pvect(new_data, bot_loc):
    pvect = np.empty([len(new_data), 2])
    for i in range(len(pvect)):
        # Check if new_data[i][0] equals bot_loc[0], which will cause div by 0 error.
        # If yes, check new_data[i][1] is above or below bot_loc[1].
        # If above, pvect[i][1] set to -pi/2, if below set to pi/2
        if new_data[i][0] == bot_loc[0]:
            if new_data[i][1] < bot_loc[1]:
                pvect_ang = -1*np.pi/2
            else:
                pvect_ang = np.pi/2
        else:
            pvect_ang = np.arctan((new_data[i][1] - bot_loc[1])/(new_data[i][0] - bot_loc[0]))

        # Calculate vector magnitude and angle to each point with respect to point of rotation
        pvect[i]    = [np.sqrt((bot_loc[0] - new_data[i][0])**2 + (bot_loc[1] - new_data[i][1])**2),
                      pvect_ang]

        # arctan only give correct angle for x greater than x of rotation, if less than, need to add
        # pi.
        if new_data[i][0] < bot_loc[0]:
            pvect[i][1] += np.pi

        # convert all angles to positive from 0 to 2*pi 
        if (pvect[i][1] < 0):
            pvect[i][1] += np.pi*2
    return(pvect)

##### END Calculate Polar Vectors from bot to all FP vertices #####

##### Convert Polar Vectors to Cartesian segments #####

def pvect2cvect(pvect, bot_loc):
    cvect = np.empty([len(pvect), 2])
    for i in range(len(pvect)):
        cvect[i] = [pvect[i][0]*np.cos(pvect[i][1]) + bot_loc[0],
                            pvect[i][0]*np.sin(pvect[i][1]) + bot_loc[1]]
    return(cvect)

##### END Convert Polar Vectors to Cartesian segments #####

##### Get key input and recalculate xfrmd_arr #####

def recacl_xarr(event, xfrmd_arr, bot_x, bot_y): 
    if event.key == pygame.K_RIGHT:
        trans_x = -10
        xfrmd_arr = translate_array(xfrmd_arr, [trans_x, 0])
    elif event.key == pygame.K_LEFT:
        trans_x = 10
        xfrmd_arr = translate_array(xfrmd_arr, [trans_x, 0])
    elif event.key == pygame.K_DOWN:
        trans_y = -10
        xfrmd_arr = translate_array(xfrmd_arr, [0, trans_y])
    elif event.key == pygame.K_UP:
        trans_y = 10
        xfrmd_arr = translate_array(xfrmd_arr, [0, trans_y])
    elif event.key == pygame.K_COMMA:
        rotation_inc = np.pi*(1/180)
        xfrmd_arr = rotate_array(xfrmd_arr, ([bot_x, bot_y]), rotation_inc)
    elif event.key == pygame.K_PERIOD:
        rotation_inc = np.pi*(-1/180)
        xfrmd_arr = rotate_array(xfrmd_arr, ([bot_x, bot_y]), rotation_inc)
    return(xfrmd_arr)

##### END Get key input and recalculate xfrmd_arr #####

##### Find the maximum common variance #####

def find_max_common_var(fp_data_v, fp_data_sl, t_r_data_v, t_r_data_sl):
    common_var = np.empty([len(fp_data_v),1])
#    print("len(fp_data_v = ", len(fp_data_v))
#    print("len(t_r_data_v = ", len(t_r_data_v))
    for i in range(len(fp_data_v)):
        common_var[i] = 0
        for j in range(len(t_r_data_v)):
            index = (i + j) % len(t_r_data_v)
#            print("i = ", i,"  j = ", j,"  index = ", index)
            if (abs(fp_data_v[j] - t_r_data_v[index]) < 0.05) and \
               (fp_data_sl[j] - t_r_data_sl[index] >= 0):
                common_var[i] += 1
    return(common_var)

##### Find index with max common variance #####

def find_mcv_index(common_var):
    c_v_index = 0
    max_index = -1
    for i in range(len(common_var)):
        if common_var[i] > c_v_index:
            max_index = i
            c_v_index = common_var[i]
    return(max_index)

#### Find rotation and translation ####
def find_rot_trans(xfrmd_arr, fp_data, fp_data_m, max_index, bot_arr, bot_x, bot_y, x_back_trans, y_back_trans):
    back_calc_rotation = 0
    t_r_data_m_back = find_slopes(xfrmd_arr)
#            print("t_r_data_m_back[0] = ", t_r_data_m_back[0])
#            print("fp_data_m[",max_index,"] = ", fp_data_m[max_index])
    while (abs(t_r_data_m_back[0] - fp_data_m[max_index]) > np.pi/180):
        if t_r_data_m_back[0] - fp_data_m[max_index] < 0:
            back_calc_rotation += 1
            t_r_data_m_back = find_slopes(rotate_array(xfrmd_arr, ([bot_x, bot_y]), np.pi*(1/180)*back_calc_rotation))
        else:
            back_calc_rotation -= 1
            t_r_data_m_back = find_slopes(rotate_array(xfrmd_arr, ([bot_x, bot_y]), np.pi*(1/180)*back_calc_rotation)) 
#                print("t_r_data_m_back[0] = ", t_r_data_m_back[0])
#                print("fp_data_m[",max_index,"] = ", fp_data_m[max_index])
#                print("difference = ", t_r_data_m_back[0] - fp_data_m[max_index])
        print("back_calc_rotation = ", back_calc_rotation)

    back_rotated_arr = rotate_array(xfrmd_arr, ([bot_x, bot_y]), np.pi*(1/180)*back_calc_rotation)
    back_rotated_bot_arr = rotate_array(bot_arr, ([bot_x, bot_y]), np.pi*(1/180)*back_calc_rotation)
    x_back_trans = fp_data[0][0] - back_rotated_arr[0][0]
    y_back_trans = fp_data[0][1] - back_rotated_arr[0][1]
    back_tr_bot_arr = translate_array(back_rotated_bot_arr, [x_back_trans, y_back_trans])
    return(back_tr_bot_arr, x_back_trans, y_back_trans)

#### Calc distance between two cartesian points ####
def get_distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
#    print("point2 = ", point2)
    dist = np.linalg.norm(point1 - point2)
#    print("dist = ", dist)
    return dist


def find_y_intercept(sample_points, m_array):
    b_array = np.empty(len(m_array))
    for i in range(len(m_array)):
        b_array[i] = sample_points[i][1] - np.tan(m_array[i])*sample_points[i][0]
    return(b_array)