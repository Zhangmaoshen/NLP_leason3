#!/usr/bin/env python 
# -*- coding:utf-8 -*-
########################################################
#initial data for dict city_location{city: coordination}
############################################################
#type(coordination_source)=str
coordination_source = """
{name:'lanzhou', geoCoord:[103.73, 36.03]},
{name:'jiayuguan', geoCoord:[98.17, 39.47]},
{name:'xining', geoCoord:[101.74, 36.56]},
{name:'chengdu', geoCoord:[104.06, 30.67]},
{name:'shijiazhuang', geoCoord:[114.48, 38.03]},
{name:'lasa', geoCoord:[102.73, 25.04]},
{name:'guiyang', geoCoord:[106.71, 26.57]},
{name:'wuhan', geoCoord:[114.31, 30.52]},
{name:'zhengzhou', geoCoord:[113.65, 34.76]},
{name:'jinan', geoCoord:[117, 36.65]},
{name:'nanjing', geoCoord:[118.78, 32.04]},
{name:'hefei', geoCoord:[117.27, 31.86]},
{name:'hangzhou', geoCoord:[120.19, 30.26]},
{name:'nanchang', geoCoord:[115.89, 28.68]},
{name:'fuzhou', geoCoord:[119.3, 26.08]},
{name:'guangzhou', geoCoord:[113.23, 23.16]},
{name:'changsha', geoCoord:[113, 28.21]},
//{name:'海口', geoCoord:[110.35, 20.02]},
{name:'shengyang', geoCoord:[123.38, 41.8]},
{name:'changchun', geoCoord:[125.35, 43.88]},
{name:'haorbing', geoCoord:[126.63, 45.75]},
{name:'taiyuan', geoCoord:[112.53, 37.87]},
{name:'xian', geoCoord:[108.95, 34.27]},
//{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'beijing', geoCoord:[116.46, 39.92]},
{name:'shanghai', geoCoord:[121.48, 31.22]},
{name:'chongqing', geoCoord:[106.54, 29.59]},
{name:'tianjing', geoCoord:[117.2, 39.13]},
{name:'huhehaote', geoCoord:[111.65, 40.82]},
{name:'nanning', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'yinchuan', geoCoord:[106.27, 38.47]},
{name:'wulumuqi', geoCoord:[87.68, 43.77]},
{name:'xiangang', geoCoord:[114.17, 22.28]},
{name:'aomen', geoCoord:[113.54, 22.19]}
"""

import re
city_location = {}
for line in coordination_source.split('\n'):#Extract name and coordinates
    if line.startswith('//'): continue
    if line.strip() == '': continue     #strip--剥夺, delete empty in the beginning. if str==None, 'True' will be returned

    city = re.findall("name:'(\w+)'", line)[0]   #[0] means the first name is selected
    x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]", line)[0]   #first coord is selected
    x_y = tuple(map(float, x_y))  #translate x_y into type float
    city_location[city] = x_y           #city_location: type-dict; cities' coordination
    #print(city, x_y)
#####################################################################################################

###################################################################################
import math
def geo_distance(origin, destination):       #get distance between origin and destination according to their Coordination
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d

def get_city_distance(city1, city2):       #get distance between two cities
    return geo_distance(city_location[city1], city_location[city2])
#coordination is got from dict city_location

import networkx as nx
cities = list(city_location.keys())
city_graph = nx.Graph()   #an empty no-direction graph
city_graph.add_nodes_from(cities)   #add cities as nodes
nx.draw(city_graph, city_location, with_labels=True, node_size=10) #networkx.draw(name, coordination, , node_size= )
##########################################################

#main
#show city_connection route which the distance between two nodes is less than threshold
#############################################
threshold = 700
from collections import defaultdict
cities_connection = defaultdict(list)
for c1 in cities:
    for c2 in cities:
        if c1 == c2: continue
        if get_city_distance(c1, c2) < threshold:
            cities_connection[c1].append(c2)
cities_connection_graph = nx.Graph(cities_connection)
nx.draw(cities_connection_graph, city_location, with_labels=True, node_size=10)

#import matplotlib.pyplot as plt   #show nx graph
#plt.show()
##############################################

#func search()
#############################################

def is_goal(desitination):       #判断找到目的地
    def _wrap(current_path):
        return current_path[-1] == desitination
    return _wrap

#graph is dict--city_connection,
# start is initial city,
# is_goal return true if city is goal
#search_strategy: operate pathes
def search(graph, start, is_goal, search_strategy):
    pathes = [[start]]
    seen = set()
    while pathes:
        path = pathes.pop(0)                    #delete pathes[0] and return it
        last_city_path  = path[-1]
        if last_city_path in seen: continue
        successors = graph[last_city_path ]   #coordinate
        for city in successors:
            if city in path: continue
            new_path = path + [city]
            pathes.append(new_path)
            if is_goal(new_path): return new_path

        seen.add(last_city_path )
        pathes = search_strategy(pathes)

#########################################################3

#func used for strategy
####################################################

#path的总距离
def get_path_distance(path):
    distance = 0
    for i, c in enumerate(path[:-1]):
        distance += get_city_distance(c, path[i + 1])
    return distance

def sort_path(cmp_func, beam=-1):
    def _sorted(pathes):
        return sorted(pathes, key=cmp_func)[:beam]
    return _sorted

def get_comprehensive_path(path):
    return get_path_distance(path) + get_total_station(path)

#统计站点数
def get_total_station(path):
    return len(path)
##################################################
#result=search(cities_connection, start='beijing', is_goal=is_goal('lasa'), search_strategy=lambda n: n)
#print(result)
###########################################
result=search(cities_connection, start='beijing', is_goal=is_goal('lasa'),
              search_strategy=sort_path(get_path_distance, beam=10))
print(result)

