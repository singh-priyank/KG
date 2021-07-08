    '''
		Create grahml file from node and edge list
	'''
    # gra = Import()
	# syn = Synonym() 
	# nodes = syn.add_synonyms(nodes)          # Adding synonym to each node
	
	# G = gra.create_graph(nodes,edges)        # Creating the graph from node and edge list
	# nx.write_graphml(G, "g2.graphml")


    ''' Visualizing the knowledge graph '''
	# nx.draw(G2,with_labels=True)
	# plt.show()
	#nx.write_graphml(G1, "graph1.graphml")
	#print(vet.properties('142'))


    ''' 
		Import graphml file
	'''
    # gra = Import()
	# G3 = gra.import_graphml('g3.graphml')
	# G2 = gra.import_graphml('g2.graphml')
	
    ''' Calling join_graph function, to merge two graphml files    '''
	# algo = Algo()
	# G = algo.join_graphs(G2,G3)

    ''' Storing final graphml file back to the final file'''
	# nx.write_graphml(G, "gf.graphml")


	''' Graph traversal '''
	# g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
	
	
	''' Get all the nodes '''
	#l = g.with_('evaluationTimeout', 500).V().toList()

    ''' Query Graph '''
    # q = Query()
	# subGraph = q.findTrees(g, name, 1)      # Find Tree
	# print(subGraph)
	# print("Descendants")
	# print(q.findDescendants(g, name, 1))    # Find descendants 

    ''' Convert Gremlin graph to Python graph'''
    # graph = {}
	# edge = []
	# tem_edge = subGraph['@value']['edges']
	
	# for edg in tem_edge:
	# 	tem = str(edg).split('[')[2].replace('-edge-','').replace(']','')
	# 	tem = tem.split('>')
	# 	if tem[0] not in maping or tem[1] not in maping:
	# 		continue
	# 	if tem[0] not in graph:
	# 		graph[tem[0]] = []
	# 	graph[tem[0]].append(tem[1])

	# 	if tem[1] not in graph:
	# 		graph[tem[1]] = []
	# 	graph[tem[1]].append(tem[0])

	# 	edge.append(tuple(tem))
	# # print(graph)
