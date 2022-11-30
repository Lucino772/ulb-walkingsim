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


class Genotype(nx.Graph):
    def __init__(self):
        pass


class GenotypeNode:
    """
    Represents a node in the genotype directed graph, with information
    describing a rigid body part.

    Attributes:
        dimensions: 3-tuple with 3d size of the body part
        joint_type: joint type that sets constraints on relative motion
                    between the part and its parent
        recursive_limit: int stating how many times a phenotype should
                         add this part if adding it several times recursively
        neurons:
    """

    def __init__(self):
        self.dimensions = 0, 0, 0
        # TODO (see joint types in K. Sims paper and in PyChrono)
        self.joint_type
        self.recursive_limit = 0
        # TODO still have to define how to implement neurons
        self.neurons
        # TODO connections not necessary if using NetworkX lib
        self.connections


class GenotypeEdge:
    """
    Represents an edge in the genotype directed graph, with information
    describing a connection between a parent and a child node.

    Attributes:
        position: 3d position of attachment of a child to its parent, constrained
                  to be on the parent's surface
        orientation: an orientation matrix based on the child's parent
        scale: a scale matrix based on the child's parent
        reflection: a reflection matrix based on the child's parent
        terminal_only: boolean flag, which when set to True allows the connection
                       to be applied only when the recursive_limit of a node is
                       reached, for hand or tail-like parts
    """

    def __init__(self):
        self.position = 0, 0, 0
        self.orientation
        self.scale
        self.reflection

        self.terminal_only = False
