from unittest import TestCase
import os
import tempfile
import numpy as np
from aequilibrae.paths import Graph
from os.path import join
from uuid import uuid4
from .parameters_test import centroids
from aequilibrae.project import Project
from ...data import siouxfalls_project
from aequilibrae.paths.results import PathResults
from aequilibrae.paths import binary_version

# Adds the folder with the data to the path and collects the paths to the files
# lib_path = os.path.abspath(os.path.join('..', '../tests'))
# sys.path.append(lib_path)
from ...data import path_test, test_graph, test_network
from shutil import copytree, rmtree


class TestGraph(TestCase):
    def setUp(self) -> None:
        os.environ['PATH'] = os.path.join(tempfile.gettempdir(), 'temp_data') + ';' + os.environ['PATH']
        self.temp_proj_folder = os.path.join(tempfile.gettempdir(), uuid4().hex)
        copytree(siouxfalls_project, self.temp_proj_folder)

    def test_create_from_geography(self):
        self.graph = Graph()
        self.graph.create_from_geography(
            test_network,
            "link_id",
            "dir",
            "distance",
            centroids=centroids,
            skim_fields=[],
            anode="A_NODE",
            bnode="B_NODE",
        )
        self.graph.set_graph(cost_field="distance")
        self.graph.set_blocked_centroid_flows(block_centroid_flows=True)
        self.graph.set_skimming("distance")

    def test_prepare_graph(self):
        self.test_create_from_geography()
        self.graph.prepare_graph(centroids)

        reference_graph = Graph()
        reference_graph.load_from_disk(test_graph)
        reference_graph.__version__ = binary_version
        if not np.array_equal(self.graph.graph, reference_graph.graph):
            self.fail("Reference graph and newly-prepared graph are not equal")

    def test_set_graph(self):
        self.test_prepare_graph()
        self.graph.set_graph(cost_field="distance")
        self.graph.set_blocked_centroid_flows(block_centroid_flows=True)
        if self.graph.num_zones != centroids.shape[0]:
            self.fail("Number of centroids not properly set")
        if self.graph.num_links != 222:
            self.fail("Number of links not properly set")
        if self.graph.num_nodes != 93:
            self.fail("Number of nodes not properly set - " + str(self.graph.num_nodes))

    def test_save_to_disk(self):
        self.test_create_from_geography()
        self.graph.save_to_disk(join(path_test, "aequilibrae_test_graph.aeg"))
        self.graph_id = self.graph.__id__
        self.graph_version = self.graph.__version__

    def test_load_from_disk(self):
        self.test_save_to_disk()
        reference_graph = Graph()
        reference_graph.load_from_disk(test_graph)
        reference_graph.__version__ = binary_version

        new_graph = Graph()
        new_graph.load_from_disk(join(path_test, "aequilibrae_test_graph.aeg"))

        comparisons = [
            ("Graph", new_graph.graph, reference_graph.graph),
            ("b_nodes", new_graph.b_node, reference_graph.b_node),
            ("Forward-Star", new_graph.fs, reference_graph.fs),
            ("cost", new_graph.cost, reference_graph.cost),
            ("centroids", new_graph.centroids, reference_graph.centroids),
            ("skims", new_graph.skims, reference_graph.skims),
            ("link ids", new_graph.ids, reference_graph.ids),
            ("Network", new_graph.network, reference_graph.network),
            ("All Nodes", new_graph.all_nodes, reference_graph.all_nodes),
            ("Nodes to indices", new_graph.nodes_to_indices, reference_graph.nodes_to_indices),
        ]

        for comparison, newg, refg in comparisons:
            if not np.array_equal(newg, refg):
                self.fail("Reference %s and %s created and saved to disk are not equal" % (comparison, comparison))

        comparisons = [
            ("nodes", new_graph.num_nodes, reference_graph.num_nodes),
            ("links", new_graph.num_links, reference_graph.num_links),
            ("zones", new_graph.num_zones, reference_graph.num_zones),
            ("block through centroids", new_graph.block_centroid_flows, reference_graph.block_centroid_flows),
            ("Graph ID", new_graph.__id__, self.graph_id),
            ("Graph Version", new_graph.__version__, self.graph_version),
        ]

        for comparison, newg, refg in comparisons:
            if newg != refg:
                self.fail("Reference %s and %s created and saved to disk are not equal" % (comparison, comparison))

    def test_available_skims(self):
        self.test_set_graph()
        if self.graph.available_skims() != ["distance"]:
            self.fail("Skim availability with problems")

    def test_exclude_links(self):
        p = Project()
        p.open(self.temp_proj_folder)
        p.network.build_graphs()

        g = p.network.graphs['c']  # type: Graph

        # excludes a link before any setting or preparation
        g.exclude_links([12])

        g.set_graph('distance')
        r1 = PathResults()
        r1.prepare(g)
        r1.compute_path(1, 14)
        self.assertEqual(list(r1.path), [2, 6, 10, 34])

        # We exclude one link that we know was part of the last shortest path
        g.exclude_links([10])
        r2 = PathResults()
        r2.prepare(g)
        r2.compute_path(1, 14)
        self.assertEqual(list(r2.path), [2, 7, 36, 34])

        p.close()
