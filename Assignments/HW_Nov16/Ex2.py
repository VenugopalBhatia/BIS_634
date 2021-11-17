import multiprocessing as mp
import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import random
import itertools
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def plot_figure(data,s = None,plt_show = True,saveFig = False):
    fig = plt.figure(figsize=(10, 10), dpi=80)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.coastlines()
    ax.scatter(data['lng'], data['lat'], s = 2,c = list(data['cluster']), transform=ccrs.PlateCarree())
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
    
    
    if(s != None):
        fname = "Files/img_"+s
        plt.savefig(fname)
    if(plt_show):
        plt.show()
    else:
        plt.close(fig)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def assign_cluster_ids(pts,centers):
    pts = list(pts)
    cluster_ids = []
    for pt in pts:
            min_cluster = -1
            min_dist = float('inf')
            for i, center in enumerate(centers):
                dist = haversine(pt[0],pt[1],center[0],center[1])
                if dist < min_dist:
                    min_cluster = i
                    min_dist = dist
            cluster_ids.append(min_cluster)
    return cluster_ids


def kmeans(df,k = 5):
    data = df.copy()
    pts = [np.array(pt) for pt in zip(data['lng'],data['lat'])]
    centers = random.sample(pts, k)
    old_cluster_ids, cluster_ids = None, [] # arbitrary but different
    while cluster_ids != old_cluster_ids:
        old_cluster_ids = list(cluster_ids)
        cluster_ids = []
        for pt in pts:
            min_cluster = -1
            min_dist = float('inf')
            for i, center in enumerate(centers):
                dist = haversine(pt[0],pt[1],center[0],center[1])
                if dist < min_dist:
                    min_cluster = i
                    min_dist = dist
            cluster_ids.append(min_cluster)
        data['cluster'] = cluster_ids
        cluster_pts = [[pt for pt, cluster in zip(pts, cluster_ids) if cluster == match]
        for match in range(k)]
        centers = [sum(pts)/len(pts) for pts in cluster_pts]
    return data

def kmeans_parallel(df,k = 5):
    num_cpus = mp.cpu_count()
    pool = mp.Pool(num_cpus)
    data = df.copy()
    pts = [np.array(pt) for pt in zip(data['lng'],data['lat'])]
    pts_arr = np.array_split(pts,num_cpus)
    centers = random.sample(pts, k)
    old_cluster_ids, cluster_ids = None, [] # arbitrary but different
    while cluster_ids != old_cluster_ids:
        old_cluster_ids = list(cluster_ids)
        cluster_ids = [pool.starmap(assign_cluster_ids,[(_pts,centers) for _pts in pts_arr])]
        cluster_ids = list(itertools.chain(*cluster_ids))
        cluster_ids = list(itertools.chain(*cluster_ids))
        data['cluster'] = cluster_ids
        cluster_pts = [[pt for pt, cluster in zip(pts, cluster_ids) if cluster == match]
        for match in range(k)]
        centers = [sum(pts)/len(pts) for pts in cluster_pts]
    return data