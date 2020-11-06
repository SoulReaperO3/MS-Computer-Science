airCodes = ["LAX", "SFO", "PHX", "SEA", "DEN", "ATL", "ORD", "BOS",  "IAD", "JFK"]

import os
import sys
import traceback
from collections import defaultdict

sourceAirport = "LAX"
destAirport = "JFK"
maxCap = 0
graph = defaultdict(list)
temp=[]
class trip:
    source = ""
    dest = ""
    startTime = -1
    arrivalTime = -1
    capacity = 0;
    travellers = 0;
    
    def __init__(self,source, dest, startTime, arrivalTime, cap):
        self.source = source
        self.dest = dest
        self.startTime = startTime
        self.arrivalTime = arrivalTime
        self.capacity = cap
        if(source == sourceAirport):
            self.travellers = cap
        else:
            self.travellers = 0


def getRoutes():
    trips = [];
    file1 = open("./flights1.txt","r")
    routes = file1.readlines()
    for route in routes:
        props = route.strip().split(" ")
        try:
            trips.append(trip(props[0],props[1],int(props[2].strip()),int(props[3].strip()),int(props[4].strip())))
        except Exception as e:
            traceback.print_exc()
    return trips

def makeEdge(graph,k,v):
    graph[k].append(v)


def bfs(incomingFlight, flightCount,cap):
    if(flightCount>2):
        return 0
    else:
       if(incomingFlight.dest == destAirport):
           cap = cap + incomingFlight.travellers
           #maxCap = cap
           return cap
       else:
           if(len(graph[incomingFlight.dest])>0):
               for flight in graph[incomingFlight.dest]:
                   if(incomingFlight.arrivalTime > flight.startTime):
                       continue
                   else:
                       temp.append(incomingFlight.travellers)
                       if(incomingFlight.travellers >= flight.capacity):
                           incomingFlight.travellers = incomingFlight.travellers - flight.capacity
                           flight.travellers = flight.capacity
                       else:
                           flight.travellers = incomingFlight.travellers
                           incomingFlight.travellers = 0;
                       res = bfs(flight, flightCount+1,cap)
                       if(res==0):
                           incomingFlight.travellers = temp.pop()
                           continue
               if(res == 0):
                    return 0
               else:
                   cap = cap + res
    return cap

if __name__ == '__main__':
    try:
        print("test")
        routes = getRoutes()
        for route in routes:
            if(route.source in airCodes and route.dest in airCodes and route.dest != sourceAirport):
                makeEdge(graph, route.source, route)
        for flight in graph[sourceAirport]:
            maxCap = maxCap + bfs(flight,0,0)
        print(maxCap)
    except Exception as detail:
        traceback.print_exc()
