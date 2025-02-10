from collections import deque, defaultdict

class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)  # Adjacency list representation

    def add_edge(self, src, dest, bidirectional=True):
        """
        Adds an edge to the graph.
        If bidirectional is True, it creates an undirected graph.
        """
        self.adj_list[src].append(dest)
        if bidirectional:
            self.adj_list[dest].append(src)

    ## ======== Iterative Deepening DFS (IDDFS) ========
    def depth_limited_search(self, current, target, limit, visited_nodes):
        """
        Depth-Limited Search (DLS) helper function for IDDFS.
        """
        if current == target:
            return True
        if limit <= 0:
            return False
        visited_nodes.add(current)
        for neighbor in self.adj_list[current]:
            if neighbor not in visited_nodes and self.depth_limited_search(neighbor, target, limit - 1, visited_nodes):
                return True
        visited_nodes.remove(current)  # Backtrack
        return False

    def iterative_deepening_dfs(self, start, target, max_depth):
        """
        Iterative Deepening DFS (IDDFS) function.
        """
        for depth in range(max_depth + 1):
            visited_nodes = set()
            if self.depth_limited_search(start, target, depth, visited_nodes):
                return True
        return False

    ## ======== Bidirectional Search (BDS) ========
    def bidirectional_search(self, start, target):
        """
        Bidirectional search implementation.
        """
        if start == target:
            return True
        
        forward_queue = deque([start])
        backward_queue = deque([target])
        forward_visited = {start}
        backward_visited = {target}

        while forward_queue and backward_queue:
            if self.expand_search(forward_queue, forward_visited, backward_visited):
                return True
            if self.expand_search(backward_queue, backward_visited, forward_visited):
                return True
        return False

    def expand_search(self, queue, visited_nodes, opposite_visited):
        """
        Expands nodes in the current queue and checks for intersection.
        """
        current = queue.popleft()
        for neighbor in self.adj_list[current]:
            if neighbor in opposite_visited:
                return True  # Searches met
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                queue.append(neighbor)
        return False

# ==== Example Usage ====
g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 5)
g.add_edge(2, 6)

# Testing IDDFS
start_node = 0
goal_node = 5
max_depth = 3
found_iddfs = g.iterative_deepening_dfs(start_node, goal_node, max_depth)
print("IDDFS - Goal Found:", found_iddfs)  # Output: True

# Testing Bidirectional Search
found_bds = g.bidirectional_search(start_node, goal_node)
print("Bidirectional Search - Path Exists:", found_bds)  # Output: True
