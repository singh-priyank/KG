from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from nltk.corpus import wordnet
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import collections
import pandas as pd




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

    # Import already existing graph
    def import_graphml(self, file_name):
        G1 = nx.read_graphml(file_name)
        G1 = G1.to_undirected()
        self.graph = G1
        return G1

    # Generate new graph from node and edge list
    def create_graph(self, nodes, edges):
        G2 = nx.Graph()
        G2.add_nodes_from(nodes)
        G2.add_edges_from(edges)
        return G2

    # Generate subgraph upto some depth
    def generate_subg(self, node_name, depth=3):

        ego_graph = nx.ego_graph(self.graph, node_name, radius=depth)
        
        # plot graph 
        # nx.draw(ego_graph,with_labels=True)
        # plt.show()

        return ego_graph


class Algo:
    def __init__(self):
        self.graph = None

    def join_graphs(self, graph1, graph2):

        '''  
            Converting two graph object to single object
            So that Adding vertex and edges can be done easily
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
            if 'labelV' in s[1]:
                cb = wordnet.synsets(s[1]['labelV'])
            else:
                continue
            if len(cb)==0:
                continue
            cb = cb[0]

            for e in g2:
                if 'labelV' in e[1]:
                    ib = wordnet.synsets(e[1]['labelV'])
                else:
                    continue
                if len(ib)==0:
                    continue
                ib = ib[0]
                if s[1]['labelV'].lower() == e[1]['labelV'].lower():
                    for i in e[1]:
                        if i not in s[1]:
                            s[1][i] = e[1][i]
                    edg = list(G.edges(e[0]))
                    for i in range(len(edg)):
                        #print([s[0],edg[i][1],{'labelE': 'has'}])
                        G.add_edges_from([(s[0],edg[i][1],{'labelE': 'has'})])
                    G.remove_node(e[0])
                    continue
                # Condition if similarity is more than 50% 
                if ib.wup_similarity(cb)>=0.5:

                    # Lowest hypernym will be bridge node
                    bridgess = cb.lowest_common_hypernyms(ib)
                    lemma = bridgess[0].lemmas()

                    # If that node is already there add only new edge, else add vertex and edges

                    if G.has_node(lemma[0].name()):
                        G.add_edge(e[0],lemma[0].name())
                    else:
                        G.add_nodes_from([(str(l),{"labelB":lemma[0].name().lower()}),])
                        G.add_edges_from([(s[0],str(l),{'labelE': 'has'})])
                        G.add_edges_from([(e[0],str(l),{'labelE': 'has'})])
                        l+=1

                    # print(s[1]['labelV'],e[1]['labelV'],end="...............")
                    # print(ib.wup_similarity(cb), lemma[0].name())

        return G

class Synonym:
    def find_synonyms(self,string):
        synonym_words = []
        synonym_words.append(string)
        try:
            # Remove whitespace before and after word and use underscore between words
            stripped_string = string.strip()
            fixed_string = stripped_string.replace(" ", "_")
            #print(f"{fixed_string}:")

            # Set the url using the amended string
            my_url = f'https://thesaurus.plus/thesaurus/{fixed_string}'
            # Open and read the HTMLz
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()

            # Parse the html into text
            page_soup = soup(page_html, "html.parser")
            word_boxes = page_soup.find("ul", {"class": "list paper"})
            results = word_boxes.find_all("div", "list_item")

            # Iterate over results and print
            for result in results:
                synonym_words.append(result.text.strip().lower())

        except HTTPError:
            pass

        return synonym_words

    def add_synonyms(self,nodes):
        for node in nodes:
            synonyms = self.find_synonyms(node[1]['labelV'])
            for syn in synonyms:
                node[1]['$'+syn] = 'Synonym'

        return nodes

class Excel:
    def convert_nodes(self,path,n):
        edges,nodes = [],[]
        xls = pd.ExcelFile(path)
        df = xls.parse(0)
        mapping = {}
        for index, row in df.iterrows():
            if row['SourceTable'] not in mapping:
                mapping[row['SourceTable']] = [n,row['SourceTableKey']]
                n+=1
            if row['TargetTable'] not in mapping:
                mapping[row['TargetTable']] = [n,row['TargetTableKey']]
                n+=1
            edges.append(tuple([mapping[row['SourceTable']][0],mapping[row['TargetTable']][0],{'labelE':row['RelationName']}]))
    #         print(row['SourceTable'],row['TargetTable'])
        
        for name in mapping:
            key = mapping[name][1]
            node_attr = {}
            attr_name, attr_type = [],[]
            for tables in range(1,len(mapping)+1):
                next_df = xls.parse(tables)
                if key in list(next_df['Column Name']):
                    attr_name = list(next_df['Column Name'])
                    attr_type = list(next_df['Column Type'])
                    break
                    
            for i in range(len(attr_name)):
                node_attr[attr_name[i]] = attr_type[i]
            node_attr['labelV'] = name.lower()
            nodes.append(tuple([mapping[name][0],node_attr]))

        return nodes,edges


if __name__=="__main__":

    ''' 
        Import graphml file
    '''
    gra = Import()
    ex = Excel()
    algo = Algo()
    syn = Synonym() 

    nodes,edges = ex.convert_nodes('test.xlsx',1)
    nodes = syn.add_synonyms(nodes)
    Gf = gra.create_graph(nodes,edges)
    # nx.write_graphml(Gf, "tf.graphml")

    file_list = ['test1.xls']
    for file in file_list:
        nodes,edges = ex.convert_nodes(file,len(Gf)+1)
        syn = Synonym() 
        nodes = syn.add_synonyms(nodes)
        G = gra.create_graph(nodes,edges)
        # nx.write_graphml(G, "t.graphml")
        
        Gf = algo.join_graphs(G,Gf)
    
    nx.write_graphml(Gf, "tf.graphml")