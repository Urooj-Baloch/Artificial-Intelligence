import heapq
import random
import time

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Node:
    def __init__(self, position, g_cost, h_cost, parent=None):
        self.position = position
        self.g = g_cost
        self.h = h_cost
        self.f = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def a_star(grid, start, end, edge_costs):
    open_list = []
    closed_list = set()
    
    start_node = Node(start, 0, calculate_heuristic(start, end))
    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)

        if current.position == end:
            return reconstruct_path(current)

        closed_list.add(current.position)

        for dx, dy in MOVES:
            x, y = current.position
            nx, ny = x + dx, y + dy

            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue

            if grid[nx][ny] == 1 or (nx, ny) in closed_list:
                continue

            edge_cost = edge_costs.get((current.position, (nx, ny)), 1)

            g_cost = current.g + edge_cost
            h_cost = calculate_heuristic((nx, ny), end)
            neighbor = Node((nx, ny), g_cost, h_cost, current)

            heapq.heappush(open_list, neighbor)

    return None

def calculate_heuristic(position, end):
    return abs(position[0] - end[0]) + abs(position[1] - end[1])

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]

def update_edge_costs(edge_costs):
    for _ in range(5):
        edge = random.choice(list(edge_costs.keys()))
        new_cost = random.randint(1, 5)
        edge_costs[edge] = new_cost
        time.sleep(2)

def main():
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    end = (4, 4)

    edge_costs = {
        ((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1,
        ((0, 1), (0, 0)): 1, ((1, 0), (0, 0)): 1,
        ((1, 0), (1, 1)): 1, ((1, 1), (1, 0)): 1,
    }

    while True:
        print("Running A* Search...")
        path = a_star(grid, start, end, edge_costs)
        if path:
            print(f"Found path: {path}")
        else:
            print("No path found.")
        
        print("Updating edge costs.")
        update_edge_costs(edge_costs)

if __name__ == "__main__":
    main()
