from queue import Queue, PriorityQueue

romania = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Oradea', 71), ('Arad', 75)],
    'Oradea': [('Sibiu', 151), ('Zerind', 71)],
    'Sibiu': [('Fagaras', 99), ('Rimnicu Vilcea', 80), ('Arad', 140), ('Oradea', 151)],
    'Timisoara': [('Lugoj', 111), ('Arad', 118)],
    'Lugoj': [('Mehadia', 70), ('Timisoara', 111)],
    'Mehadia': [('Drobeta', 75), ('Lugoj', 70)],
    'Drobeta': [('Craiova', 120), ('Mehadia', 75)],
    'Craiova': [('Pitesti', 138), ('Rimnicu Vilcea', 146), ('Drobeta', 120)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Pitesti', 97), ('Craiova', 146)],
    'Fagaras': [('Bucharest', 211), ('Sibiu', 99)],
    'Pitesti': [('Bucharest', 101), ('Rimnicu Vilcea', 97), ('Craiova', 138)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101)]
}

h_values = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Sibiu': 253,
    'Timisoara': 329, 'Lugoj': 244, 'Mehadia': 241, 'Drobeta': 242,
    'Craiova': 160, 'Rimnicu Vilcea': 193, 'Fagaras': 178, 'Pitesti': 98,
    'Bucharest': 0
}

def bfs(start, end):
    q = Queue()
    q.put((start, [start]))
    while not q.empty():
        (city, route) = q.get()
        for (neighbor, _) in romania[city]:
            if neighbor not in route:
                if neighbor == end:
                    return route + [neighbor]
                q.put((neighbor, route + [neighbor]))

def ucs(start, end):
    pq = PriorityQueue()
    pq.put((0, start, [start]))
    while not pq.empty():
        (cost, city, route) = pq.get()
        if city == end:
            return route, cost
        for (neighbor, step_cost) in romania[city]:
            if neighbor not in route:
                pq.put((cost + step_cost, neighbor, route + [neighbor]))

def greedy_bfs(start, end):
    pq = PriorityQueue()
    pq.put((h_values[start], start, [start]))
    while not pq.empty():
        (_, city, route) = pq.get()
        if city == end:
            return route
        for (neighbor, _) in romania[city]:
            if neighbor not in route:
                pq.put((h_values[neighbor], neighbor, route + [neighbor]))

def iddfs(start, end, max_depth=10):
    def dls(node, end, path, depth):
        if depth == 0 and node == end:
            return path
        if depth > 0:
            for (neighbor, _) in romania[node]:
                if neighbor not in path:
                    new_route = dls(neighbor, end, path + [neighbor], depth - 1)
                    if new_route:
                        return new_route
        return None

    for depth in range(max_depth):
        result = dls(start, end, [start], depth)
        if result:
            return result
    return None

source = 'Arad'
destination = 'Bucharest'

print("BFS Path:", bfs(source, destination))
ucs_path, ucs_cost = ucs(source, destination)
print("UCS Path:", ucs_path, "with cost:", ucs_cost)
print("Greedy BFS Path:", greedy_bfs(source, destination))
print("IDDFS Path:", iddfs(source, destination))
