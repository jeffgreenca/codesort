# check that networkit is installed and can calculate betweenness
import networkit

g = networkit.graph.Graph(weighted=True)
for i in range(4):
    g.addNode()

g.addEdge(0, 1, 4.0)
g.addEdge(0, 2, 2.0)
g.addEdge(0, 3, 2.0)

# runs in O(m) per sample
a1 = networkit.centrality.EstimateBetweenness(g, 3, normalized=True, parallel=True)
a1.run()
# runs in O(nm)
a2 = networkit.centrality.Betweenness(g, normalized=True)
a2.run()

print(a1.ranking())
print(a2.ranking())
