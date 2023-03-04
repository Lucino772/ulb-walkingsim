"""
3D PyChrono muscle-based walking simulator
File: phenotype.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Classes for generating creatures.
"""

import functools
import json
import math
import os

import networkx as nx
import pychrono as chrono

import walkingsim.utils.utils as utils


class CreatureGenerator:
    """Class to generate creatures based on a JSON file.

    Each JSON file describes a creature genotype as a directed graph.

    Nodes describe bones and have the following attributes:
    - dimensions: 3-tuple with 3d size of the body part
    - joint_type: joint type that sets constraints on relative motion between
                  the part and its parent
    - recursive_limit: int stating how many times a phenotype should
                       add this part if adding it several times recursively
    - neurons

    Edges describe connections between a parent and a child node and have the
    following attributes:
    - position: 3d position of attachment of a child to its parent, constrained
                to be on the parent's surface
    - orientation: an orientation matrix based on the child's parent
    - scale: a scale matrix based on the child's parent
    - reflection: a reflection matrix based on the child's parent
    - terminal_only: boolean flag, which when set to True allows the connection
                     to be applied only when the recursive_limit of a node is
                     reached, for hand or tail-like parts
    """

    def __init__(self, __datapath: str, __engine: str) -> None:
        self.__datapath = __datapath
        self.__engine = __engine

        self.__creature = {"chrono": ChronoCreature}

    def generate_creature(self, __creature: str):
        filename = os.path.join(self.__datapath, f"{__creature}.json")
        with open(filename, "r") as fp:
            creature_spec = json.load(fp)

        nodes = [(node["id"], node["meta"]) for node in creature_spec["nodes"]]

        edges = [
            (*edge["nodes"], edge["meta"]) for edge in creature_spec["edges"]
        ]

        creature_graph = nx.MultiDiGraph()
        creature_graph.add_nodes_from(nodes)
        creature_graph.add_edges_from(edges)

        return self.__creature[self.__engine](
            __creature, creature_graph, (0, 1.9, 0)
        )


class ChronoCreature:
    """Class to create a creature for the `chrono` engine based on a directed
    graph, which represents the creature genotype.
    """

    _collision_family = 2

    def __init__(
        self, __creature: str, __graph: nx.Graph, pos: tuple, movement_matrix
    ) -> None:
        self.__creature = __creature
        self.__graph = __graph
        self.__pos = chrono.ChVectorD(pos[0], pos[1], pos[2])

        self.__joints = []
        self.__bodies = []
        self.__sensor_data = []

        self.__movement_matrix = movement_matrix

        self._create_morphology()

    def _create_bone(self, size: tuple):
        bone_material = chrono.ChMaterialSurfaceNSC()
        bone_material.SetFriction(0.5)
        bone_material.SetDampingF(0.2)
        #  bone_material.SetCompliance(0.0005)
        #  bone_material.SetComplianceT(0.0005)

        bone = chrono.ChBodyEasyBox(
            size[0], size[1], size[2], 1000, True, True, bone_material
        )
        bone.SetBodyFixed(False)
        bone.GetVisualShape(0).SetColor(chrono.ChColor(0.5, 0.7, 0.5))

        return bone

    def _create_body(
        self, index: int, pos: chrono.ChVectorD, recursive_cnt: int = 0
    ):
        meta = self.__graph.nodes[index]
        body_part = self._create_bone(meta["dimensions"])
        body_part.GetCollisionModel().SetFamily(self._collision_family)
        body_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
            self._collision_family
        )
        body_part.SetPos(pos)
        self.__bodies.append(body_part)

        # FIXME: For debug purposes
        # if index == 0:
        #     body_part.SetBodyFixed(True)

        for (edge_node1, edge_node2, edge_meta) in self.__graph.edges(
            nbunch=index, data=True
        ):
            # TODO different types of joints?
            # TODO: Add constraints on the joints
            joint = chrono.ChLinkMotorRotationTorque()
            joint_pos = (
                pos.x + edge_meta["position"][0],
                pos.y + edge_meta["position"][1],
                pos.z + edge_meta["position"][2],
            )
            joint_frame = chrono.ChFrameD(chrono.ChVectorD(*joint_pos))

            do_create_body = True
            recursive_limit = self.__graph.nodes[edge_node2]["recursive_limit"]
            if edge_node1 == edge_node2 and recursive_cnt >= recursive_limit:
                do_create_body = False

            if do_create_body:
                _recursive_cnt = (
                    recursive_cnt + 1 if edge_node1 == edge_node2 else 0
                )

                node2_dim = self.__graph.nodes[edge_node2]["dimensions"]
                node2_body_part_pos = (
                    joint_pos[0],
                    joint_pos[1] - node2_dim[1] / 2,
                    joint_pos[2],
                )
                node2_body_part = self._create_body(
                    edge_node2,
                    chrono.ChVectorD(*node2_body_part_pos),
                    _recursive_cnt,
                )

                joint.Initialize(body_part, node2_body_part, joint_frame)
                self.__joints.append(joint)

        return body_part

    def _create_morphology(self):
        # TODO how to choose automatically position of spawned creature wrt
        # the position of the ground?
        # TODO establish rules for joint placement
        # and collision box reductions in procedural generation
        self._create_body(0, self.__pos)

        # XXX torque function test
        for i, joint in enumerate(self.__joints):
            mod = 1 if i % 2 == 0 else -1
            sin_torque = chrono.ChFunction_Sine(
                0, 1, mod * 90  # phase [rad]  # frequency [Hz]
            )  # amplitude [Nm]
            joint.SetTorqueFunction(sin_torque)

    def add_to_env(self, __env):
        for body in self.__bodies:
            __env.Add(body)

        for joint in self.__joints:
            __env.Add(joint)

    def capture_sensor_data(self):
        # We capture the information from basic sensors (position, rotation, etc.)
        pos = self.__bodies[0].GetPos()
        self.__sensor_data.append({"position": (pos.x, pos.y, pos.z)})

        # We compute additional information (distance, total distance, etc.)
        distance = 0
        total_distance = 0
        if len(self.__sensor_data) > 1:
            distance = utils.distance(
                self.__sensor_data[-1]["position"],
                self.__sensor_data[0]["position"],
            )
            total_distance = functools.reduce(
                lambda prev, curr: (
                    prev[0]
                    if prev[1] is None
                    else prev[0]
                    + utils.distance(curr["position"], prev[1]["position"]),
                    curr,
                ),
                self.__sensor_data,
                (0, None),
            )[0]

        # We update the last sensor data added with those additional information
        self.__sensor_data[-1].update(
            {"distance": distance, "total_distance": total_distance}
        )

    @property
    def sensor_data(self):
        return self.__sensor_data
