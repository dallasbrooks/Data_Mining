# Course: Seng 474
# Project: Final
# Name:				UvicID:
# Griffin Storback	V00849885
# Jeffrey Olmstead	V00852585
# Dallas Brooks		V00868024

# Data:
# 	https://www.kaggle.com/martinellis/nhl-game-data#game_plays.csv
# File:
# 	game_plays.csv

# python3 NHL_best_shot.py game_plays.csv

import sys
import csv
import time
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

t0 = time.time()

#
# Functions
#

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def print_goal_averages():
    slap_average = 1.0 * goal_counts["Slap Shot"] / (goal_counts["Slap Shot"] + shot_counts["Slap Shot"])
    snap_average = 1.0 * goal_counts["Snap Shot"] / (goal_counts["Snap Shot"] + shot_counts["Snap Shot"])
    wrist_average = 1.0 * goal_counts["Wrist Shot"] / (goal_counts["Wrist Shot"] + shot_counts["Wrist Shot"])
    wrap_average = 1.0 * goal_counts["Wrap-around"] / (goal_counts["Wrap-around"] + shot_counts["Wrap-around"])
    tip_average = 1.0 * goal_counts["Tip-In"] / (goal_counts["Tip-In"] + shot_counts["Tip-In"])
    backhand_average = 1.0 * goal_counts["Backhand"] / (goal_counts["Backhand"] + shot_counts["Backhand"])
    deflected_average = 1.0 * goal_counts["Deflected"] / (goal_counts["Deflected"] + shot_counts["Deflected"])
    print("Slap average:\t\t" + str(round(100 * slap_average, 3)) + "%")
    print("Snap average:\t\t" + str(round(100 * snap_average, 3)) + "%")
    print("Wrist average:\t\t" + str(round(100 * wrist_average, 3)) + "%")
    print("Wrap average:\t\t" + str(round(100 * wrap_average, 3)) + "%")
    print("Tip average:\t\t" + str(round(100 * tip_average, 3)) + "%")
    print("Backhand average:\t" + str(round(100 * backhand_average, 3)) + "%")
    print("Deflected average:\t" + str(round(100 * deflected_average, 3)) + "%")
    return

def scatter_goal_locations():
    plt.figure(1)
    xx, yy = zip(*goal_positions["Slap Shot"])
    p1 = plt.scatter(xx, yy, color="blue", alpha=0.4)
    xx, yy = zip(*goal_positions["Snap Shot"])
    p2 = plt.scatter(xx, yy, color="red", alpha=0.4)
    xx, yy = zip(*goal_positions["Deflected"])
    p3 = plt.scatter(xx, yy, color="orange", alpha=0.4)
    xx, yy = zip(*goal_positions["Wrist Shot"])
    p4 = plt.scatter(xx, yy, color="green", alpha=0.4)
    xx, yy = zip(*goal_positions["Backhand"])
    p5 = plt.scatter(xx, yy, color="yellow", alpha=0.4)
    xx, yy = zip(*goal_positions["Tip-In"])
    p6 = plt.scatter(xx, yy, color="cyan", alpha=0.4)
    xx, yy = zip(*goal_positions["Wrap-around"])
    p7 = plt.scatter(xx, yy, color="magenta", alpha=0.4)
    plt.legend((p1, p2, p3, p4, p5, p6, p7), ('Slap Shot', 'Snap Shot', 'Deflected', 'Wrist Shot', 'Backhand', 'Tip-In', 'Wrap-around'))
    plt.title("Goal Locations by Shot Type")
    plt.show()
    return

def goals_shots_bar_graph():
    plt.figure(2)
    ind = np.arange(7)
    width = 0.35
    goal_counts_array = []
    shot_counts_array = []
    names_array = []
    for goal_type in goal_counts:
        goal_counts_array.append(goal_counts[goal_type])
        shot_counts_array.append(shot_counts[goal_type])
        names_array.append(goal_type)
    p1 = plt.bar(ind, goal_counts_array, width)
    p2 = plt.bar(ind, shot_counts_array, width, bottom=goal_counts_array)
    plt.xticks(ind, names_array)
    plt.legend((p1[0], p2[0]), ('Goals', 'Shots'))
    plt.title('Unsuccessful Shots vs Successful Shots by Shot Type')
    plt.show()
    return

def goal_location_heat_map(str1):
    plt.figure(3)
    plt.clf()
    xx, yy = zip(*goal_positions[str1])
    heatmap, xedges, yedges = np.histogram2d(xx, yy, bins=(1500, 800))
    heatmap = gaussian_filter(heatmap, sigma=16)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap.T, extent=extent, origin="lower", cmap=cm.get_cmap("jet"))
    plt.title(str1 + " Goal Locations")
    plt.show()
    return

#
# Load data
#

if(len(sys.argv) != 2):
    print("Error: No File Given.")
    exit()

f = open(sys.argv[1])

shot_counts = dict()
goal_counts = dict()
goal_positions = dict()

shot_counts["Snap Shot"] = 0
shot_counts["Slap Shot"] = 0
shot_counts["Wrist Shot"] = 0
shot_counts["Wrap-around"] = 0
shot_counts["Tip-In"] = 0
shot_counts["Backhand"] = 0
shot_counts["Deflected"] = 0
goal_counts["Snap Shot"] = 0
goal_counts["Slap Shot"] = 0
goal_counts["Wrist Shot"] = 0
goal_counts["Wrap-around"] = 0
goal_counts["Tip-In"] = 0
goal_counts["Backhand"] = 0
goal_counts["Deflected"] = 0

goal_positions["Snap Shot"] = list()
goal_positions["Slap Shot"] = list()
goal_positions["Wrist Shot"] = list()
goal_positions["Wrap-around"] = list()
goal_positions["Tip-In"] = list()
goal_positions["Backhand"] = list()
goal_positions["Deflected"] = list()

for line in f:
    line_values = line.rsplit(",")
    event = line_values[5].strip('\"')
    secondary_type = line_values[6].strip('\"')
    x = line_values[7].strip('\"')
    y = line_values[8].strip('\"')
    if(event == "Goal" and secondary_type != "NA"):
        goal_counts[secondary_type] += 1
        if(is_number(x) and is_number(y)):
            x = float(x)
            y = float(y)
            goal_positions[secondary_type].append((x,y))
    elif(event == "Shot" and secondary_type != "NA"):
        shot_counts[secondary_type] += 1

f.close()

print_goal_averages()

# Print time to find data and print averages
print("Time: " + str((time.time()-t0)/60))

goals_shots_bar_graph()

# Show heat map of the given shot type
goal_location_heat_map("Slap Shot")
goal_location_heat_map("Snap Shot")
goal_location_heat_map("Wrist Shot")
goal_location_heat_map("Backhand")

# Scatter goal locations, colored by their type
scatter_goal_locations()
