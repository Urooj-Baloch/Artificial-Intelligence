from functools import lru_cache

# Cost matrix representation of the given graph
dist = [
    [0, 10, 15, 20],  # City A
    [10, 0, 35, 25],  # City B
    [15, 35, 0, 30],  # City C
    [20, 25, 30, 0]   # City D
]
cities = len(dist)  # Number of cities
@lru_cache(None)
def find_min_cost(visited, curr_city):
    """
    visited: A bitmask representing the visited cities.
    curr_city: The current city.
    Returns the minimum cost to visit all cities and return to the start.
    """
    if visited == (1 << cities) - 1:  
        return dist[curr_city][0]  
    min_path_cost = float('inf')
    
    for next_city in range(cities):
        if visited & (1 << next_city) == 0:  
            new_cost = dist[curr_city][next_city] + find_min_cost(visited | (1 << next_city), next_city)
            min_path_cost = min(min_path_cost, new_cost)
    
    return min_path_cost
optimal_cost = find_min_cost(1, 0)
print("Minimum cost of the shortest route:", optimal_cost)
