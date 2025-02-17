import math
import heapq

class DeliveryPoint:
    def __init__(self, x, y, start_time, end_time):
        self.x = x
        self.y = y
        self.start_time = start_time
        self.end_time = end_time
        self.visited = False
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __lt__(self, other):
        return self.start_time < other.start_time

def greedy_best_first_search(start, delivery_points):
    current_position = start
    current_time = 0
    total_distance = 0
    route = [start]

    delivery_points.sort()

    while delivery_points:
        next_point = None
        for point in delivery_points:
            if not point.visited:
                travel_time = current_position.distance_to(point)
                arrival_time = current_time + travel_time
                if arrival_time <= point.end_time:
                    if next_point is None or point.start_time < next_point.start_time:
                        next_point = point
                        travel_distance = travel_time

        if next_point:
            total_distance += travel_distance
            current_position = next_point
            current_time += travel_distance
            next_point.visited = True
            route.append((current_position.x, current_position.y))
        else:
            break

    return route, total_distance

def main():
    delivery_points = [
        DeliveryPoint(1, 3, 5, 10),
        DeliveryPoint(4, 4, 2, 6),
        DeliveryPoint(6, 1, 7, 12),
        DeliveryPoint(7, 5, 3, 8)
    ]

    start = DeliveryPoint(0, 0, 0, 0)

    route, total_distance = greedy_best_first_search(start, delivery_points)

    print(f"Optimized Delivery Route: {route}")
    print(f"Total Distance Traveled: {total_distance}")

if __name__ == "__main__":
    main()
