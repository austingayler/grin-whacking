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


def find_naive_solution(rectangles):
    placement = []
    upper_left_x = 0
    upper_left_y = 0

    for rectangle in rectangles:
        # print(str(rectangle[1]) + " * " + str(rectangle[0]))
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)  # make a tuple
        placement.insert(0, coordinate)  # insert tuple at front of list
        upper_left_x = upper_left_x + width

    placement.reverse()  # original order
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
    print("Number of rectangles: " + str(len(rectangles)))
    print(str(max[0]) + " * " + str(max[1]))

    mid = math.floor(len(rectangles) / 2)
    print("Midpoint: " + str(rectangles[mid][0]) + " * " + str(rectangles[mid][1]))

    # return find_naive_solution(rectangles)  # a working example!
    return find_solution_ffdh(rectangles)


def find_solution_ffdh(rectangles):
    placement = [None] * len(rectangles)

    cur_x = 0
    cur_y = 0
    calc_y = False

    rectInfo = index_and_sort_rect_list(rectangles)
    rects = rectInfo[0]
    width_sum = rectInfo[1]
    height_sum = rectInfo[2]

    # TODO need to find a better metric for finding the row size.  20 is simply the number of rows.
    row_size = width_sum / 20
    print("width_sum:", width_sum)
    print("height_sum:", height_sum)
    print("row_size:", row_size)
    print("num_rows:", int(width_sum)/row_size)
    max_y = rects[0][1]

    for rect in rects:
        width = rect[0]
        height = rect[1]
        index = rect[2]

        if calc_y is True:
            cur_y = cur_y + max_y
            max_y = 0
            calc_y = False

        if height > max_y:
            max_y = height

        coordinate = (cur_x, cur_y)
        placement[index] = coordinate

        cur_x = cur_x + width

        if cur_x > row_size:
            cur_x = 0
            calc_y = True

    return placement


# TODO find standard deviation between rectangle sizes?  Also returning a bunch of things from a function is bad
# TODO    practice, but it is fast.
def index_and_sort_rect_list(rectangles):
    rects = []
    width_sum = 0
    height_sum = 0
    for index, rect in enumerate(rectangles):
        width_sum += rect[0]
        height_sum += rect[1]
        cur = (rect[0], rect[1], index)
        rects.insert(0, cur)
    rects.sort(key=lambda x: x[1], reverse=True)

    return rects, width_sum, height_sum


def find_max_width_height(rectangles):
    max = [0, 0]  # max = [width, height]
    for rectangle in rectangles:
        # print(str(rectangle[1]) + " * " + str(rectangle[0]))
        if max[0] < rectangle[0]:
            max[0] = rectangle[0]  # width
        if max[1] < rectangle[1]:
            max[1] = rectangle[1]  # height
    return max
