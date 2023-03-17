import math

import pychrono as chrono

from walkingsim.creature.bipede import Bipede
from walkingsim.creature.quadrupede import Quadrupede
from walkingsim.envs.chrono.creature import ChronoCreatureBody
from walkingsim.envs.chrono.utils import _tuple_to_chrono_vector
from walkingsim.envs.chrono.visualizer import ChronoVisualizer


class ChCustomTorqueFunction(chrono.ChFunction_SetpointCallback):
    def __init__(self, value: float):
        super().__init__()
        self.__value = value

    def SetpointCallback(self, t: float):
        return self.__value


class ChronoEnvironment:
    def __init__(self, visualize: bool = False, creature: str = "quadrupede"):
        self.__environment = chrono.ChSystemNSC()
        if creature == "quadrupede":
            self.__creature_cls = Quadrupede
        else:
            self.__creature_cls = Bipede

        self.__creature = None

        self.__visualize = visualize
        self.__visualizer = None

        # Materials & Colors
        self.__ground_material = chrono.ChMaterialSurfaceNSC()
        self.__ground_color = chrono.ChColor(0.5, 0.7, 0.3)

        # Observations
        self.__observations = []

    @property
    def observations(self):
        return self.__observations

    @property
    def creature_shape(self):
        return self.__creature_cls._CREATURE_MOTORS

    @property
    def time(self):
        return self.__environment.GetChTime()

    @property
    def closed(self):
        if self.__visualizer:
            return not self.__visualizer.check()

        return False

    def reset(self, properties: dict):
        self.__environment.Clear()
        self.__environment.SetChTime(0)  # NOTE: Is this necessary ?
        self.__observations.clear()

        # Set environment properties
        gravity = properties.get("gravity", (0, -9.81, 0))
        self.__environment.Set_G_acc(_tuple_to_chrono_vector(gravity))
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

        # Add ground
        ground_size = (100, 5, 200)
        ground = chrono.ChBodyEasyBox(
            ground_size[0],  # Xsize
            ground_size[1],  # Ysize
            ground_size[2],  # Zsize
            4000,  # Density
            True,  # Collide
            True,  # Visualize
            self.__ground_material,  # Material
        )
        ground.SetBodyFixed(True)
        ground.SetPos(chrono.ChVectorD(0, -ground_size[1] / 2, 0))
        ground.GetVisualShape(0).SetColor(self.__ground_color)
        ground.GetVisualShape(0).SetTexture(
            "resources/materials/floor/dirty_concrete.jpg",
            scale_x=10,
            scale_y=10,
        )
        self.__environment.Add(ground)

        # Add creature
        self.__creature = self.__creature_cls(
            ChronoCreatureBody, (0, self.__creature_cls._CREATURE_HEIGHT, 0)
        )
        for body in self.__creature.bodies():
            self.__environment.Add(body)
        for joint in self.__creature.motors():
            self.__environment.Add(joint)
        for link in self.__creature.links():
            self.__environment.AddLink(link)

        self._gather_observations()
        if self.__visualizer:
            self.__visualizer.refresh()

    def step(self, action, timestep: float):
        self._apply_forces(action.tolist())
        self.__environment.DoStepDynamics(timestep)
        self._gather_observations()

    def render(self):
        if self.__visualize and self.__visualizer is None:
            self.__visualizer = ChronoVisualizer(self.__environment)
            self.__visualizer.setup()

        if self.__visualizer is not None:
            self.__visualizer.render()
            self.__visualizer.check()

    def close(self):
        if self.__visualizer is not None:
            self.__visualizer.close()

    # private methods
    def _apply_forces(self, action: list):
        if len(action) < len(self.__creature.motors()):
            raise RuntimeError("Forces for joints are not enough")

        # NOTE: Important to store the function otherwise they are destroyed
        # when function is terminated, so chrono cannot access them anymore
        self.__joints_funcs = []

        for i, joint in enumerate(self.__creature.motors()):
            self.__joints_funcs.append(ChCustomTorqueFunction(action[i]))
            if isinstance(joint, chrono.ChLinkMotorRotationTorque):
                joint.SetTorqueFunction(self.__joints_funcs[i])
            elif isinstance(joint, chrono.ChLinkMotorRotationAngle):
                joint.SetAngleFunction(self.__joints_funcs[i])

    def _get_nb_joints_at_limit(self):
        """
        Returns the nb of joints that are closer to their limit angles
        """
        nb_joints_at_limit = 0
        for link in self.__creature.links():
            max_angle = link.GetLimit_Rz().GetMax()
            min_angle = link.GetLimit_Rz().GetMin()
            current_angle = link.GetRelAngle()
            treshold = 0.99
            if current_angle >= (treshold * max_angle) or current_angle <= (
                treshold * min_angle
            ):
                nb_joints_at_limit += 1

        return nb_joints_at_limit

    def _gather_observations(self):
        nb_joints_at_limit = self._get_nb_joints_at_limit()

        # The contact force of a body is 0 when not touching anything,
        # and != 0 when touching something (e.g. the ground)
        trunk_hit_ground = (
            self.__creature.root.body.GetContactForce().Length() != 0
        )
        legs_hit_ground = False
        # FIXME target only the thighs of the quadrupede here, to check
        # if they touch the ground
        for i in range(0, len(self.__creature.motors()) // 2):
            if (
                self.__creature.root.childs[i].body.GetContactForce().Length()
                != 0
            ):
                legs_hit_ground = True

        # Get position and rotation of trunk
        trunk_pos = self.__creature.root.body.GetPos()
        self.__observations.append(
            {
                "position": (trunk_pos.x, trunk_pos.y, trunk_pos.z),
                "link_rotations": {},
            }
        )
        for i, motor in enumerate(self.__creature.motors()):
            rot = motor.GetMotorRot()
            self.__observations[-1]["link_rotations"].update({str(i): rot})

        # Distance calculation
        step_distance = 0
        if len(self.__observations) > 1:

            step_distance = (
                self.__observations[-1]["position"][0]
                - self.__observations[0]["position"][0]
            )

        # We update the last sensor data added with those additional information
        self.__observations[-1].update(
            {
                "distance": step_distance,
                "joints_at_limits": nb_joints_at_limit,
                "trunk_hit_ground": trunk_hit_ground,
                "legs_hit_ground": legs_hit_ground,
            }
        )
