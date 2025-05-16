# Setiap aset memiliki (return, risiko)
assets = [
    (0.10, 0.05),  # Aset 0
    (0.20, 0.10),  # Aset 1
    (0.15, 0.07),  # Aset 2
    (0.12, 0.06),  # Aset 3
    (0.18, 0.09),  # Aset 4
    (0.08, 0.04),  # Aset 5
]

import random

# Data aset (return, risiko)
assets = [
    (0.10, 0.05),
    (0.20, 0.10),
    (0.15, 0.07),
    (0.12, 0.06),
    (0.18, 0.09),
    (0.08, 0.04),
]

RISK_FREE_RATE = 0.03

# Parameter AG
POP_SIZE = 10
CHROMOSOME_LENGTH = len(assets)
GENERATIONS = 50
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1

# Fungsi evaluasi (fitness) berdasarkan rasio Sharpe
def fitness(chromosome):
    total_return = 0
    total_risk = 0
    count = sum(chromosome)

    if count == 0: return 0  # Tidak valid jika tidak memilih aset

    for gene, (ret, risk) in zip(chromosome, assets):
        if gene == 1:
            total_return += ret
            total_risk += risk

    avg_return = total_return / count
    avg_risk = total_risk / count

    sharpe_ratio = (avg_return - RISK_FREE_RATE) / avg_risk if avg_risk != 0 else 0
    return sharpe_ratio

# Inisialisasi populasi
def init_population():
    return [ [random.randint(0,1) for _ in range(CHROMOSOME_LENGTH)] for _ in range(POP_SIZE) ]

# Seleksi (tournament)
def select(population):
    best = random.choice(population)
    for _ in range(2):
        challenger = random.choice(population)
        if fitness(challenger) > fitness(best):
            best = challenger
    return best

# Crossover satu titik
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

# Mutasi
def mutate(chromosome):
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Algoritma Genetika
def genetic_algorithm():
    population = init_population()
    best_solution = None
    best_fitness = 0

    for gen in range(GENERATIONS):
        new_population = []
        for _ in range(POP_SIZE // 2):
            parent1 = select(population)
            parent2 = select(population)
            child1, child2 = crossover(parent1[:], parent2[:])
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population

        # Simpan solusi terbaik
        for chrom in population:
            f = fitness(chrom)
            if f > best_fitness:
                best_fitness = f
                best_solution = chrom

        print(f"Generasi {gen+1}: Fitness Terbaik = {best_fitness:.4f}")

    return best_solution, best_fitness

# Eksekusi
best_portfolio, best_fitness = genetic_algorithm()
print("\n✅ Solusi Terbaik:", best_portfolio)
print("📈 Fitness (Sharpe Ratio):", round(best_fitness, 4))
