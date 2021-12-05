import numpy as np
from randomgen import PCG64
import itertools
import time
import multiprocessing as mp
from mpi4py import MPI


size_of_generation = 1000
communicator = MPI.COMM_WORLD
rank = communicator.rank
n_cores = communicator.size
stepsize = size_of_generation/n_cores
gene_bases = [base for base in " ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
i = int(rank*stepsize)
j = int(i + stepsize)

print(i,j)

def print_status(gen, parent, score):
    print(f"{gen:3d}  {parent}  ({score})")

def mutate(prng_i, advance, gene,seed_ = 0,mutation_rate=0.05):
    prng = np.random.Generator(PCG64(seed_, prng_i).advance(advance))
    return "".join(
        prng.choice(gene_bases) if prng.random() < mutation_rate else base
        for base in gene
    )

def mutate_parallel(advance,parent,mutation_rate):
    return max([
                mutate(prng_i, advance, parent, mutation_rate=mutation_rate)
                for prng_i in range(i,j)
            ],key = fitness)

def fitness(gene, reference="METHINKS IT IS LIKE A WEASEL"):
    return sum(base == ref_base for base, ref_base in zip(gene, reference))






def weasel_program(mutation_rate=0.05, initial="                            "):
    generation = 0
    score = fitness(initial)
    parent = initial
    
    while score < len(parent):
        print_status(generation, parent, score)
        advance = generation * 2 * len(parent)
        parent_objs = communicator.allgather(mutate_parallel(advance,parent,mutation_rate))
        parent = max(parent_objs,key = fitness)
        generation += 1
        score = fitness(parent)
    print_status(generation, parent, score)
    return generation


start_time = time.perf_counter()
num_generations = weasel_program()
stop_time = time.perf_counter()
print(f"per generation evolution time: {(stop_time - start_time) / num_generations} s")
print(f"total evolution time: {stop_time - start_time} s")





