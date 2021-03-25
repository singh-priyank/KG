from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import Column
from gremlin_python.process.traversal import Direction
from gremlin_python.process.traversal import Operator
from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions
from gremlin_python.structure.graph import Graph
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from nltk.corpus import wordnet


class Import:

	def __init__(self):
		self.graph = None

	def import_graphml(self, file_name):
		G1 = nx.read_graphml(file_name)
		G1 = G1.to_undirected()

		nx.draw(G1,with_labels=True)
		#plt.show()
		self.graph = G1
		return G1

	def create_graph(self, nodes, edges):
		G2 = nx.Graph()
		G2.add_nodes_from(nodes)
		G2.add_edges_from(edges)
		nx.draw(G2,with_labels=True)
		#plt.show()
		print(G2.nodes(data=True))
		#self.graph = G2
		return G2

	def generate_subg(self, node_name, depth=3):

		ego_graph = nx.ego_graph(self.graph, node_name, radius=depth)
		# plot to check
		nx.draw(ego_graph,with_labels=True)
		plt.show()

		return ego_graph

class Algo:
	def __init__(self):
		self.graph = None

	def join_graphs(self, graph1, graph2):

		G = nx.compose(graph1,graph2)

		g1 = [node for node in graph1.nodes(data=True)]
		g2 = [node for node in graph2.nodes(data=True)]
		
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
				#print(s[1]['labelV'],e[1]['labelV'],ib.wup_similarity(cb))
				# Condition if similarity is more than 50% and path is already not there 
				if ib.wup_similarity(cb)>=0.5:
					G.add_edge(s[0],e[0])
					tt='........'
					print(s[1]['labelV'],e[1]['labelV'],tt,s[0],e[0])
					print(ib.wup_similarity(cb))
		#self.graph = G
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
	print(g.with_('evaluationTimeout', 500).V().toList())


	#
	subGraph = g.V('0').repeat(__.bothE().subgraph('subGraph').V()).times(1).cap('subGraph').next()
	#sg = traversal().withEmbedded(subGraph)
	#g.V('0').valueMap(True).toList()
	print(subGraph)