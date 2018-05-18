import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import os, json, requests, pickle
from scipy.stats import skew
from shapely.geometry import Point,Polygon,MultiPoint,MultiPolygon
from scipy.stats import ttest_ind, f_oneway, lognorm, levy, skew, chisquare
#import scipy.stats as st
from sklearn.preprocessing import normalize, scale
from tabulate import tabulate #pretty print of tables. source: http://txt.arboreus.com/2013/03/13/pretty-print-tables-in-python.html
from shapely.geometry import Point,Polygon,MultiPoint
#matplotlib inline
from geopy.geocoders import Nominatim
import warnings
warnings.filterwarnings('ignore')

def get_addr(loc):
    geolocator = Nominatim()
    location = geolocator.reverse(loc)
    print(location.address)

        
# Download the September 2015 dataset
if os.path.exists('green_tripdata_2016-02.csv'): # Check if the dataset is present on local disk and load it
    data = pd.read_csv('green_tripdata_2016-02.csv')
else: # Download dataset if not available on disk
    url = "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2016-02.csv"
    data = pd.read_csv(url)
    data.to_csv(url.split('/')[-1])

data['Pickup_dt'] = data.lpep_pickup_datetime.apply(lambda x:dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
data['days'] = pd.to_datetime(data['Pickup_dt']).dt.weekday

loc1 = []
loc2 = []
for i in range(len(data)):
    #populate pickup locations weekdays into loc1
    if data['days'][i] < 5:
        loc1.append((data['Pickup_latitude'][i],data['Pickup_longitude'][i]))
    #populate pickup locations of weekends in loc2
    else:
        loc2.append((data['Pickup_latitude'][i],data['Pickup_longitude'][i]))

#take a count of each location on weekdays
u1 = []
for x in sorted(set(loc1)):
    times = loc1.count(x)
    u1.append((x, times))
#u1's second index contains the highest count, so print address of u1[1] 
if not u1:
     #skip if no weekdays were in the list 
    print('No weekdays found')
else: 
    print('Most popular location on weekday', len(u1),u1[1][0])
    get_addr(u1[1][0])
    
#take a count of each location on weekends
u2 = []
for x in sorted(set(loc2)):
    times = loc2.count(x)
    u2.append((x, times))
#u2's second index contains the highest count, so print address of u2[1] 
if not u2:
    #skip if no weekends were in the list 
    print('No weekends found')
else:
    print('Most popular location on weekends', len(u2),u2[1])
    get_addr(u2[1][0])

