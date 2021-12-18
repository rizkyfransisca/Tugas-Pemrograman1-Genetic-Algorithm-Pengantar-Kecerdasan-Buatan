import random
import math


def generateChromosome(chrom_len):
    chromosome = [int(random.choice([1, 0])) for i in range(chrom_len)]
    return chromosome

def generatePopulation(popul_len, chrom_len):
    population = [generateChromosome(chrom_len) for i in range(popul_len)]
    return population


def decodeChrom(chrom):
    rax = 2
    ray = 1
    rbx = -1
    rby = -1
    sumGx = 0
    sumGy = 0
    sumKuadratx = 0
    sumKuadraty = 0
    for i in range(len(chrom)//2):
        sumGx = sumGx + chrom[i] * (2**(-(i+1)))
        sumKuadratx = sumKuadratx + (2**(-(i+1)))
    for i in range(len(chrom)//2, len(chrom)):
        sumGy = sumGy + chrom[i] * (2**(-(i+1)))
        sumKuadraty = sumKuadraty + (2**(-(i+1)))
    x = rbx + ((rax - rbx)/sumKuadratx)*sumGx
    y = rby + ((ray - rby)/sumKuadraty)*sumGy
    return x, y


def generateFitness(population):
    fitness = list()
    for i in population:
        x, y = decodeChrom(i)
        hxy = ((math.cos(x**2))*(math.sin(y**2))) + (x+y)
        fitness.append(hxy)
    return fitness


def tournament(population, fitness, n):
    idx_chrom = random.sample(range(n), round(n/4))
    # print(idx_chrom)
    parent_candidate = [(fitness[idx_chrom[i]], population[idx_chrom[i]])
                        for i in range(round(n/4))]
    grade = sorted(parent_candidate, key=lambda x: x[0], reverse=True)
    parent = grade[0][1]
    return parent


def crossover(parent1, parent2, pc):
    if pc > random.random():
        titik1 = random.randint(0, len(parent1)//2)
        titik2 = random.randint((len(parent1)//2)+1, len(parent1))
        parent1[titik1:titik2], parent2[titik1:titik2] = parent2[titik1:titik2], parent1[titik1:titik2]
    return parent1, parent2


def mutation(chrom, pm):
    for i in range(len(chrom)):
        if pm > random.random():
            if chrom[i] == 0:
                chrom[i] = 1
            else:
                chrom[i] = 0
    return chrom


def elitisme(population, fitness):
    bestChrom = [(fitness[i], population[i]) for i in range(len(population))]
    grade = sorted(bestChrom, key=lambda x: x[0], reverse=True)
    return [grade[0][1]]


def regeneration(new_population, population, fitness, popul_len, chrom_len, pc, pm):
    while len(new_population) < popul_len:
        parent1 = tournament(population, fitness, popul_len)
        parent2 = tournament(population, fitness, popul_len)
        parent1 = list(parent1)
        parent2 = list(parent2)
        child1, child2 = crossover(parent1, parent2, pc)
        child1 = mutation(child1, pm)
        child2 = mutation(child2, pm)
        new_population.extend([child1, child2])


popul_len = 200
chrom_len = 14
pc = 0.7
pm = 0.2
population = generatePopulation(popul_len, chrom_len)
fitness = generateFitness(population)
count = 0
while fitness[0] < 2.4817210964013796:
    new_population = elitisme(population, fitness)
    regeneration(new_population, population, fitness, popul_len, chrom_len, pc, pm)
    population = new_population
    count += 1
    print("Generasi ke ", count,"\n", population, end="\n")
    fitness = generateFitness(population)

print("Nilai Fitness Maksimum Didapatkan Pada Generasi Ke", count)
print("Kromosom Terbaik: ", population[0])
print(f"Nilai x dan y Kromosom Terbaik: x = {decodeChrom(population[0])[0]} dan y = {decodeChrom(population[0])[1]}" )
print("Fitness Kromosom Terbaik: ", generateFitness(population)[0])
