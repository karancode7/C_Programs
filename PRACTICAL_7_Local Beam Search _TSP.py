import random


def calculate_cost(tour, distance):
    cost = 0
    n = len(tour)

    for i in range(n):
        cost += distance[tour[i]][tour[(i + 1) % n]]

    return cost


def generate_neighbors(tour):
    neighbors = []
    n = len(tour)

    for i in range(n):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            neighbors.append(new_tour)

    return neighbors


def local_beam_search(distance, k, max_iterations):
    n = len(distance)

    # Generate k random initial tours
    beam = []

    for _ in range(k):
        tour = list(range(n))
        random.shuffle(tour)
        beam.append(tour)

    # Find initial best tour
    best_tour = min(
        beam,
        key=lambda x: calculate_cost(x, distance)
    )

    best_cost = calculate_cost(best_tour, distance)

    for _ in range(max_iterations):

        all_neighbors = []

        # Generate neighbors for every tour
        for tour in beam:
            all_neighbors.extend(
                generate_neighbors(tour)
            )

        # Sort neighbors according to their cost
        all_neighbors.sort(
            key=lambda x: calculate_cost(x, distance)
        )

        # Select best k tours
        beam = all_neighbors[:k]

        # Check current best tour
        current_tour = beam[0]
        current_cost = calculate_cost(
            current_tour, distance
        )

        # Update best solution
        if current_cost < best_cost:
            best_cost = current_cost
            best_tour = current_tour[:]
        else:
            break

    return best_tour, best_cost


# -------- MAIN PROGRAM --------

print("LOCAL BEAM SEARCH FOR TSP")

n = int(input("Enter number of cities: "))

print("\nEnter the distance matrix:")

distance = []

for i in range(n):
    row = list(
        map(int, input(f"Row {i + 1}: ").split())
    )
    distance.append(row)

k = int(input("\nEnter beam width (k): "))
max_iterations = int(
    input("Enter maximum number of iterations: ")
)

best_tour, best_cost = local_beam_search(
    distance, k, max_iterations
)

print("\nBest Tour:")

for city in best_tour:
    print(city + 1, end=" -> ")

print(best_tour[0] + 1)

print("Minimum Tour Cost:", best_cost)