import math
import random

def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calc_route_dist(path):
    dist = 0
    n = len(path)
    for i in range(n):
        dist += get_dist(path[i], path[(i+1)%n])
    return dist

def make_random_path(points):
    path = points.copy()
    random.shuffle(path)
    return path

def get_swapped_paths(path):
    new_paths = []
    n = len(path)
    for i in range(n):
        for j in range(i+1, n):
            temp = path.copy()
            temp[i], temp[j] = temp[j], temp[i]
            new_paths.append(temp)
    return new_paths

def optimize_path(points, tries=1000):
    curr_path = make_random_path(points)
    curr_dist = calc_route_dist(curr_path)

    for _ in range(tries):
        possible_paths = get_swapped_paths(curr_path)
        best_path = None
        best_dist = float('inf')

        for p in possible_paths:
            d = calc_route_dist(p)
            if d < best_dist:
                best_path = p
                best_dist = d

        if best_dist >= curr_dist:
            break

        curr_path = best_path
        curr_dist = best_dist

    return curr_path, curr_dist

if __name__ == "__main__":
    locations = [
        (0, 0),
        (2, 4),
        (3, 1),
        (5, 2),
        (4, 5),
        (1, 3)
    ]
    
    final_path, final_dist = optimize_path(locations)
    
    print("Best Path Found:")
    for pt in final_path:
        print(pt)
    print(f"Path Distance: {final_dist:.2f}")