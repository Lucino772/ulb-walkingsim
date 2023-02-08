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

import pychrono as chrono


class Quadrupede:
    _trunk_collision_family = 2
    _trunk_dimensions = (0.5, 0.5, 0.5)

    def __init__(self, pos: tuple) -> None:
        self.__pos = chrono.ChVectorD(pos[0], pos[1], pos[2])

        self.__joints = []
        self.__bodies = []
        self.__sensor_data = []

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

    def _create_morphology(self):
        self._create_trunk()
        self._create_legs()

    def _create_trunk(self):
        trunk_part = self._create_bone(self._trunk_dimensions)
        trunk_part.GetCollisionModel().SetFamily(self._trunk_collision_family)
        trunk_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
            self._trunk_collision_family
        )
        trunk_part.SetPos(self.__pos)
        self.__bodies.append(trunk_part)

        # FIXME: For debug purposes
        # if index == 0:
        #     body_part.SetBodyFixed(True)


    def _create_body():
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

    def _apply_forces(self):
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
            distance = _distance(
                self.__sensor_data[-1]["position"],
                self.__sensor_data[0]["position"],
            )
            total_distance = functools.reduce(
                lambda prev, curr: (
                    prev[0]
                    if prev[1] is None
                    else prev[0]
                    + _distance(curr["position"], prev[1]["position"]),
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
