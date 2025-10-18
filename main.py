import numpy as np
import matplotlib.pyplot as plt
import json
import re
import argparse
import os  # ← dodane

# Klasa reprezentująca osobnika
class Individual:
    def __init__(self, x, f1, f2):
        self.x = x
        self.f1 = f1
        self.f2 = f2

    def to_dict(self):
        return {"x": self.x.tolist(), "f1": self.f1, "f2": self.f2}


# Funkcje ZDT
def zdt1_f1(x): return x[0]
def zdt1_g(x): return 1 + 9 * np.sum(x[1:]) / (len(x) - 1)
def zdt1_h(f1, g): return 1 - np.sqrt(f1 / g)
def zdt1_f2(x): return zdt1_g(x) * zdt1_h(zdt1_f1(x), zdt1_g(x))
def zdt2_h(f1, g): return 1 - (f1 / g) ** 2
def zdt2_f2(x): return zdt1_g(x) * zdt2_h(zdt1_f1(x), zdt1_g(x))
def zdt3_h(f1, g): return 1 - np.sqrt(f1 / g) - (f1 / g) * np.sin(10 * np.pi * f1)
def zdt3_f2(x): return zdt1_g(x) * zdt3_h(zdt1_f1(x), zdt1_g(x))
def zdt4_g(x): return 1 + 10 * (len(x) - 1) + np.sum(x[1:] ** 2 - 10 * np.cos(4 * np.pi * x[1:]))
def zdt4_f2(x): return zdt4_g(x) * zdt1_h(zdt1_f1(x), zdt4_g(x))
def zdt6_f1(x): return 1 - np.exp(-4 * x[0]) * (np.sin(6 * np.pi * x[0]))**6
def zdt6_g(x): return 1 + 9 * (np.sum(x[1:]) / (len(x) - 1))**0.25
def zdt6_h(f1, g): return 1 - (f1 / g)**2
def zdt6_f2(x): return zdt6_g(x) * zdt6_h(zdt6_f1(x), zdt6_g(x))


def initialize_population(pop_size, num_variables):
    return np.random.rand(pop_size, num_variables)


def evaluate_population(population, zdt_f1, zdt_f2):
    individuals = []
    for x in population:
        f1 = zdt_f1(x)
        f2 = zdt_f2(x)
        individuals.append(Individual(x, f1, f2))
    return individuals


def extract_objectives(individuals):
    return np.array([[ind.f1, ind.f2] for ind in individuals])


def non_dominated_sorting(objectives):
    num_individuals = len(objectives)
    domination_count = np.zeros(num_individuals, dtype=int)
    dominated_solutions = [[] for _ in range(num_individuals)]
    fronts = [[]]
    for p in range(num_individuals):
        for q in range(num_individuals):
            if all(objectives[p] <= objectives[q]) and any(objectives[p] < objectives[q]):
                dominated_solutions[p].append(q)
            elif all(objectives[q] <= objectives[p]) and any(objectives[q] < objectives[p]):
                domination_count[p] += 1
        if domination_count[p] == 0:
            fronts[0].append(p)
    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in dominated_solutions[p]:
                domination_count[q] -= 1
                if domination_count[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    return fronts[:-1]


def calculate_crowding_distance(front, objectives):
    distances = np.zeros(len(front))
    for m in range(objectives.shape[1]):
        sorted_indices = np.argsort(objectives[front, m])
        distances[sorted_indices[0]] = distances[sorted_indices[-1]] = np.inf
        f_min = objectives[front, m][sorted_indices[0]]
        f_max = objectives[front, m][sorted_indices[-1]]
        if f_max - f_min == 0:
            continue
        for i in range(1, len(front) - 1):
            distances[sorted_indices[i]] += (
                (objectives[front, m][sorted_indices[i + 1]] - objectives[front, m][sorted_indices[i - 1]]) / (f_max - f_min)
            )
    return distances


def crossover(parent1, parent2, crossover_rate=0.9):
    if np.random.rand() < crossover_rate:
        point = np.random.randint(1, len(parent1))
        child1 = np.concatenate([parent1[:point], parent2[point:]])
        child2 = np.concatenate([parent2[:point], parent1[point:]])
        return child1, child2
    else:
        return parent1.copy(), parent2.copy()


def mutate(individual, mutation_rate=0.1):
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            individual[i] = np.random.rand()
    return individual


def tournament_selection(population, objectives, k=2):
    selected = []
    pop_size = len(population)
    fronts = non_dominated_sorting(objectives)
    rank = np.zeros(pop_size, dtype=int)
    for i, front in enumerate(fronts):
        for idx in front:
            rank[idx] = i
    distances = np.zeros(pop_size)
    for front in fronts:
        distances_front = calculate_crowding_distance(front, objectives)
        for i, idx in enumerate(front):
            distances[idx] = distances_front[i]
    for _ in range(pop_size):
        participants = np.random.choice(pop_size, k, replace=False)
        best = participants[0]
        for p in participants[1:]:
            if rank[p] < rank[best]:
                best = p
            elif rank[p] == rank[best]:
                if distances[p] > distances[best]:
                    best = p
        selected.append(population[best])
    return np.array(selected)


def nsga2(pop_size, num_generations, num_variables, zdt_f1, zdt_f2, save_iterations):
    population = initialize_population(pop_size, num_variables)
    all_objectives = {}
    for generation in range(num_generations):
        print(f"Iteracja: {generation + 1}/{num_generations}")
        individuals = evaluate_population(population, zdt_f1, zdt_f2)
        objectives = extract_objectives(individuals)
        fronts = non_dominated_sorting(objectives)
        if generation + 1 in save_iterations:
            all_objectives[generation + 1] = objectives
        selected_population = tournament_selection(population, objectives)
        offspring = []
        for i in range(0, pop_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1 if i + 1 < pop_size else 0]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            offspring.append(child1)
            offspring.append(child2)
        offspring = np.array(offspring[:pop_size])
        combined_population = np.vstack((population, offspring))
        individuals = evaluate_population(combined_population, zdt_f1, zdt_f2)
        objectives = extract_objectives(individuals)
        combined_fronts = non_dominated_sorting(objectives)
        new_population = []
        for front in combined_fronts:
            if len(new_population) + len(front) > pop_size:
                distances = calculate_crowding_distance(front, objectives)
                sorted_front = [front[i] for i in np.argsort(-distances)]
                remaining_slots = pop_size - len(new_population)
                new_population.extend(sorted_front[:remaining_slots])
                break
            else:
                new_population.extend(front)
        population = combined_population[np.array(new_population)]
    return all_objectives


def save_results_to_json(results, filename="results.json"):
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    serializable = {
        str(dim): {
            str(iteration): objectives.tolist()
            for iteration, objectives in iteration_dict.items()
        }
        for dim, iteration_dict in results.items()
    }
    with open(filepath, "w") as f:
        json.dump(serializable, f, indent=4)
    print(f"Wyniki zapisane do pliku JSON: {filepath}")


def load_results_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return {int(dim): {int(it): np.array(vals) for it, vals in iters.items()} for dim, iters in data.items()}


def extract_problem_number(name):
    match = re.fullmatch(r"ZDT[1-6]", name)
    return int(name[3:]) if match else None


def plot_pareto(problem_name, dimensions, results, pop_size, seed=3333):
    os.makedirs("results", exist_ok=True)
    for d in dimensions:
        plt.figure(figsize=(10, 8))
        for iter_count, objectives in sorted(results[d].items()):
            plt.scatter(objectives[:, 0], objectives[:, 1], label=f"Iteracja {iter_count}", s=15)
            pareto_front = objectives[non_dominated_sorting(objectives)[0]]
            pareto_front = pareto_front[np.argsort(pareto_front[:, 0])]
            plt.plot(pareto_front[:, 0], pareto_front[:, 1], linestyle='-', marker=None, label=f"Front Pareto {iter_count}")
        plt.title(f"NSGA-II {problem_name} (D={d})", fontsize=14)
        plt.xlabel("f1", fontsize=12)
        plt.ylabel("f2", fontsize=12)
        plt.grid(True)
        plt.legend(title="Iteracje", fontsize=10)
        plt.text(0.01, 1.05, f"Iteracje: {list(results[d].keys())}, Pop Size: {pop_size}, Dim: {d}, Seed: {seed}",
                 transform=plt.gca().transAxes, fontsize=10, verticalalignment='center')
        filename = f"results/{problem_name}_D{d}_pareto.png"
        plt.savefig(filename)
        print(f"Zapisano wykres: {filename}")
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=str, default="ZDT1")
    parser.add_argument("--load", type=str, help="Wczytaj wyniki z pliku JSON")
    parser.add_argument("--save", action="store_true", help="Zapisz wyniki do JSON")
    args = parser.parse_args()

    problems = {
        "ZDT1": (zdt1_f1, zdt1_f2),
        "ZDT2": (zdt1_f1, zdt2_f2),
        "ZDT3": (zdt1_f1, zdt3_f2),
        "ZDT4": (zdt1_f1, zdt4_f2),
        "ZDT6": (zdt6_f1, zdt6_f2),
    }

    if args.problem not in problems:
        print("Nieznany problem. Dozwolone: ZDT1-ZDT6")
        exit(1)

    dimensions = [10, 30, 50]
    iterations = [20, 50, 100, 500]
    pop_size = 150
    seed = 3333
    np.random.seed(seed)
    f1_func, f2_func = problems[args.problem]

    if args.load:
        results = load_results_from_json(args.load)
    else:
        results = {d: nsga2(pop_size, max(iterations), d, f1_func, f2_func, iterations) for d in dimensions}

    plot_pareto(args.problem, dimensions, results, pop_size, seed)

    if args.save:
        save_results_to_json(results, f"{args.problem}_D_results.json")
