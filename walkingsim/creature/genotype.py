"""
3D PyChrono muscle-based walking simulator
File: genotype.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Classes for a genotype, represented as a directed graph.
"""
import networkx as nx

from walkingsim.auto_indent import *

from walkingsim._logging import logger
logger.debug("Starting genotype.py")

sys.stdout = AutoIndent(sys.stdout)


class Genotype(nx.MultiDiGraph):
    """
    Representing a creature genotype as a directed graph.

    Nodes describe bones and have the following attributes:
        dimensions - 3-tuple with 3d size of the body part
        joint_type - joint type that sets constraints on relative motion
                    between the part and its parent
        recursive_limit - int stating how many times a phenotype should
                         add this part if adding it several times recursively
        neurons -

    Edges describe connections between a parent and a child node and have the
    following attributes:
        position - 3d position of attachment of a child to its parent, constrained
                  to be on the parent's surface
        orientation - an orientation matrix based on the child's parent
        scale - a scale matrix based on the child's parent
        reflection - a reflection matrix based on the child's parent
        terminal_only - boolean flag, which when set to True allows the connection
                       to be applied only when the recursive_limit of a node is
                       reached, for hand or tail-like parts
    """

    def __init__(self, nodes_list, connections_list):
        """
        Args:
            nodes_list - a list of 2-tuples consisting of (node_nb, attributes_dict)
                        for each node
            connections_list - a list of 3-tuples consisting of (father_node_nb,
                              child_node_nb, attributes_dict)
        """
        super().__init__()
        print("Genotype.__init__")
        logger.debug("Genotype.__init__")

        # logger.debug(["node: {}", node] for node in nodes_list)
        self.add_nodes_from(nodes_list)
        # logger.debug("connection: {}".format(
        #     connection for connection in connections_list))
        self.add_edges_from(connections_list)
