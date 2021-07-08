from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from nltk.corpus import wordnet
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import collections


class Query:
	# Given the string name find the numerical value of that node
	# So that traversal is possible
	def findNode(self,g,name):
		nodes = set(g.V().has('$'+name).toList())
		if len(nodes)==0:
			return "No such node"
		
		final_node = '0'
		for node in nodes:
			node_name = g.V(node).valueMap(True).toList()[0]['labelV'][0]
			if name == node_name:
				final_node = node
		if final_node == '0':
			final_node = list(nodes)[0]
		
		return final_node

	# Extract vertex from the graph 
	def extractVertex(self,g,graph):
		tem_vertex = graph['@value']['vertices']
		l = []
		for v in tem_vertex:
			for p in g.V(v).properties():
				if p.label=='labelV':
					l.append(p.value)
					break
		return tuple(l)

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
	def findTrees(self,g,name,depth):
		node = self.findNode(g,name)
		if node == "No such node":
			return
		subGraph = g.V(node).repeat(__.bothE().subgraph('subGraph').V()).times(depth).cap('subGraph').next()
		vertex = self.extractVertex(g,subGraph)
		edges = self.extractEdges(g,subGraph)
		return (vertex,edges)
		
	# Find Descendant of the node upto particular depth
	def findDescendants(self,g,name,depth):
		node = self.findNode(g,name)
		if node == "No such node":
			return

		subGraph = g.V(node).repeat(__.bothE().subgraph('subGraph').V()).times(depth).cap('subGraph').next()

		tem_vertex = subGraph['@value']['vertices']

		nodes = []

		for ver in tem_vertex:
			for p in g.V(ver).properties():
				if p.label=='labelV':
					nodes.append((p.value,ver))
					break
		return tuple(nodes)

	def bfs(graph,root,g):
		visited, queue = set(), collections.deque([(root,root)])
		removed = set()
		visited.add(root)

		while queue:

			# Dequeue a vertex from queue
			vertex = queue.popleft()
			if vertex[0] in removed or vertex[1] in removed:
				continue
			flag = 0
			for p in g.V(vertex[0]).properties():
				if p.label=='labelV':
					flag=1
					break
			if flag:
				print(maping[vertex[0]],end=' ')
				visited.add(vertex[0])
				for neighbour in graph[vertex[0]]:
					if neighbour not in visited:
						queue.append((neighbour,vertex[0]))
			else:
				print("...",maping[vertex[0]],maping[vertex[1]])
				visited.add(vertex[0])
				removed.add(vertex[0])
				for neighbour in graph[vertex[0]]:
					if neighbour not in visited:
						print(maping[neighbour],neighbour)
						response = input()
						if response == 'y' or response=='Y':
							graph[vertex[1]].append(neighbour)
							graph[neighbour].remove(vertex[0])
							graph[neighbour].append(vertex[1])

							queue.append((neighbour,vertex[1]))
						else:
							graph[neighbour].remove(vertex[0])
						graph.pop(vertex[0])
		return graph


if __name__=="__main__":

	''' 
		Import graphml file
	'''
	# gra = Import()
	# G3 = gra.import_graphml('g3.graphml')
	# G2 = gra.import_graphml('g2.graphml')
	
	# algo = Algo()
	# G = algo.join_graphs(G2,G3)
	# nx.write_graphml(G, "gf.graphml")

	#G = gra.import_graphml('gf.graphml')


	''' Graph traversal '''
	g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
	
	
	
	name = input("Enter the word: ")
	q = Query()
	subGraph = q.findTrees(g, name, 1)
	print(subGraph)
	print("Descendants")
	print(q.findDescendants(g, name, 1))
	

