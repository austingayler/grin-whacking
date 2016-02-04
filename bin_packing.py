import math

# ----------------------------------------------
# CSCI 338, Spring 2016, Bin Packing Assignment
# Author: John Paxton
# Last Modified: January 25, 2016
# ----------------------------------------------
# Modified to include find_naive_solution so that
# driver does not need to be imported.  You may delete
# find_naive_solution from your submission.
# ----------------------------------------------

"""
FIND_NAIVE_SOLUTION:
    Line the the top left corners of the rectangles up along
the y = 0 axis starting with (0,0).
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""

def find_naive_solution (rectangles):
    placement = []
    upper_left_x = 0
    upper_left_y = 0

    for rectangle in rectangles:
        # print(str(rectangle[1]) + " * " + str(rectangle[0]))
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)   # make a tuple
        placement.insert(0, coordinate)             # insert tuple at front of list
        upper_left_x = upper_left_x + width

    placement.reverse()                             # original order
    return placement

# -----------------------------------------------

"""
FIND_SOLUTION:
    Define this function in bin_packing.py, along with any auxiliary
functions that you need.  Do not change the driver.py file at all.
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""

def find_solution(rectangles):
    max = find_max_width_height(rectangles)
    print ("Number of rectangles: " + str(len(rectangles)))
    print(str(max[0]) + " * " + str(max[1]))

    mid = math.floor(len(rectangles)/2)
    print ("Midpoint: " + str(rectangles[mid][0]) + " * " + str(rectangles[mid][1]))

    # return find_naive_solution(rectangles)  # a working example!
    return find_solution_ffdh(rectangles)

def find_solution_ffdh(rectangles):
    placement = []
    max_width = 50000 #arbitrary

    cur_x = 0
    cur_y = 0
    calc_y = False


    rects = index_and_sort_rect_list(rectangles)

    for x in rects:
        print(str(x[0]) + ", " + str(x[1]) + ", " + str(x[2]))

    left_rect_y = rects[0][1]

    for rect in rects:
        width = rect[0]
        height = rect[1]
        index = rect[2]

        if calc_y is True:
            cur_y = left_rect_y
            left_rect_y = cur_y + height
            calc_y = False


        cur_x = cur_x + width
        coordinate = (cur_x, cur_y)
        placement.insert(index, coordinate)

        if cur_x > max_width:
            cur_x = 0
            calc_y = True

    return placement

def index_and_sort_rect_list(rectangles):
    rects = []
    for index, rect in enumerate(rectangles):
        cur = (rect[0], rect[1], index)
        rects.insert(0, cur)
    rects.sort(key = lambda x : x[0], reverse=True)

    return rects

def find_max_width_height(rectangles):
    max = [0,0] # max = [width, height]
    for rectangle in rectangles:
        # print(str(rectangle[1]) + " * " + str(rectangle[0]))
        if max[0] < rectangle[0]: max[0] = rectangle[0]  # width
        if max[1] < rectangle[1]: max[1] = rectangle[1]  # height
    return max
