from numpy import random
from math import sqrt
import time
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

random.seed(15)

#2(2), 13(2.5), 15(2.5)

def create_points(k, amount, loc=0, scale=0.8):
    points = []
    std_size = int(amount/k)
    last_size = std_size + int(amount - k*std_size)
    for i in range(k):
        if i == k-1:
            for point in random.normal(loc, scale, size=(last_size, 2)):
                points.append([point[0]+i*2.5,point[1]+i*2.5])
        else:
            for point in random.normal(loc, scale, size=(std_size, 2)):
                points.append([point[0]+i*2.5,point[1]+i*2.5])
    return points

def create_dendra(points):
    labelList = []
    for point in points:
        labelList.append('[' + str(round(point[0], 2)) + ',' + str(round(point[1], 2)) + ']')

    linked = linkage(points, 'single')
    plt.figure(figsize = (10, 7))
    dendrogram(linked, orientation = 'top', labels=labelList,
    distance_sort ='descending',show_leaf_counts = True)
    plt.show()

def clasterize(points, k):
    centers = []
    prev_centers = []
    for i in range(k):
        center_index = random.randint(0, len(points))
        centers.append(points[center_index])
        del points[center_index]

    points_with_clasters = empty_points(points)
    iteration = 0
    plt.show()
    while not prev_centers==centers:
        for key, value in points_with_clasters.items():
            points_with_clasters[key] = find_cluster(from_key_to_point(key), centers)
        prev_centers = centers.copy()
        centers = recalculate_centers(points_with_clasters, centers)
        #print("Iteration", iteration) 
        display_clusters(points_with_clasters, centers, iteration)
        iteration+=1

    plt.close()
    
def empty_points(points):
    points_with_clusters = dict()
    for point in points:
        points_with_clusters[str(point[0]) + "," + str(point[1])]=0
    return points_with_clusters

def find_cluster(point, centers):
    distances = []
    for center in centers:
        distances.append(sqrt(pow(center[0]-point[0],2)+pow(center[1]-point[1],2)))
    cluster = distances.index(min(distances)) + 1
    return cluster

def recalculate_centers(points_with_clusters, centers):
    _new_centers = []
    distances = dict()
    for center in centers:
        points_with_clusters[str(center[0]) + "," + str(center[1])] = centers.index(center) + 1

    for i in range(len(centers)):
        temp_x = 0
        temp_y = 0
        num = 0
        for key, value in points_with_clusters.items():
            if value==i+1:
                temp_x+=from_key_to_point(key)[0]
                temp_y+=from_key_to_point(key)[1]
                num+=1

        _new_centers.append([temp_x/num, temp_y/num])

    for i in range(len(_new_centers)):
        for key, value in points_with_clusters.items():
            point = from_key_to_point(key)
            distances[key] = sqrt(pow(_new_centers[i][0]-point[0],2)+pow(_new_centers[i][1]-point[1],2))
        distances = dict(sorted(distances.items(), key=lambda item: item[1]))
        keys_view = distances.keys()
        keys_iterator = iter(keys_view)
        center = next(keys_iterator)
        del points_with_clusters[center]
        distances=dict()
        _new_centers[i]=from_key_to_point(center)
    return _new_centers

def from_key_to_point(s):
    return [float(s.split(',')[0]),float(s.split(',')[1])]

def display_points(points):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.title("Points") 
    plt.xlabel("x") 
    plt.ylabel("y") 
    plt.plot(x, y, 'ro', markersize=2) 
    plt.show()

def display_clusters(points_with_clasters, centers, iteration):
    x_centers, y_centers = [], []
    x1, y1, x2, y2, x3, y3, x4, y4 = [], [], [], [], [], [], [], []
    for center in centers:
        x_centers.append(center[0])
        y_centers.append(center[1])
    for key, value in points_with_clasters.items():
        if value == 1:
            x1.append(float(key.split(',')[0]))
            y1.append(float(key.split(',')[1]))
        elif value == 2:
            x2.append(float(key.split(',')[0]))
            y2.append(float(key.split(',')[1]))
        elif value == 3:
            x3.append(float(key.split(',')[0]))
            y3.append(float(key.split(',')[1]))
        else:
            x4.append(float(key.split(',')[0]))
            y4.append(float(key.split(',')[1]))

    plt.title("Points") 
    plt.xlabel("x") 
    plt.ylabel("y")

    axes = plt.gca()
    axes.text(7, -1, "Iteration: " + str(iteration))
    axes.plot([x_centers[0]], [y_centers[0]], 'b', zorder=200, marker='s', markersize=5)
    axes.plot([x_centers[1]], [y_centers[1]], 'r', zorder=200, marker='s', markersize=5) 
    axes.plot([x_centers[2]], [y_centers[2]], 'g', zorder=200, marker='s', markersize=5) 
    axes.plot([x_centers[3]], [y_centers[3]], 'k', zorder=200, marker='s', markersize=5) 
    axes.plot(x1, y1, 'cornflowerblue',
            x2, y2, 'lightcoral',
            x3, y3, 'limegreen',
            x4, y4, 'slategrey',
            marker = 'o',
            ls='',
            markersize=3)
    plt.pause(0.5)
    plt.draw()
    plt.pause(0.5)
    plt.clf()

def main():
    points = create_points(4, 445)
    clasterize(points, 4)
    create_dendra(points)

main()