import time
import json
import random
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# Sorting algorithms
def algorithm1(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def algorithm2(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def algorithm3(arr):
    if len(arr) <= 1:
        return
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    algorithm3(left)
    algorithm3(right)
    
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

# Data generation functions
def generate_sorted_array(n):
    return list(range(n))

def generate_reversed_array(n):
    return list(range(n, 0, -1))

def generate_random_array(n):
    return [random.randint(0, n) for _ in range(n)]

# Function to copy array
def copy_array(arr):
    return arr[:]

# Function to run sorting tests in parallel
def run_test(algorithm, original_array, iterations):
    total_time = 0
    for _ in range(iterations):
        array_copy = copy_array(original_array)
        start_time = time.time()
        algorithm(array_copy)
        elapsed_time = time.time() - start_time
        total_time += elapsed_time
    return total_time / iterations

# Function to parallelize using ProcessPoolExecutor
def parallel_execution(algorithm, size, arr_type, iterations):
    if arr_type == 'sorted':
        original_array = generate_sorted_array(size)
    elif arr_type == 'reversed':
        original_array = generate_reversed_array(size)
    else:
        original_array = generate_random_array(size)
    
    # Run test to compute the average time
    avg_time = run_test(algorithm, original_array, iterations)
    
    return avg_time

# Main execution to test algorithms
def main():
    sizes = [50, 200, 500, 800, 1200,1800,2500, 5000, 10000]
    types = ['sorted', 'reversed', 'random']
    iterations = 20
    results = []
    algorithms = [algorithm1, algorithm2, algorithm3]
    algorithm_names = ['Algorithm1 (Bubble Sort)', 'Algorithm2 (Selection Sort)', 'Algorithm3 (Merge Sort)']

    # Use ProcessPoolExecutor to parallelize the tests
    with ProcessPoolExecutor() as executor:
        futures = []
        for alg_idx, algorithm in enumerate(algorithms):
            for size in sizes:
                for arr_type in types:
                    futures.append(executor.submit(parallel_execution, algorithm, size, arr_type, iterations))

        # Collect the results
        for idx, future in enumerate(futures):
            alg_idx = idx // (len(sizes) * len(types))
            size_idx = (idx % (len(sizes) * len(types))) // len(types)
            type_idx = (idx % (len(sizes) * len(types))) % len(types)
            
            avg_time = future.result()
            results.append({
                'algorithm': algorithm_names[alg_idx],
                'input_size': sizes[size_idx],
                'input_type': types[type_idx],
                'average_time': avg_time
            })

    # Save results to a JSON file
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    return results

# Run the main function
results = main()

# Plot the results for better visualization
def plot_results_combined(results):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    algorithm_names = ['Algorithm1 (Bubble Sort)', 'Algorithm2 (Selection Sort)', 'Algorithm3 (Merge Sort)']
    input_types = ['sorted', 'reversed', 'random']
    
    for idx, alg in enumerate(algorithm_names):
        ax = axs[idx]
        for arr_type in input_types:
            sizes = [r['input_size'] for r in results if r['algorithm'] == alg and r['input_type'] == arr_type]
            times = [r['average_time'] for r in results if r['algorithm'] == alg and r['input_type'] == arr_type]
            ax.plot(sizes, times, label=f"{arr_type} array")

        ax.set_title(f"Performance of {alg}")
        ax.set_xlabel("Input Size")
        ax.set_ylabel("Average Time (s)")
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.show()

# Call the updated plotting function
plot_results_combined(results)
