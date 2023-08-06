import numpy as np


class MultiThreadedAoN:
    def __init__(self):
        # The predecessors for each node in the graph
        self.predecessors = None

        # holds the skims for all nodes in the network (during path finding)
        self.temporary_skims = None

        # Keeps the order in which the nodes were reached for the cascading network loading
        self.reached_first = None
        # The previous link for each node in the tree
        self.connectors = None
        # Temporary results for assignment. Necessary for parallelization
        self.temp_link_loads = None
        # Temporary nodes for assignment. Necessary for cascading
        self.temp_node_loads = None
        #  holds the b_nodes in case of flows through centroid connectors are blocked
        self.temp_b_nodes = None

    # In case we want to do by hand, we can prepare each method individually
    def prepare(self, graph, results):
        itype = graph.default_types("int")
        ftype = graph.default_types("float")
        self.predecessors = np.zeros((results.nodes, results.cores), dtype=itype)
        if results.num_skims > 0:
            self.temporary_skims = np.zeros((results.nodes, results.num_skims, results.cores), dtype=ftype)
        else:
            self.temporary_skims = np.zeros((1, 1, results.cores), dtype=ftype)
        self.reached_first = np.zeros((results.nodes, results.cores), dtype=itype)
        self.connectors = np.zeros((results.nodes, results.cores), dtype=itype)
        self.temp_link_loads = np.zeros((results.links, results.classes["number"], results.cores), dtype=ftype)
        self.temp_node_loads = np.zeros((results.nodes, results.classes["number"], results.cores), dtype=ftype)
        self.temp_b_nodes = np.zeros((graph.b_node.shape[0], results.cores), dtype=itype)
        for i in range(results.cores):
            self.temp_b_nodes[:, i] = graph.b_node[:]
