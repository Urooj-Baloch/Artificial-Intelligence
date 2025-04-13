#Question2:
import random
tasks = {
    'Task1': {'time': 5, 'costs': [10, 12, 9]},
    'Task2': {'time': 8, 'costs': [15, 14, 16]},
    'Task3': {'time': 4, 'costs': [8, 9, 7]},
    'Task4': {'time': 7, 'costs': [12, 10, 13]},
    'Task5': {'time': 6, 'costs': [14, 13, 12]},
    'Task6': {'time': 3, 'costs': [9, 8, 10]},
    'Task7': {'time': 9, 'costs': [11, 12, 13]}
}

facilities = {
    'Facility1': {'capacity': 24},
    'Facility2': {'capacity': 30},
    'Facility3': {'capacity': 28}
}

POPULATION_SIZE = 6
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
MAX_GENERATIONS = 100

def create_chromosome():
    return [random.randint(0, 2) for _ in range(7)]

def calculate_fitness(chromosome):
    total_cost = 0
    facility_load = [0, 0, 0]

    for task_idx, facility_idx in enumerate(chromosome):
        task = list(tasks.values())[task_idx]
        total_cost += task['costs'][facility_idx] * task['time']
        facility_load[facility_idx] += task['time']
    penalty = 0
    for i, capacity in enumerate([24, 30, 28]):
        if facility_load[i] > capacity:
            penalty += (facility_load[i] - capacity) * 1000

    return 1 / (total_cost + penalty + 1)

def roulette_wheel_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, fitness in enumerate(fitnesses):
        current += fitness
        if current > pick:
            return population[i]
    return population[-1]

def one_point_crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, len(parent1)-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def swap_mutation(chromosome):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

def genetic_algorithm():
    population = [create_chromosome() for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        fitnesses = [calculate_fitness(chrom) for chrom in population]
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)
            child1, child2 = one_point_crossover(parent1, parent2)
            new_population.append(swap_mutation(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(swap_mutation(child2))

        population = new_population

    best_chromosome = max(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_chromosome)

    assignment = {}
    facility_load = [0, 0, 0]
    total_cost = 0

    for task_idx, facility_idx in enumerate(best_chromosome):
        task_name = list(tasks.keys())[task_idx]
        facility_name = list(facilities.keys())[facility_idx]
        task = list(tasks.values())[task_idx]
        assignment[task_name] = facility_name
        facility_load[facility_idx] += task['time']
        total_cost += task['costs'][facility_idx] * task['time']

    return {
        'assignment': assignment,
        'total_cost': total_cost,
        'facility_loads': {
            'Facility1': facility_load[0],
            'Facility2': facility_load[1],
            'Facility3': facility_load[2]
        }
    }

solution = genetic_algorithm()
print("Task Assignments:", solution['assignment'])
print("Total Cost:", solution['total_cost'])
print("Facility Loads:", solution['facility_loads'])