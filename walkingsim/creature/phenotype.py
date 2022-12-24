"""
3D PyChrono muscle-based walking simulator
File: phenotype.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for a walking creature.
"""

import pychrono as chrono

import walkingsim.creature.bone as bone


class Phenotype:
    def __init__(self, genotype, env):
        self.genotype = genotype
        self.env = env
        self.bones = []
        self.joints = []
        self._create_morphology()

    def _create_morphology(self):
        # TODO how to choose automatically position of spawned creature wrt
        # the position of the ground?
        # TODO establish rules for joint placement
        # and collision box reductions in procedural generation
        for node in self.genotype.nodes():
            parent_part = None
            if node == 1:  # Root node
                parent_part = bone.Bone(
                    self.genotype.nodes[node]["dimensions"],
                    chrono.ChVectorD(0, 1.9, 0),
                )
                parent_part.GetCollisionModel().SetFamily(2)
                parent_part.SetBodyFixed(True)
                parent_part.SetBodyFixed(False)
                # parent_part.SetBodyFixed(True)
                self.bones.append(parent_part)
                self.env.Add(parent_part)
            for edge in self.genotype.edges(
                nbunch=node  # nbunch :
                # iterable container of
                # nodes which will be
                # iterated through once.
                ,
                data=True,  # If True, return edge attribute
            ):
                new_node = edge[1]
                dimensions = self.genotype.nodes[new_node]["dimensions"]
                new_joint = chrono.ChLinkMotorRotationTorque()
                new_joint_pos = list(edge[2]["position"])
                # TODO different types of joints?
                joint_frame = chrono.ChFrameD(chrono.ChVectorD(*new_joint_pos))
                # TODO how to find position of new part based on parent's pos?
                child_part_pos = new_joint_pos
                # child_part_pos y -= child bone dimensions why y / 2
                # y / 2 because the joint is placed at the center of the bone
                # ?
                child_part_pos[1] -= dimensions[1] / 2  #
                child_part = bone.Bone(
                    dimensions, chrono.ChVectorD(*child_part_pos)
                )  # *child_part_pos : * unpacks the list
                child_part.GetCollisionModel().ClearModel()  #
                # ClearModel() : Remove all collision shapes from the model.
                # because we don't want collision between bones?
                child_part.GetCollisionModel().AddBox(
                    bone.Bone.bone_material,
                    dimensions[0] / 2,
                    dimensions[1] / 2,
                    dimensions[2] / 2,
                    chrono.ChVectorD(0, 0, 0),
                )
                child_part.GetCollisionModel().SetFamily(2)
                child_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
                    2
                )
                child_part.GetCollisionModel().BuildModel()
                self.bones.append(child_part)
                self.env.Add(child_part)
                new_joint.Initialize(parent_part, child_part, joint_frame)
                self.joints.append(new_joint)
                self.env.Add(new_joint)

        # XXX torque function test
        for i in range(len(self.joints)):
            mod = 1 if i % 2 == 0 else -1
            sin_torque = chrono.ChFunction_Sine(
                0  # phase [rad]
                # , 2  # frequency [Hz]
                ,
                1,  # frequency [Hz]
                mod * 290  # amplitude [Nm] Nm stands for Newton meter
                # , mod * 90  # amplitude [Nm] Nm stands for Newton meter
            )
            self.joints[i].SetTorqueFunction(sin_torque)
