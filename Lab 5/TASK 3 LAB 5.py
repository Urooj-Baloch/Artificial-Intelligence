import random
import math
from operator import itemgetter
import matplotlib.pyplot as plt

class TSPOptimizer:
    def __init__(self, locations, pop_count=100, max_gens=500, mutate_chance=0.01):
        self.places = locations
        self.place_count = len(locations)
        self.pop_count = pop_count
        self.max_gens = max_gens
        self.mutate_chance = mutate_chance
        self.current_pop = []
        self.min_dist = float('inf')
        self.optimal_path = []
        self.dist_history = []

    def get_dist(self, place1, place2):
        x1, y1 = place1
        x2, y2 = place2
        return math.hypot(x2 - x1, y2 - y1)

    def calc_path_dist(self, path):
        total = 0
        for i in range(self.place_count):
            total += self.get_dist(path[i], path[(i+1)%self.place_count])
        return total

    def make_random_path(self):
        path = self.places.copy()
        random.shuffle(path)
        return path

    def init_population(self):
        self.current_pop = [self.make_random_path() for _ in range(self.pop_count)]

    def evaluate_population(self):
        scores = [(i, self.calc_path_dist(path)) for i, path in enumerate(self.current_pop)]
        return sorted(scores, key=itemgetter(1))

    def select_parents(self, ranked_paths):
        chosen = []
        for i in range(len(ranked_paths)):
            if i < int(len(ranked_paths)*0.2): 
                chosen.append(ranked_paths[i][0])
            else:  
                chosen.append(ranked_paths[random.randint(0, len(ranked_paths)-1)][0])
        return chosen

    def combine_paths(self, path_a, path_b):
        new_path = [None]*self.place_count
        start, end = sorted([random.randint(0, self.place_count-1) for _ in range(2)])
        new_path[start:end] = path_a[start:end]
        
        remaining = [city for city in path_b if city not in new_path[start:end]]
        ptr = 0
        for i in range(self.place_count):
            if new_path[i] is None:
                new_path[i] = remaining[ptr]
                ptr += 1
        return new_path

    def alter_path(self, path):
        for i in range(self.place_count):
            if random.random() < self.mutate_chance:
                j = random.randint(0, self.place_count-1)
                path[i], path[j] = path[j], path[i]
        return path

    def next_generation(self):
        ranked = self.evaluate_population()
        self.dist_history.append(ranked[0][1])
        
        if ranked[0][1] < self.min_dist:
            self.min_dist = ranked[0][1]
            self.optimal_path = self.current_pop[ranked[0][0]]
        
        parents = self.select_parents(ranked)
        new_pop = []

        elite_count = int(self.pop_count * 0.1)
        for i in range(elite_count):
            new_pop.append(self.current_pop[ranked[i][0]])

        for _ in range(elite_count, self.pop_count):
            parent_a = self.current_pop[random.choice(parents)]
            parent_b = self.current_pop[random.choice(parents)]
            child = self.combine_paths(parent_a, parent_b)
            new_pop.append(child)
        
        self.current_pop = [self.alter_path(path) for path in new_pop]

    def find_best_path(self):
        self.init_population()
        for _ in range(self.max_gens):
            self.next_generation()
   
        plt.plot(self.dist_history)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.title('Optimization Progress')
        plt.show()
        
        return self.optimal_path, self.min_dist

if __name__ == "__main__":
    city_list = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    optimizer = TSPOptimizer(city_list, pop_count=100, max_gens=500)
    best_path, shortest_dist = optimizer.find_best_path()
    
    print("Optimal Path:")
    for city in best_path:
        print(city)
    print(f"\nTotal Distance: {shortest_dist:.2f}")
 
    x_coords, y_coords = zip(*best_path)
    x_coords = x_coords + (x_coords[0],)
    y_coords = y_coords + (y_coords[0],)
    
    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, 'o-')
    plt.title('Optimal Path Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    for i, (x, y) in enumerate(best_path):
        plt.text(x, y, str(i+1))
    plt.show()