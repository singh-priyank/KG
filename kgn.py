from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.structure.graph import Graph
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from nltk.corpus import wordnet


class Vertex:

	g = None
	def __init__(self,graph):
		self.g = graph
	
	def list_all(self):
		return self.g.with_('evaluationTimeout', 500).V().toList()
		#self.g.V().limit(limit).elementMap().toList()

	def properties(self,vid):
		data = dict()
		for p in self.g.V(vid).properties():
			data[p.label] =  p.value
		return data

	def add_vertex(self,label,prop):
		g.addV('vertex').property('labelV',label).next()
		for k in prop:
			g.V().has('labelV', label).property(k, prop[k]).iterate()

	def delete_vertex(self,vid):
		g.V(vid).drop()


class Edge:

	g = None

	def __init__(self,graph):
		self.g = graph

	def add_edge(self,label1,label2,prop):
		g.V().has('vertex','labelV',label1).addE(prop).to(g.V().has('vertex','labelV',label2))
		#g.V().has('vertex','labelV',label1).as('a').V().has('vertex','labelV',label2).addE(prop).to('a')


class Import:

	def __init__(self):
		self.graph = None

	def import_graphml(self, file_name):
		G1 = nx.read_graphml(file_name)
		G1 = G1.to_undirected()
		self.graph = G1
		return G1

	def create_graph(self, nodes, edges):
		G2 = nx.Graph()
		G2.add_nodes_from(nodes)
		G2.add_edges_from(edges)
		return G2

	def generate_subg(self, node_name, depth=3):

		ego_graph = nx.ego_graph(self.graph, node_name, radius=depth)
		
		# plot graph 
		nx.draw(ego_graph,with_labels=True)
		plt.show()

		return ego_graph


class Algo:
	def __init__(self):
		self.graph = None

	def join_graphs(self, graph1, graph2):

		'''  
			Converting two graph object to single object
			Adding vertex and edges can be done easily
		''' 
		G = nx.compose(graph1,graph2)

		# List of all nodes in a graph
		g1 = [node for node in graph1.nodes(data=True)]
		g2 = [node for node in graph2.nodes(data=True)]
        
		'''
			Iterate over each node and find similarity between the nodes
			If similarity is more than 50% add bridge node to connect both the nodes
		'''
		for s in g1:
			cb = wordnet.synsets(s[1]['labelV'])
			if len(cb)==0:
				continue
			cb = cb[0]

			for e in g2:
				ib = wordnet.synsets(e[1]['labelV'])
				if len(ib)==0:
					continue
				ib = ib[0]

                # Condition if similarity is more than 50% 
				if ib.wup_similarity(cb)>=0.5:
                    
					# Lowest hypernym will be bridge node
					bridgess = cb.lowest_common_hypernyms(ib)
					lemma = bridgess[0].lemmas()

					# If that node is already there add only new edge, else add vertex and edges

					if G.has_node(lemma[0].name()):
						G.add_edge(e[0],lemma[0].name())
					else:
						G.add_nodes_from([(lemma[0].name(),{"labelB":lemma[0].name()}),])
						G.add_edge(s[0],lemma[0].name())
						G.add_edge(e[0],lemma[0].name())

					# print(s[1]['labelV'],e[1]['labelV'],tt,s[0],e[0])
					# print(ib.wup_similarity(cb))

		return G



if __name__=="__main__":
	gra = Import()
	G1 = gra.import_graphml('my-graph.graphml')

	nodes = [('1', {"labelV": "college"}), ('2', {"labelV": "department"}), ('3', {"labelV": "professor"}), ('4', {"labelV": "student"}), ('5', {"labelV": "section"}), ]
	edges = [('1', '2'), ('1', '3'), ('1', '4'), ('4', '5')]
	G2 = gra.create_graph(nodes,edges)
	
	# algo = Algo()
	# G = algo.join_graphs(G1,G2)
	#nx.write_graphml(G, "g.graphml")

	g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
	#g.addV('book').property('name', 'The French Chef Cookbook').property('year' , 1968).property('ISBN', '0-394-40135-2')
	vet = Vertex(g)
	ed = Edge(g)
	#print(vet.list_all())

	''' Add vertex '''
	data = {'ISBN': '0-394-40135-2', 'year': 1968, 'name': 'The French Chef Cookbook'}
	vet.add_vertex('file',data)	

	#print(vet.list_all())
	ed.add_edge('book','file','has')

	
	#print(vet.properties('160'))
	

	subGraph = g.V('0').repeat(__.bothE().subgraph('subGraph').V()).times(1).cap('subGraph').next()
	#sg = traversal().withEmbedded(subGraph)
	#g.V('0').valueMap(True).toList()
	#print(subGraph)

	#print(g.with_('evaluationTimeout', 500).V().toList())

	#print(vet.list_all())





	# def find_vertex(self, vid):
	# 	return self.g.V(vid).elementMap().next()

	# def list_by_label_name(self, vlabel, name):
	# 	return self.g.V().has(vlabel, 'name', name).elementMap().toList()

	# def update_vertex(self, vid, name):
	# 	self.g.V(vid).property(Cardinality.single, 'name', name).next()