##perfectMatch.py
##7.64 one run of Dijkstra's Algorithm and O(n) extra time to find the minimum-cost path from s to t.
##7.65 obtain M' by augmenting along the minimum-cost path from s to t. Then p'(v) = cost_dp(v) + p(v) becomes the set of compatible prices for M'

##pseudo

##steps:
##1. object oriented design
##2. further understanding of the algorithm
##3. numpy optimization
import numpy as np
import math
import random

subj = 'person'
obj = 'house'
n = 100 #size of the perfect matching.

class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.cost = w
        self.ingraph = False
    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.sink, self.cost)
    def isequal(self, other):
        return self.source == other.source and self.sink == other.sink 
 
class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.cost_dp = {}
        self.price = {}
        self.vertices = []
        self.M = []
        self.heap = []
        self.last_index = -1
        self.source = 's'
        self.sink = 't'
 
    def add_vertex(self, vertex):
        self.adj[vertex] = []
        self.price[vertex] = 0
        self.vertices.append(vertex)
 
    def add_edge(self, u, v, w=0):
        source = self.source
        sink = self.sink
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,-w)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)

    def find_path(self,source,sink):
        in_edge = {}
        for vertex in self.vertices:
            if vertex == source:
                self.cost_dp[vertex] = 0
            else:
                self.cost_dp[vertex] = float('inf')
            self.increase_heap(vertex)
        while self.heap: #heap is not empty
            u = self.delete_min()
            cost_u = self.cost_dp[u]
            adjs = []
            for edge in self.adj[u]:
                if edge.ingraph:
                    adjs.append(edge)
            for edge in adjs:
                u = edge.source
                v = edge.sink
                w = edge.cost
                reduced_cost = self.price[u] + w - self.price[v]
                if reduced_cost + cost_u < self.cost_dp[v]:
                    self.cost_dp[v] = reduced_cost + cost_u
                    in_edge[v] = edge
            ## need to reheapify after changing costs
            self.reheapify(self.heap)
        # using in_edge dictionary to find the shortest augmented path.
        cur_vertex = sink
        path = []
        # get the node disjoint path of the 
        while cur_vertex != source:
            edge = in_edge[cur_vertex]
            path = [edge] + path
            cur_vertex = edge.source        
        return path

    def reheapify(self,heap):
        self.heap = []
        self.last_index = -1
        for vertex in heap:
            self.increase_heap(vertex)
 
    def increase_heap(self,x):
        self.last_index += 1
        index = self.last_index
        self.heap.append(x)
        while index > 0:
            p_index = math.floor((index-1)/2)
            p_x = self.heap[p_index]
            if self.cost_dp[x] >= self.cost_dp[p_x]:
                break
            #percolate up
            self.heap[index] = p_x
            index = p_index
        self.heap[index] = x
        
    def delete_min(self):
        heap = self.heap
        if len(heap) > 0:
            min_vertex = heap[0]
            heap[0] = heap[-1]
            del heap[-1]
            self.last_index -= 1
            index = 0
            smallest = index
            while heap:
                x = heap[index]
                left_index = 2*index+1
                right_index = 2*index+2
                if left_index <= self.last_index and self.cost_dp[heap[left_index]] < self.cost_dp[heap[smallest]]:
                    smallest = left_index
                if right_index <= self.last_index and self.cost_dp[heap[right_index]] < self.cost_dp[heap[smallest]]:
                    smallest = right_index
                if smallest != index:
                    heap[index], heap[smallest] = heap[smallest], heap[index]
                    index = smallest
                else:
                    break
            self.heap = heap
            return min_vertex
        else:
            raise Exception("Trying to delete an element off an empty heap!")

    def repr_heap(self):
        result = ''
        for vertex in self.heap:
            result+= vertex+':'+str(self.cost_dp[vertex])+', '
        print('heap: '+result)
    
    def min_cost_perfectMatching(self, source, sink):
        M = []
        ##set all residual edges of (s,x) and (y,t) to cost infinity.
        for edge in self.adj[source]:
            edge.redge.cost = float('inf')
        for edge in self.adj[sink]:
            edge.cost = float('inf')
        ##initialize the prices.
        ##initialize p(y) for all the in edges.
        for vertex in self.vertices:
            if vertex[0:len(obj)] == obj:
                adjs = self.adj[vertex]
                min_cost = 0
                for edge in adjs:
                    inedge = edge.redge
                    if inedge.cost < min_cost:
                        self.price[vertex] = inedge.cost
                        min_cost = inedge.cost
        while len(M) < n:
            ##construct Gm
            # all (x,y) not in M are in Gm
            # all (y,x) in M are in Gm
            start_edges = []
            arrival_edges = []
            matched_y = []
            matched_x = []
            for edge in self.adj[source]:
                start_edges.append(edge)
            for edge in self.adj[sink]:
                arrival_edges.append(edge.redge)
            for edge in M:
                if edge.source not in matched_y:
                    matched_y.append(edge.source)
                if edge.sink not in matched_x:
                    matched_x.append(edge.sink)
            for edge in start_edges:
                if edge.sink in matched_x:
                    edge.ingraph = False
                else:
                    edge.ingraph = True
            for edge in arrival_edges:
                if edge.source in matched_y:
                    edge.ingraph = False
                else:
                    edge.ingraph = True
            for vertex in self.vertices:
                for edge in self.adj[vertex]:
                    u = edge.source
                    v = edge.sink
                    #get all the (y,x) edges
                    if u[0:len(obj)] == obj and v[0:len(subj)] == subj:
                        if edge in M:
                            edge.ingraph = True
                            edge.redge.ingraph = False
                        else:                           
                            edge.redge.ingraph = True
                            edge.ingraph = False
            
            path = self.find_path(source,sink)
##            print(self.price)
##            print(path)
##            print(self.cost_dp)
            #Get M' from M using augmenting path.
            for edge in path:
                u = edge.source
                v = edge.sink
                ##augmentation
                if u[0:len(subj)] == subj:
                    # add edge to M when edge points from X to Y.
                    redge = edge.redge
                    M.append(redge)
                if u[0:len(obj)] == obj and edge in M:
                    # delete edge in M if edge points from Y to X.
                    for i in range(0,len(M)):
                        if edge.isequal(M[i]):
                            del M[i]
                            break
            for vertex in self.vertices:
                self.price[vertex] = self.cost_dp[vertex] + self.price[vertex]
        self.M = M

    ## this method shoould be called before executing the perfect matching algorithm.
    def input_info(self):
        for i in range(1,n+1):
            adjs = self.adj[subj+' '+str(i)]
            for edge in adjs:
                if edge.sink != self.source:
                    print(edge.sink+' is of value at '+str(-edge.cost)+' to '+edge.source)
        print()
        
    def output_info(self):
        # matching info.
        result = ""
        for edge in self.M:
            result += edge.sink+" is matched with "+edge.source + '\n'
        print(result)
        # pricing info.
        for i in range(1,n+1):
            obj_i = obj+' '+str(i)
            print(obj_i+' is set at price: '+str(-self.price[obj_i]))
 
def createNetwork(G):
    G.add_vertex('s')
    G.add_vertex('t')
    for i in range(1,n+1):
        G.add_vertex(subj+' '+str(i))
        G.add_vertex(obj+' '+str(i))
##    G.add_edge(subj+' 1',obj+' 1',-10)
##    G.add_edge(subj+' 1',obj+' 2',-30)
##    G.add_edge(subj+' 2',obj+' 1',-50)
##    G.add_edge(subj+' 2',obj+' 2',-20)
        
    for i in range(1,n+1):
        for j in range(1, n+1):
            G.add_edge(subj+' '+str(i),obj+' '+str(j),-random.randint(10,90))
    for i in range(1,n+1):
        G.add_edge('s',subj+' '+str(i),0)
        G.add_edge(obj+' '+str(i),'t',0)
    G.input_info()
    G.min_cost_perfectMatching('s','t')
    G.output_info()
    return G



G = FlowNetwork() #graph for the flow network.
G = createNetwork(G)


