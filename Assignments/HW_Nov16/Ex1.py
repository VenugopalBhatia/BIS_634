import pandas as pd
import requests
import numpy as np
from tqdm.notebook import tqdm
from p_tqdm import p_map
import multiprocessing as mp
## Query the api


def f(a,b):

    params = {
        'a':a,
        'b':b
    }
    headers = {
        "User-Agent": "Sample"
    }
    url = "http://ramcdougal.com/cgi-bin/error_function.py"
    data = requests.get(url,params = params,headers=headers)
    return float(data.text)


def partial_derivatives(h,f,a,b):
    d1 = (f(a+h,b) - f(a-h,b))/(2*h)
    d2 = (f(a,b+h) - f(a,b-h))/(2*h)

    return d1,d2


def gradientDescent(seed,alpha = 0.1,n_iterations = 1000,h = 0.01,stop_threshold = 0.001):
    #print(seed)
    np.random.seed(seed)
    a = np.random.random()
    b = np.random.random()
    #print((a,b))
    check = False
    progress_ = tqdm(total = n_iterations)
    i = 0
    while i < n_iterations :
        try:
            dela,delb = partial_derivatives(h,f,a,b)
            if(abs(dela) < stop_threshold and abs(delb) < stop_threshold):
                check = True
                break
            
            t1 = a - alpha*dela
            t2 = b - alpha*delb
            a = t1
            b = t2
            i+=1
            progress_.update(1)
        except:
            # a, b went out of range so we reset i and a, b
            i = 0
            a = np.random.random()
            b = np.random.random()
    return (a,b),check

def runParallelGradientDescent():
    num_cpus = mp.cpu_count()
    pool = mp.Pool(num_cpus)
    params = pool.map(gradientDescent,list(range(5)))
    return params
