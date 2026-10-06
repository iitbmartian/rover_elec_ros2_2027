import math
from typing import List


class VroomVroom:
    def __init__(self, half_width=0.35, half_length=0.45, speed_scalar=250, r_scalar=1, deadzone=0.0):
        self.a = half_width
        self.b = half_length
        self.speed_scalar = speed_scalar
        self.r_scalar = r_scalar
        self.deadzone = deadzone

    def magnitude(self, vec) -> float:
        return (vec[0] ** 2 + vec[1] ** 2) ** 0.5

    def angle(self, vec) -> float:
        return math.atan2(vec[1], vec[0])

    def smooooth_operatorrrr(self, throttle: float, rotate: float, crab: float) -> List[List[float]]:
        """
        Smooth Operator mode: the rover moves on a circular path with radius
        of curvature and velocity set by joystick input.
        :param throttle: Throttle of Joystick (from -1 to 1)
        :param rotate: Rotate of Joystick (from -1 to 1)
        :param crab: Crab of Joystick (from -1 to 1)
        :return: [angles_deg, vels], both length-4 lists, wheel order FR, BL, FL, BR
        """
        if abs(throttle) <= self.deadzone:
            throttle = 0
        if abs(rotate) <= self.deadzone:
            rotate = 0
        if abs(crab) <= self.deadzone:
            crab = 0

        flipper = False
        rinv = math.tan(rotate * (math.pi / 2 - 0.01))
        if rinv == 0:
            R = 10 ** 5
        else:
            R = self.r_scalar / rinv
        if R < 0:
            flipper = not flipper
        theta = -crab * math.pi / 2
        if theta > 0:
            flipper = not flipper
            theta -= math.pi
        R_vec = [R * math.cos(theta), R * math.sin(theta)]
        angles, vels = self.from_R_vec(R_vec, flipper)
        max_vel = max(vels)
        if max_vel > 0:
            for i in range(len(vels)):
                vels[i] *= self.speed_scalar * throttle / max_vel
        return [angles, vels]

    def from_R_vec(self, R_vec, flipper):
        angles = [0.0] * 4
        vels = [0.0] * 4
        w1 = [self.a - R_vec[0], self.b - R_vec[1]]
        w2 = [self.a - R_vec[0], -self.b - R_vec[1]]
        w3 = [-self.a - R_vec[0], self.b - R_vec[1]]
        w4 = [-self.a - R_vec[0], -self.b - R_vec[1]]
        w_vecs = [w1, w2, w3, w4]
        for i in range(4):
            angles[i] = self.angle(w_vecs[i]) - math.pi
            vels[i] = self.magnitude(w_vecs[i])
        if flipper:
            for i in range(4):
                angles[i] += math.pi
        for i in range(4):
            angles[i] *= 180 / math.pi
            while angles[i] > 180:
                angles[i] -= 360
            while angles[i] < -180:
                angles[i] += 360
        return [angles, vels]

    def watering_well(self, frontz, sidez, yaww):
        if frontz == 0:
            frontz = 10 ** (-5)
        R_vec = [-frontz, -sidez]
        vel_mag = self.magnitude(R_vec)
        if yaww == 0:
            yaww = 10 ** (-10)
        R_vec[0] /= yaww
        R_vec[1] /= yaww
        flipper = True
        if yaww < 0:
            flipper = not flipper
        if frontz < 0:
            flipper = not flipper
        angles, vels = self.from_R_vec(R_vec, flipper)
        max_vel = max(vels)
        if max_vel > 0:
            for i in range(len(vels)):
                vels[i] *= self.speed_scalar * self.magnitude([vel_mag, yaww]) / max_vel
                if frontz < 0:
                    vels[i] *= -1
        return [angles, vels]
