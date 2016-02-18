import math
import statistics

# ----------------------------------------------
# CSCI 338, Spring 2016, Bin Packing Assignment
# Author: AJ Gayler, Luke Welna
# Last Modified: Feb 17, 2016
# ----------------------------------------------
"""
FIND_SOLUTION:
    Our solution is pretty simple.  We came up with different solutions
    based on the coefficient of variance but as it turns out.  FFDH
    (First-Fit Decreasing Height) is pretty good in most cases. The
    only data-sets our solution seems to have trouble with is perfect
    split and data-sets where the coefficient of variance for heights
    is high. I have a feeling a lot of solutions won't be much better
    for the latter case because the naive isn't that bad... Another
    solution that would break it is if there is one big rectangle
    followed by a bunch of smaller ones, etc.
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
    num_rects = len(rectangles)
    placement = [None] * num_rects

    all_widths = [rect[0] for rect in rectangles]
    all_heights = [rect[1] for rect in rectangles]

    w_sum = sum(all_widths)

    # statistics
    w_stdev, w_coefVar = getStats(all_widths)
    h_stdev, h_coefVar = getStats(all_heights)
    # Was going to use different heuristics based on the coefficient of variation, however, as it turns out.  FFDH is
    #   pretty good in most cases and large data-sets.
    if w_coefVar < 1.75 and h_coefVar < 1.75:
        print("We got some uniformly distributed rectangles")
        if w_stdev / h_stdev < .7:
            print("We got some tall and skinny rectangles yo!")
        else:
            print("Our rectangles are not tall and skinny!")
    else:
        print("Our rectangles are not uniformly distributed")

    get_std_ffdh(rectangles, placement, w_sum, 1, 25)

    return placement


def get_std_ffdh(rectangles, placement, w_sum, sort_key, row_size_multiplier):
    # Standard placement.  Sorts on height, appends rectangles end to end until a given row_size, then starts a new row.
    # this only works perfectly if it is uniformly distributed...
    # don't ask me why this works for a large number of rectangles.
    rects = index_and_sort_rect(rectangles, sort_key)
    row_size = math.sqrt(w_sum) * row_size_multiplier
    cur_x = 0
    cur_y = 0
    calc_y = False
    max_h = 0
    for rect in rects:
        width, height, index = rect
        if calc_y is True:
            cur_y = cur_y + max_h
            max_h = 0
            calc_y = False
        if height > max_h:
            max_h = height
        coordinate = (cur_x, cur_y)
        placement[index] = coordinate
        cur_x = cur_x + width
        if cur_x > row_size:
            cur_x = 0
            calc_y = True


def index_and_sort_rect(rectangles, sort_key):
    rects = []
    for index, rect in enumerate(rectangles):
        cur = (rect[0], rect[1], index)
        rects.insert(0, cur)
    rects.sort(key=lambda x: x[sort_key], reverse=True)
    return rects


def getStats(rects):
    var = statistics.variance(rects)
    stdev = math.sqrt(var)
    mu = statistics.mean(rects)
    coefVar = stdev / mu
    print(coefVar)
    return stdev, coefVar
