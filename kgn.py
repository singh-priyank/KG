from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __, label, properties, to
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from nltk.corpus import wordnet
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import collections

class Node:
	def __init__(self,label,properties) -> None:
		self.label = label
		self.properties = properties

class Edge:
	def __init__(self,source,to) -> None:
		self.source = source
		self.to = to

class Query:

	# Given the string name find the numerical value of that node
	# So that traversal is possible
	def findNode(self, g, name) -> str:
		nodes = set(g.V().has('$'+name).toList())
		
		if len(nodes)==0:
			return None
		
		final_node = '0'
		for node in nodes:
			node_name = g.V(node).valueMap(True).toList()[0]['labelV'][0]
			if name == node_name:
				final_node = node
		if final_node == '0':
			final_node = list(nodes)[0]
		
		return final_node

	# Extract vertex from the graph 
	def extractVertex(self, g, graph)->list:
		tem_vertex = graph['@value']['vertices']
		nodes = []
		for v in tem_vertex:
			node_property = {}
			for p in g.V(v).properties():
				if p.label == 'labelV':
					name = p.value
				elif p.label == 'labelB':
					name = p.value
				elif p.label[0] != '$':
					node_property[p.label] = p.value
			nodes.append(tuple([name,node_property]))
		return nodes

	# Extract edges from the graph
	def extractEdges(self,g,graph):
		tem_edge = graph['@value']['edges']
		edges = []
		for edg in tem_edge:
			tem = str(edg).split('[')[2].replace('-edge-','').replace(']','')
			tem = tem.split('>')
			try:	
				start = g.V(tem[0]).valueMap(True).toList()[0]['labelV'][0]
			except:
				start = g.V(tem[0]).valueMap(True).toList()[0]['labelB'][0]
			try:
				end = g.V(tem[1]).valueMap(True).toList()[0]['labelV'][0]
			except:
				end = g.V(tem[1]).valueMap(True).toList()[0]['labelB'][0]
			edges.append((start,end))
		return tuple(edges)

	# Find tree of required depth 
	def findTrees(self, g, name, depth) -> Graph:
		node = self.findNode(g, name)
		if node == None:
			return
		
		# Find the subgraph of the given depth (direct function from tinkerPop)
		subGraph = g.V(node).repeat(__.bothE().subgraph('subGraph').bothV()).times(depth).cap('subGraph').next()
		
		nodes = self.extractVertex(g,subGraph)
		edges = self.extractEdges(g,subGraph)

		# Converting the nodes and edges to the objects of Node and Edge
		node_objects = []
		edge_objects = []
		
		for node in nodes:
			node_objects.append(Node(node[0],node[1]))
		for edge in edges:
			edge_objects.append(Edge(edge[0],edge[1]))

		return tuple(node_objects),tuple(edge_objects)
		
	# Find Descendant of the node upto particular depth
	def findDescendants(self, g, name, depth):
		node = self.findNode(g,name)
		if node == "No such node":
			return

		subGraph = g.V(node).repeat(__.bothE().subgraph('subGraph').bothV()).times(depth).cap('subGraph').next()

		tem_vertex = subGraph['@value']['vertices']

		nodes = []

		for ver in tem_vertex:
			for p in g.V(ver).properties():
				if p.label=='labelV':
					nodes.append((p.value,ver))
					break
		return tuple(nodes)

# Visualize the grph using networkx 
def draw(Gs):
	plt.figure(figsize=(4, 3))
	nx.draw(Gs,node_color='lightblue',with_labels=True,node_size=1000)
	plt.show()


if __name__=="__main__":


	''' Graph traversal '''
	g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
	
	
	name = input("Enter the word: ").lower()
	q = Query()
	height = int(input("Enter the height"))
	subGraph = q.findTrees(g, name, height)
	print(subGraph)
	# draw(subGraph)
	# print("Descendants")
	# print(q.findDescendants(g, name, 1))
	

