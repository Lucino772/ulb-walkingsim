"""
3D PyChrono muscle-based walking simulator
File: creature.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for basic bipede creature.
"""

import math
import typing as t
from collections import namedtuple

import pychrono as chrono

import walkingsim.utils.utils as utils

Vector = namedtuple("vector", ["x", "y", "z"])
VectorZero = Vector(0, 0, 0)


class CreatureBranch:
    def __init__(
        self,
        size: Vector,
        material,
        family,
        position: Vector = VectorZero,
        density=1000,
        visualize=True,
        collide=True,
        parent=None,
    ) -> None:
        self.__size = size
        self.__material = material
        self.__family = family

        self.__density = density
        self.__visualize = visualize
        self.__collide = collide
        self.__parent = parent
        self.__position = position
        self.__childs = []

        self.__body = self._create_body()
        self.__motor = None
        self.__link = None

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position

    @property
    def parent(self):
        return self.__parent

    @property
    def childs(self) -> t.List["CreatureBranch"]:
        return self.__childs

    @property
    def body(self):
        return self.__body

    @property
    def link(self):
        return self.__link

    @property
    def motor(self):
        return self.__motor

    def _create_body(self):
        body = chrono.ChBodyEasyBox(
            self.__size.x,
            self.__size.y,
            self.__size.z,
            self.__density,
            self.__visualize,
            self.__collide,
            self.__material,
        )
        body.SetBodyFixed(False)
        body.GetVisualShape(0).SetColor(chrono.ChColor(0.5, 0.7, 0.5))
        body.GetCollisionModel().SetFamily(self.__family)
        body.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
            self.__family
        )

        chrono_pos = chrono.ChVectorD(
            self.__position.x, self.__position.y, self.__position.z
        )
        body.SetPos(chrono_pos)

        return body

    def branch(self, size: Vector):
        _child = CreatureBranch(
            size, self.__material, self.__family, parent=self
        )
        self.__childs.append(_child)
        return _child

    def join(
        self,
        relative_pos: Vector = VectorZero,
        constraints_z: Vector = None,
        motor=None,
    ):
        if not isinstance(self.__parent, CreatureBranch):
            raise RuntimeError("Cannot create joint, body has not parent")

        parent_pos = self.__parent.position
        parent_size = self.__parent.size
        joint_pos = Vector(
            parent_pos.x + relative_pos.x,
            parent_pos.y - (parent_size.y / 2) + relative_pos.y,
            parent_pos.z + relative_pos.z,
        )
        self.__position = Vector(
            joint_pos.x, joint_pos.y - (self.__size.y / 2), joint_pos.z
        )
        chrono_joint_pos = chrono.ChVectorD(
            joint_pos.x, joint_pos.y, joint_pos.z
        )
        chrono_position = chrono.ChVectorD(
            self.__position.x, self.__position.y, self.__position.z
        )
        self.__body.SetPos(chrono_position)

        if motor == "torque":
            self.__motor = chrono.ChLinkMotorRotationTorque()
            _motor_frame = chrono.ChFrameD(chrono_joint_pos)
            self.__motor.Initialize(
                self.__parent.body, self.__body, _motor_frame
            )

        if constraints_z is not None:
            self.__link = chrono.ChLinkLockRevolute()
            self.__link.GetLimit_Rz().SetActive(True)
            self.__link.GetLimit_Rz().SetMin(constraints_z[0])
            self.__link.GetLimit_Rz().SetMax(constraints_z[1])
            self.__link.Initialize(
                self.__parent.body,
                self.__body,
                chrono.ChCoordsysD(chrono_joint_pos, chrono.QUNIT),
            )

        # If no link was set yet, use a fix link
        if self.__link is None:
            self.__link = chrono.ChLinkLockLock()
            self.__link.Initialize(
                self.__parent.body,
                self.__body,
                chrono.ChCoordsysD(chrono_joint_pos, chrono.QUNIT),
            )

        return self


class Creature:
    """
    Parent class for all creatures.

    Attributes:
        root
        sensor_data

    Methods:
        bodies: retrieve a list of all the bodies in the creature
        links: retrieve a list of all the links in the creature
        motors: retrieve a list of all the motors in the creature
    """

    def __init__(
        self, root_size: Vector, root_pos: Vector = VectorZero
    ) -> None:
        self.__material = chrono.ChMaterialSurfaceNSC()
        self.__material.SetFriction(0.5)
        self.__material.SetDampingF(0.2)
        self.__family = 2
        self.__sensor_data = []

        self.__root = CreatureBranch(
            root_size, self.__material, self.__family, position=root_pos
        )
        self.create()

    def create(self):
        raise NotImplementedError

    @property
    def root(self):
        return self.__root

    def bodies(self, root=None):
        if root is None:
            root = self.root

        _bodies = [root.body]
        for child in root.childs:
            _bodies.extend(self.bodies(root=child))
        return _bodies

    def links(self, root=None):
        if root is None:
            root = self.root

        _links = []
        if root.link is not None:
            _links.append(root.link)

        for child in root.childs:
            _links.extend(self.links(root=child))
        return _links

    def motors(self, root=None):
        if root is None:
            root = self.root

        _motors = []
        if root.motor is not None:
            _motors.append(root.motor)

        for child in root.childs:
            _motors.extend(self.motors(root=child))
        return _motors

    @property
    def pos(self):
        return chrono.ChVectorD(
            self.root.position.x, self.root.position.y, self.root.position.z
        )

    def joints_nbr(self) -> int:
        return len(self.motors())

    def get_nb_joints_at_limit(self):
        """
        Returns the nb of joints that are closer to their limit angles
        """
        nb_joints_at_limit = 0
        for link in self.links():
            max_angle = link.GetLimit_Rz().GetMax()
            min_angle = link.GetLimit_Rz().GetMin()
            current_angle = link.GetRelAngle()
            treshold = 0.99
            if current_angle >= (treshold * max_angle) or current_angle <= (
                treshold * min_angle
            ):
                nb_joints_at_limit += 1

        return nb_joints_at_limit

    @property
    def trunk_dim(self):
        return self.root.size

    def get_trunk_contact_force(self):
        # The contact force of the trunk is 0 when not touching anything,
        # and != 0 when touching something (e.g. the ground)
        return self.root.body.GetContactForce().Length()

    def set_forces(self, forces: list, timestep: float):
        if len(forces) < len(self.motors()):
            raise RuntimeError("Forces for joints are not enough")

        # Store the forces for later use
        self.__joints_forces = forces

        # NOTE: Important to store the function otherwise they are destroyed
        # when function is terminated, so chrono cannot access them anymore
        self.__joints_funcs = []

        for i, joint in enumerate(self.motors()):
            # print(forces[i])
            self.__joints_funcs.append(
                utils.ChCustomTorqueFunction(timestep, forces[i])
            )
            joint.SetTorqueFunction(self.__joints_funcs[i])

    def add_to_env(self, __env):
        for body in self.bodies():
            __env.Add(body)
        for joint in self.motors():
            __env.Add(joint)
        for link in self.links():
            __env.AddLink(link)

    def capture_sensor_data(self):
        self._capture_legs_sensors_data()

        # Distance calculation
        step_distance = 0
        total_distance = 0
        if len(self.__sensor_data) > 1:
            step_distance = utils.distance(
                self.__sensor_data[-1]["position"],
                self.__sensor_data[0]["position"],
            )

            # FIXME : Total distance is not calculated correctly
            for i, data in enumerate(self.__sensor_data[1:]):
                prev_pos = self.__sensor_data[i]
                distance_from_prev_pos = utils.distance(
                    data["position"], prev_pos["position"]
                )
                total_distance += distance_from_prev_pos

        # We update the last sensor data added with those additional information
        self.__sensor_data[-1].update(
            {"distance": step_distance, "total_distance": total_distance}
        )

    def _capture_legs_sensors_data(self):
        trunk_pos = self.root.body.GetPos()
        self.__sensor_data.append(
            {
                "position": (trunk_pos.x, trunk_pos.y, trunk_pos.z),
                "link_rotations": {},
            }
        )
        for b in range(len(self.motors())):
            rot = self.motors()[b].GetMotorRot()
            self.__sensor_data[-1]["link_rotations"].update({str(b): rot})

        front_left_leg_pos = self.root.childs[0].body.GetPos()
        self.__sensor_data[-1].update(
            {
                "front_left_leg_position": (
                    front_left_leg_pos.x,
                    front_left_leg_pos.y,
                    front_left_leg_pos.z,
                ),
                "link_rotations": {},
            }
        )

        front_right_leg_pos = self.root.childs[1].body.GetPos()
        self.__sensor_data[-1].update(
            {
                "front_right_leg_position": (
                    front_right_leg_pos.x,
                    front_right_leg_pos.y,
                    front_right_leg_pos.z,
                ),
                "link_rotations": {},
            }
        )

        back_left_leg_pos = self.root.childs[2].body.GetPos()
        self.__sensor_data[-1].update(
            {
                "back_left_leg_position": (
                    back_left_leg_pos.x,
                    back_left_leg_pos.y,
                    back_left_leg_pos.z,
                ),
                "link_rotations": {},
            }
        )

        back_right_leg_pos = self.root.childs[3].body.GetPos()
        self.__sensor_data[-1].update(
            {
                "back_right_leg_position": (
                    back_right_leg_pos.x,
                    back_right_leg_pos.y,
                    back_right_leg_pos.z,
                ),
                "link_rotations": {},
            }
        )

    @property
    def sensor_data(self):
        return self.__sensor_data
