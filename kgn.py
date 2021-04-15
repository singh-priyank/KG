from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
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
		return self.g.nodes

	def properties(self,vid):
		return self.g.nodes[vid]

	def add_vertex(self,label,prop):
		vertex = tuple([label,prop])
		vertex = [vertex]
		self.g.add_nodes_from(vertex)

	def add_multiple_vertex(self,nodes):
		self.g.add_nodes_from(nodes)

	def delete_vertex(self,vid):
		self.g.remove_node(vid)


class Edge:

	g = None

	def __init__(self,graph):
		self.g = graph

	def add_edge(self,id1,id2,prop):
		edge = tuple([id1,id2,prop])
		edge = [edge]
		self.g.add_edges_from(edge)
	
	def add_multiple_edges(self,edges):
		self.g.add_edges_from(edges)

	def delete_edge(self,id1,id2):
		self.g.remove_edge(id1,id2)

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
		l = len(G.nodes)+1
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
						G.add_nodes_from([(l,{"labelB":lemma[0].name()}),])
						G.add_edge(s[0],l)
						G.add_edge(e[0],l)
						l+=1

					# print(s[1]['labelV'],e[1]['labelV'],tt,s[0],e[0])
					# print(ib.wup_similarity(cb))

		return G



if __name__=="__main__":
	# gra = Import()
	# G3 = gra.import_graphml('g3.graphml')
	# G2 = gra.import_graphml('g2.graphml')
	
	# algo = Algo()
	# G = algo.join_graphs(G3,G2)
	# nx.write_graphml(G, "gf.graphml")

	#G = gra.import_graphml('gf.graphml')
	g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
	#g.addV('book').property('name', 'The French Chef Cookbook').property('year' , 1968).property('ISBN', '0-394-40135-2')
	#vet = Vertex(G)
	# ed = Edge(g)
	#print(vet.list_all())

	
	''' Add vertex '''
	# nodes = [(1, {'labelV': 'grade', 'grade_id': 'INT', 'name': 'VARCHAR'}), (2, {'labelV': 'course', 'course_id': 'INT', 'name': 'VARCHAR', 'grade_id': 'INT'}),
	# 		 (3, {'labelV': 'classroom', 'classroom_id': 'INT', 'grade_id': 'INT', 'section': 'VARCHAR', 'teacher_id': 'INT'}),
	# 		 (4, {'labelV': 'classroom_student', 'classroom_id': 'INT', 'studen_id': 'INT'}), (5, {'labelV': 'attendance', 'date': 'Date', 'student_id': 'INT', 'status': 'INT'}),
	# 		 (6, {'exam_type': 'INT', 'name': 'VARCHAR', 'labelV': 'exam_type'}), (7, {'exam_id': 'INT', 'exam_type': 'INT', 'name': 'VARCHAR', 'labelV': 'exam'}), 
	# 		 (8, {'labelV': 'exam_result', 'exam_id': 'INT', 'student_id': 'INT', 'course_id': 'INT'}), 
	# 		 (9, {'labelV': 'student', 'student_id': 'INT', 'email': 'VARCHAR', 'name': 'VARCHAR', 'dob': 'Date', 'parent_id': 'INT'}), 
	# 		 (10, {'labelV': 'parent', 'parent_id': 'INT', 'email': 'VARCHAR', 'password': 'VARCHAR', 'mobile': 'VARCHAR'}), 
	# 		 (11, {'teacher_id': 'INT', 'name': 'VARCHAR', 'email': 'VARCHAR', 'dob': 'Date', 'labelV': 'teacher'}) ]
	
	# edges = [(1, 2, {'labelE': 'has'}), (1, 3, {'labelE': 'has'}), (3, 4, {'labelE': 'has'}), (3, 11, {'labelE': 'has'}),
	# 		 (6, 7, {'labelE': 'has'}), (7, 8, {'labelE': 'has'}), (5, 9, {'labelE': 'has'}), (4, 9, {'labelE': 'has'}), 
	# 		 (2, 8, {'labelE': 'has'}), (9, 8, {'labelE': 'has'}), (9, 10, {'labelE': 'has'})]

	# nodes = [(12, {'labelV': 'Area', 'Area_id': 'INT', 'Name': 'VARCHAR', 'Subjects_id': 'INT'}), (13, {'labelV': 'Subject', 'Subject_id': 'INT', 'Abbreviation': 'VARCHAR', 'Area_id': 'INT', 'ScoreRecords_id': 'INT', 'SubjectGrades_id': 'INT'}), 
	# 		(14, {'labelV': 'SubjectGrade', 'SubjectGrade_id': 'INT', 'Grade_id': 'INT', 'Subject_id': 'INT'}), (15, {'labelV': 'Level', 'Level_id': 'INT', 'Name': 'VARCHAR', 'Principle': 'VARCHAR', 'Garde_id': 'INT'}), 
	# 		(16, {'labelV': 'Grade', 'Garde_id': 'INT', 'Name': 'VARCHAR', 'Level_id': 'INT', 'Observation': 'VARCHAR', 'Grade_paraleloes_id': 'INT', 'Subject_grades_id': 'INT'}), 
	# 		(17, {'labelV': 'ScoreRecord', 'ScoreRecord_id': 'INT', 'Subject_id': 'INT', 'Student_id': 'INT', 'FirstTrimester': 'VARCHAR', 'SecondTrimester': 'VARCHAR', 'ThirdTrimester': 'VARCHAR', 'FinalGrade': 'INT', 'Year': 'DATE'}), 
	# 		(18, {'labelV': 'Attendance', 'Attendance_id': 'INT', 'Student_id': 'INT', 'Attended': 'VARCHAR', 'Date': 'DATE'}), 
	# 		(19, {'labelV': 'Student', 'Student_id': 'INT', 'Garde_paralelo_id': 'INT', 'Rude': 'VARCHAR', 'Attendance_id': 'INT', 'ScoreRecords_id': 'INT', 'Name': 'VARCHAR', 'Father_name': 'VARCHAR', 'Mother_name': 'VARCHAR', 'Sex': 'VARCHAR', 'Date_of_Birth': 'DATE', 'Mobile_phone': 'VARCHAR', 'Address': 'VARCHAR'}), 
	# 		(20, {'labelV': 'GradeParalelo', 'Garde_paralelo_id': 'INT', 'Grade_id': 'INT', 'Staff_id': 'INT', 'Name': 'VARCHAR', 'Student_id': 'INT'}), 
	# 		(21, {'labelV': 'Staff', 'Staff_id': 'INT', 'Name': 'VARCHAR', 'Date_of_birth': 'DATE', 'Place_of_birth': 'VARCHAR', 'Sex': 'VARCHAR', 'Mobile_phone': 'INT', 'Address': 'VARCHAR', 'Father_name': 'VARCHAR', 'Mother_name': 'VARCHAR', 'Salary': 'VARCHAR', 'StaffType_id': 'INT', 'Garde_paralelos_id': 'INT'}), 
	# 		(22, {'labelV': 'User', 'Username': 'VARCHAR', 'Password': 'VARCHAR'}), (23, {'labelV': 'StaffType', 'Name': 'VARCHAR', 'Staff_id': 'INT'})]
	
	# edges = [(13, 12, {'labelE': 'Area_info'}), (14, 13, {'labelE': 'of_Subject'}), (17, 13, {'labelE': 'subject_info'}), 
	# 		(16, 14, {'labelE': 'level_info'}), (16, 15, {'labelE': 'has'}), (16, 20, {'labelE': 'has'}), 
	# 		(20, 19, {'labelE': 'has'}), (19, 17, {'labelE': 'has'}), (19, 18, {'labelE': 'has'}), 
	# 		(20, 21, {'labelE': 'has'}), (21, 23)]



	#g3 = gra.create_graph(nodes,edges)
	# vet = Vertex(G2)
	# print(vet.list_all())
	#nx.write_graphml(g3, "g3.graphml")








# vet.add_vertex('course',data)	
	#vet.delete_vertex('grade')
	# data = {'grade_id':'INT', 'name':'VARCHAR'}
	#vet.add_vertex('grade',data)
	# print(vet.list_all())
	#vet.add_vertex('4',data)
	#ed.add_edge('grade','course','')

	#nx.draw(G,with_labels=True)
	#plt.show()
	#nx.write_graphml(G1, "graph1.graphml")
	#print(vet.properties('142'))
