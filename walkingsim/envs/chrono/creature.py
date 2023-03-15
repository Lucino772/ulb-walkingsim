import typing as t

import pychrono as chrono

from walkingsim.creature.creature import _CreatureBody
from walkingsim.envs.chrono.utils import _tuple_to_chrono_vector


class ChronoCreatureBody(_CreatureBody):
    _DENSITY = 1000
    _MATERIAL = chrono.ChMaterialSurfaceNSC()
    _MATERIAL.SetFriction(0.5)
    _MATERIAL.SetDampingF(0.2)
    _BODY_COLOR = chrono.ChColor(0.5, 0.7, 0.5)

    def _create_body(self):
        self._body = chrono.ChBodyEasyBox(
            self._size[0],
            self._size[1],
            self._size[2],
            self._DENSITY,
            True,
            True,
            self._MATERIAL,
        )
        self._body.SetBodyFixed(False)
        self._body.GetVisualShape(0).SetColor(self._BODY_COLOR)
        self.collision(family=self._family, nocollision=[self._family])
        chrono_pos = _tuple_to_chrono_vector(self._position)
        self._body.SetPos(chrono_pos)

    # Methods
    def collision(
        self,
        family: t.Optional[int] = None,
        nocollision: t.Optional[t.Sequence[int]] = None,
        docollision: t.Optional[t.Sequence[int]] = None,
    ):
        if family is not None:
            self._body.GetCollisionModel().SetFamily(family)
            self._body.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
                family
            )
            for i in range(15):
                if i != family:
                    self._body.GetCollisionModel().SetFamilyMaskDoCollisionWithFamily(
                        i
                    )
            self._family = family

        if nocollision is not None:
            for fam in nocollision:
                self._body.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
                    fam
                )

        if docollision is not None:
            for fam in docollision:
                self._body.GetCollisionModel().SetFamilyMaskDoCollisionWithFamily(
                    fam
                )

        return self

    def branch(self, size: tuple, family: int = None, relpos: tuple = None):
        if family is None:
            family = self._family

        if relpos is None:
            relpos = (0, 0, 0)

        _position = (
            self._position[0] + relpos[0],
            self._position[1] + relpos[1],
            self._position[2] + relpos[2],
        )

        _child = ChronoCreatureBody(
            size, family, position=_position, parent=self
        )
        self._childs.append(_child)
        return _child

    def join(
        self,
        relpos: tuple = None,
        constraints_z: tuple = None,
        motor=None,
    ):
        if not isinstance(self._parent, ChronoCreatureBody):
            raise RuntimeError("Cannot create joint, body has not parent")

        if relpos is None:
            relpos = (0, 0, 0)

        joint_pos = _tuple_to_chrono_vector(
            (
                self._position[0] + relpos[0],
                self._position[1] + relpos[1],
                self._position[2] + relpos[2],
            )
        )

        if motor == "torque":
            self._motor = chrono.ChLinkMotorRotationTorque()
            _motor_frame = chrono.ChFrameD(joint_pos)
            self._motor.Initialize(self._parent.body, self._body, _motor_frame)

        if constraints_z is not None:
            self._link = chrono.ChLinkLockRevolute()
            self._link.GetLimit_Rz().SetActive(True)
            self._link.GetLimit_Rz().SetMin(constraints_z[0])
            self._link.GetLimit_Rz().SetMax(constraints_z[1])
            self._link.Initialize(
                self._parent.body,
                self._body,
                chrono.ChCoordsysD(joint_pos, chrono.QUNIT),
            )

        # If no link was set yet, use a fix link
        if self._link is None:
            self._link = chrono.ChLinkLockLock()
            self._link.Initialize(
                self._parent.body,
                self._body,
                chrono.ChCoordsysD(joint_pos, chrono.QUNIT),
            )

        return self
