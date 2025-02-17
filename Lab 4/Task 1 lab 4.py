import heapq
from itertools import permutations

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def best_first_search(maze, start_pos, goal_pos):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    pq = []
    heapq.heappush(pq, (0, start_pos))
    visited.add(start_pos)
    
    while pq:
        _, current = heapq.heappop(pq)
        x, y = current

        if current == goal_pos:
            return True
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                heuristic = abs(nx - goal_pos[0]) + abs(ny - goal_pos[1])
                heapq.heappush(pq, (heuristic, (nx, ny)))

    return False

def find_shortest_route(maze, start_pos, goal_positions):
    all_positions = [start_pos] + goal_positions
    min_distance = float('inf')
    optimal_route = []

    for route in permutations(all_positions):
        total_distance = 0
        valid_route = True
        
        for i in range(len(route) - 1):
            if not best_first_search(maze, route[i], route[i + 1]):
                valid_route = False
                break
            total_distance += abs(route[i][0] - route[i + 1][0]) + abs(route[i][1] - route[i + 1][1])

        if valid_route and total_distance < min_distance:
            min_distance = total_distance
            optimal_route = route

    return min_distance, optimal_route

maze_layout = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start_pos = (0, 0)
goal_positions = [(4, 4), (2, 4)]

distance, route = find_shortest_route(maze_layout, start_pos, goal_positions)

print("Shortest path length:", distance)
print("Optimal route:", route)
