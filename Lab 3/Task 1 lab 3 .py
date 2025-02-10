import heapq

class GoalBasedAgentDFS:
    def __init__(self, graph_data, start_node, goal_node):
        self.graph_data = graph_data
        self.start_node = start_node
        self.goal_node = goal_node
        self.visited_nodes = set()

    def search(self, current_node):
        if current_node == self.goal_node:
            return [current_node]
        
        self.visited_nodes.add(current_node)
        
        for neighbor in self.graph_data[current_node]:
            if neighbor not in self.visited_nodes:
                path = self.search(neighbor)
                if path:
                    return [current_node] + path
        
        return None

    def run(self):
        return self.search(self.start_node)

class GoalBasedAgentDLS:
    def __init__(self, graph_data, start_node, goal_node, depth_limit):
        self.graph_data = graph_data
        self.start_node = start_node
        self.goal_node = goal_node
        self.depth_limit = depth_limit
        self.visited_nodes = set()

    def search(self, current_node, depth):
        if current_node == self.goal_node:
            return [current_node]
        
        if depth == 0:
            return None
        
        self.visited_nodes.add(current_node)

        for neighbor in self.graph_data[current_node]:
            if neighbor not in self.visited_nodes:
                path = self.search(neighbor, depth - 1)
                if path:
                    return [current_node] + path
        
        return None

    def run(self):
        return self.search(self.start_node, self.depth_limit)

class UtilityBasedAgentUCS:
    def __init__(self, graph_data, start_node, goal_node):
        self.graph_data = graph_data
        self.start_node = start_node
        self.goal_node = goal_node

    def run(self):
        frontier = [(0, self.start_node)]
        came_from = {self.start_node: None}
        cost_so_far = {self.start_node: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == self.goal_node:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return path[::-1]

            for neighbor, cost in self.graph_data[current_node]:
                new_cost = current_cost + cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current_node
                    heapq.heappush(frontier, (new_cost, neighbor))

        return None

# Example Graph Data
graph_data_dfs = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

graph_data_dls = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

graph_data_ucs = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2)],
    'C': [('D', 1)],
    'D': []
}

# Test DFS Agent
dfs_agent = GoalBasedAgentDFS(graph_data_dfs, 'A', 'F')
dfs_path = dfs_agent.run()
print("DFS Path:", dfs_path)

# Test DLS Agent
dls_agent = GoalBasedAgentDLS(graph_data_dls, 'A', 'F', 2)
dls_path = dls_agent.run()
print("DLS Path:", dls_path)

# Test UCS Agent
ucs_agent = UtilityBasedAgentUCS(graph_data_ucs, 'A', 'D')
ucs_path = ucs_agent.run()
print("UCS Path:", ucs_path)
