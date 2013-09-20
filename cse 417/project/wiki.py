##perfectMatch.py

##pseudo
##Start with M equal to the empty set
##Define p(x) = 0 for x in X, and p(y) = min cost(e), e into y for y in Y
##While M is not a perfect matching
##    Find a minimum-cost s-t path P in Gm USING (7.64) with prices p
##    Augment along P to produce a new matching M'
##    Find a set of compatible prices with respect to M' via (7.65)
##Endwhile

##steps:
##1. object oriented design
##2. further understanding of the algorithm
##3. numpy optimization

class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.capacity = w
    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.sink, self.capacity)
 
class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}
        self.M = {}
        self.prices = {}
        self.cost_dp = {}
    def set_price(self, vertex, price):
        self.prices[vertex] = price
    def add_vertex(self, vertex):
        self.adj[vertex] = []
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge #residual edge.
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def find_path(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge,residual) in path:
                result = self.find_path( edge.sink, sink, path + [(edge,residual)] ) 
                if result != None:
                    return result

    def max_flow(self):
        source = 's'
        sink = 't'
        path = self.find_path(source, sink, [])
        while path != None:
            flow = min(res for edge,res in path)
            for edge,res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
        return sum(self.flow[edge] for edge in self.get_edges(source))

g=FlowNetwork()
list(map(g.add_vertex, ['s','o','p','q','r','t']))  #add all vertices to the network.
g.add_edge('s','o',3)
g.add_edge('s','p',3)
g.add_edge('o','p',2)
g.add_edge('o','q',3)
g.add_edge('p','r',2)
g.add_edge('r','t',3)
g.add_edge('q','r',4)
g.add_edge('q','t',2)
print(g.max_flow())
