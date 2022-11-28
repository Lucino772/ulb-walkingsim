"""
3D PyChrono muscle-based walking simulator
File: genotype_node.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for a node in the genotype directed graph.
"""


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
        # TODO (see joint types in K. Sims paper)
        # self.joint_type
        self.recursive_limit = 0
        # TODO still have to define how to implement neurons
        # self.neurons
        # TODO connections not necessary if using NetworkX lib
        # self.connections
