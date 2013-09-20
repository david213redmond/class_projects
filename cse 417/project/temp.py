import math
import numpy as np
import random

n = 10

class flow_network(object):
    def __init__(self):
        self.heap = []
        self.vertices = []
        self.last_index = -1
        self.heap_size = n
        self.edges = [[None]*n]*n
        self.M = []
        self.X = []
        self.Y = []

    def init2():
        #vertices are denoted by integer indices.
        for i in range(0,n):
            x = Vertex()
            y = Vertex()
            self.X.append(x)
            self.Y.append(y)
        
    def increase_heap(self,x):
        if self.last_index + 1 >= self.heap_size:
            raise Exception("Exceeds the storage limit of the heap.")
        self.last_index += 1
        index = self.last_index
        self.heap.append(x)
        while index > 0:
            p_index = math.floor((index-1)/2)
            p_x = self.heap[p_index]
            if x.cost_dp >= p_x.cost_dp:
                break
            #percolate up
            self.heap[index] = p_x
            index = p_index
        self.heap[index] = x
        
    def delete_min(self):
        if len(self.heap) >= 1:
            min_val = self.heap[0]
            self.heap[0] = self.heap[-1]
            del self.heap[-1]
            self.last_index -= 1
            index = 0
            smallest = index
            while True:
                x = self.heap[index]
                left_index = 2*index+1
                right_index = 2*index+2
                if left_index <= self.last_index and self.heap[left_index].cost_dp < self.heap[smallest].cost_dp:
                    smallest = left_index
                if right_index <= self.last_index and self.heap[right_index].cost_dp < self.heap[smallest].cost_dp:
                    smallest = right_index
                if smallest != index:
                    self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                    index = smallest
                else:
                    break
            return min_val
        else:
            raise Exception("Trying to delete an element off an empty heap!")

    def find_path2(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge,residual) in path:
                result = self.find_path2( edge.sink, sink, path + [(edge,residual)] ) 
                if result != None:
                    return result
    def dijkstra(self):
        for i in range(0,n):
            self.vertices.append(Vertex())
            self.vertices[i].cost_dp = float("inf")
        self.vertices[0].cost_dp = 0
        for v in self.vertices:
            self.increase_heap(v)
        while self.heap: #heap is not empty
            n = self.delete_min()
            
    
    def __repr__(self):
        return "%s" %(self.heap)
    
class Vertex(object):
    def __init__(self):
        self.index = 0
        self.price = 0
        self.cost_dp = 0
        self.prev = None
    def __repr__(self):
        return "%s: %s" % (self.index , self.cost_dp)

class Edge(object):
    def __init__(self, w):
        self.capacity = w
        self.flow = 0 #no representation yet.
        self.matched = False
        
    def __repr__(self):
        return "%s" % self.capacity

g = flow_network()
g.dijkstra()


