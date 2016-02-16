import math
import statistics
import pprint

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
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(rectangles)
    print("Number of rectangles: " + str(len(rectangles)))

    mid = math.floor(len(rectangles) / 2)
    print("Midpoint: " + str(rectangles[mid][0]) + " * " + str(rectangles[mid][1]))

    # return find_naive_solution(rectangles)  # a working example!
    return find_solution_ffdh(rectangles)


def find_solution_ffdh(rectangles):
    num_rects = len(rectangles)
    placement = [None] * num_rects

    all_widths = [rect[0] for rect in rectangles]
    all_heights = [rect[1] for rect in rectangles]
    all_areas = [rect[0] * rect[1] for rect in rectangles]
    area_sum = sum(all_areas)

    cur_x = 0
    cur_y = 0
    calc_y = False

    rects, width_sum, height_sum = index_and_sort_rect_list(rectangles)

    w_stdev, w_var, w_mean, w_median, w_avg, w_max, w_min = getStats(all_widths, num_rects, width_sum, "width")
    h_stdev, h_var, h_mean, h_median, h_avg, h_max, h_min = getStats(all_heights, num_rects, height_sum, "height")
    a_stdev, a_var, a_mean, a_median, a_avg, a_max, a_min = getStats(all_areas, num_rects, area_sum, "area")
    print("w_stdev/h_stdev:", round(statistics.stdev(all_widths) / statistics.stdev(all_heights)), 2)

    # this only works if it is not uniformly distributed...
    # don't ask me why this works for a large number of rectangles
    row_size = math.sqrt(width_sum) * 25
    print("row_size:", round(row_size, 2))
    print("num_rows:", round(int(width_sum) / row_size), 2)

    max_y = h_max
    for rect in rects:
        width, height, index = rect

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


def find_max_width_height_area(rectangles):
    max_x, max_y, max_a = 0, 0, 0
    for rectangle in rectangles:
        w, h = rectangle
        a = w * h
        if max_x < w:
            max_x = w  # width

        if max_y < h:
            max_y = h  # height

        if max_a < a:
            max_a = a


    return max_x, max_y, max_a


def getStats(rects, num_rects, sum, name):
    print(name + " statistics: ")
    var = statistics.variance(rects)
    stdev = math.sqrt(var)
    mu = statistics.mean(rects)
    coefVar = stdev / mu
    median = statistics.median(rects)
    statistics.StatisticsError()
    avg = sum / num_rects
    max_ = max(rects)
    min_ = min(rects)
    print("    stdev    :", round(stdev, 2))
    print("    mean     :", round(mu, 2))
    print("    coef var :", round(coefVar, 2))
    print("    var      :", round(var, 2))
    print("    median   :", round(median, 2))
    print("    sum      :", round(sum, 2))
    print("    num rects:", round(num_rects, 2))
    print("    avg      :", round(avg, 2))
    print("    max      :", round(max_, 2))
    print("    min      :", round(min_, 2))
    return stdev, var, mu, median, avg, max_, min_
