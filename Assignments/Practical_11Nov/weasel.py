import numpy as np
from randomgen import PCG64
import itertools
import time
import multiprocessing as mp

gene_bases = [base for base in " ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

#seed = 1
size_of_generation = 1000






def mutate(prng_i, advance, gene, seed_ = 0,mutation_rate=0.05):
    prng = np.random.Generator(PCG64(seed_, prng_i).advance(advance))
    return "".join(
        prng.choice(gene_bases) if prng.random() < mutation_rate else base
        for base in gene
    )


def fitness(gene, reference="METHINKS IT IS LIKE A WEASEL"):
    return sum(base == ref_base for base, ref_base in zip(gene, reference))


def print_status(gen, parent, score):
    print(f"{gen:3d}  {parent}  ({score})")

def getMax(advance,parent,mutation_rate):
    return max(
            [
                mutate(prng_i, advance, parent, mutation_rate=mutation_rate)
                for prng_i in range(size_of_generation)
            ],
            key=fitness,
        )

def mutate_parallel(advance, parent,mutation_rate,i,j):
    return max([
                mutate(prng_i, advance, parent, mutation_rate=mutation_rate)
                for prng_i in range(i,j)
            ],key = fitness)
            
def mutate_parallel_s2(seed_, advance,parent,mutation_rate):
    return max(
            [
                mutate(prng_i, advance, parent, seed_,mutation_rate=mutation_rate)
                for prng_i in range(size_of_generation)
            ],
            key=fitness,
        )
def weasel_program(mutation_rate=0.05, initial="                            "):
    generation = 0
    score = fitness(initial)
    parent = initial
    num_cpus = mp.cpu_count()
    pool = mp.Pool(num_cpus)
    ll = list(range(num_cpus))
    step = size_of_generation//num_cpus
    while score < len(parent):
        print_status(generation, parent, score)
        advance = generation * 2 * len(parent)
        parent_objs = [pool.apply_async(mutate_parallel,args = (advance,parent,mutation_rate,i*step,i*step+step)) for i in ll]
        parent = max([parent_obj.get() for parent_obj in parent_objs],key = fitness)
        generation += 1
        score = fitness(parent)
    print_status(generation, parent, score)
    return generation


def weasel_program_v2(mutation_rate=0.05, initial="                            "):
    generation = 0
    score = fitness(initial)
    parent = initial
    num_cpus = mp.cpu_count()
    pool = mp.Pool(num_cpus)
    ll = list(range(num_cpus))
    step = size_of_generation//num_cpus
    while score < len(parent):
        print_status(generation, parent, score)
        advance = generation * 2 * len(parent)
        parent_objs = [pool.apply_async(mutate_parallel_s2,args = (advance,parent,seed_,mutation_rate)) for seed_ in range(num_cpus)]
        parent = max([parent_obj.get() for parent_obj in parent_objs],key = fitness)
        generation += 1
        score = fitness(parent)
    print_status(generation, parent, score)
    return generation


if __name__ == '__main__':


    start_time = time.perf_counter()
    num_generations = weasel_program()
    stop_time = time.perf_counter()
    print(f"per generation evolution time: {(stop_time - start_time) / num_generations} s")
    print(f"total evolution time: {stop_time - start_time} s")