# KG

## Change files in apache server folder 
- add graphml file to ``` path_to_server_folder/data ```
- add path of final graphml file here   ``` path_to_server_folder/scripts/school-sample.groovy ```
- add path of script file in conf folder ``` path_to_server_folder/conf/gremlin-server-school.yaml ```  in ScriptEngines value

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

### 2. Created graph is converted into graphml file using *nx.write_graphml(filename)* which is a method in networkx lib.
 
### 3. After converting two schemas into graph, *join_graphs(graph1, graph2)* is called.
* *join_graphs(graph1,graph2)* is a method of the class *Algo()*
* *Parameters* : Two graph instances graph1 and graph2.
* *Returns* : Combined graph with bridge nodes.
* *Description* : Visits each nodes in the two graph and similarity between each nodes of the two graphs is found with the help of wordnet from nltk libraray, and bridge node is added between those two nodes with suitable similarity range. The bridge node is the lowest comman hypernym of the two node.

### 4. Returned graph isntance from *join_graph()* is converted into graphml file using *nx.write_graphml()*. 
### 5. Connection with Tinkerpop server is made through:
~~~
g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
~~~
* A *GraphTraversalSource* is created from the anonymous *traversal()* method where the "g" provided to the *DriverRemoteConnection* corresponds to the name of a *GraphTraversalSource* on the remote end.
* **Note :** Whenever changes are made in the local Knowledge graph, server must be re-started so that the changes are applied to the graph at remote end. This graph at the remote end is the main **Knowledge Graph**.
### 6. A keyword is taken as input from a user's query.
### 7. If Word or any Synonym of that word exist in the Graph, it selects that node otherwise return a message(data not present).
### 8. Using the choosen word as a starting point, the knowlege graph is traversed upto a specified depth and a subgraph is generated.
### 9. All the vertices and edges in the subgraph is stored in the *node[ ]* list and *edge[ ]* list respectively and finally retuns the data in tuple.   

