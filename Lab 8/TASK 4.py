
import random

import numpy as np

states = ['Sunny', 'Cloudy', 'Rainy']
state_to_index = {state: i for i, state in enumerate(states)}

transition_matrix = np.array([
    [0.6, 0.3, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
])

def simulate_weather_sequence(start_state='Sunny', days=10):
    sequence = [start_state]
    current_state = start_state
    for _ in range(days - 1):
        probs = transition_matrix[state_to_index[current_state]]
        next_state = random.choices(states, weights=probs)[0]
        sequence.append(next_state)
        current_state = next_state
    return sequence

one_sequence = simulate_weather_sequence()
print("One simulated sequence:", one_sequence)

def estimate_rainy_probability(trials=10000, days=10, min_rainy_days=3):
    count = 0
    for _ in range(trials):
        seq = simulate_weather_sequence(days=days)
        rainy_days = seq.count('Rainy')
        if rainy_days >= min_rainy_days:
            count += 1
    return count / trials

prob = estimate_rainy_probability()
print(f"Estimated probability of at least 3 rainy days in 10 days: {prob:.4f}")
