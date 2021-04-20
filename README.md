# KG
## To run the server 
``` 
apache-tinkerpop-gremlin-server-3.4.10/bin/
./gremlin-server.sh console
```

## Creating Graph using kgn.py 
A graph can be created using create_graph(self, nodes, edges) function of the
class Import.

* Parameters of create_graph  &nbsp;&nbsp;  : list of nodes and edges between the nodes of the
graph you want to create.
* G = nx.Graph()    &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; : Using NetwrokX module imported as nx, nx.Graph() creates a
empty graph instance of name G.
* G.add_nodes_from(nodes)   &emsp; : This command adds Nodes from the list 'nodes' to
the graph instance G.
* G.add_edges_from(edges)   &emsp; : Adds edges between the nodes specified in the
'edges' list.
* returns the graph instance G to the called block.
>**Example**
>calling Function Block:<br>
```
nodes = [(1, {'labelV': 'node1', 'node_id': 'INT'}), (2, {'labelV': 'node2', 'node_id':
'INT'})]
edges = [(1,2, {'labelV' : 'has'})]
create_graph(self,nodes,edges)  
```
> Creates a graph instance with 2 node and 1 edge
