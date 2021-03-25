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


g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
print(g.with_('evaluationTimeout', 500).V().toList())
#g.io("/home/priyank/Documents/activity/my-graph.graphml")
#with(IO.reader, IO.graphml):
    #read().iterate()
#g.io("/home/priyank/Documents/activity/graph.json").read().iterate()
#g.io(graphml()).readGraph('my-graph.graphml')  
vertices = g.with_('evaluationTimeout', 500).V().out('belongs_to').toList()
print(vertices)


    # graph = Graph()
    # connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    # # The connection should be closed on shut down to close open connections with connection.close()
    # g = graph.traversal().withRemote(connection)

    # herculesAge = g.V().has('name', 'hercules').values('age').next()
