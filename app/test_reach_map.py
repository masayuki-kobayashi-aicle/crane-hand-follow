import unittest

import reach_map
from testdata import HOME

# 較正は実機の値でなく、近い値の代用（試験を、どの環境でも同じ結果にする）
CALIBRATION = {j: {"range_min": 800, "range_max": 3300} for j in ("shoulder_lift", "elbow_flex", "wrist_flex")}
UNITS = reach_map.joint_units(CALIBRATION)


class EnvelopeTests(unittest.TestCase):
    def test_home_pose_is_inside(self):
        self.assertTrue(reach_map.inside_envelope(HOME, UNITS))

    def test_pose_above_height_limit_is_outside(self):
        pose = {"shoulder_lift": -30.0, "elbow_flex": 0.0, "wrist_flex": 0.0}      # 腕をほぼ水平に伸ばした高い姿勢
        self.assertGreater(reach_map.height_above_desk(pose, UNITS), reach_map.HEIGHT_MAX)
        self.assertFalse(reach_map.inside_envelope(pose, UNITS))

    def test_shoulder_back_swing_is_outside(self):
        self.assertFalse(reach_map.inside_envelope({**HOME, "shoulder_lift": -60.0}, UNITS))

    def test_clamp_stops_before_the_outside(self):
        want = {"shoulder_lift": -30.0, "elbow_flex": 0.0, "wrist_flex": 0.0}
        got = reach_map.clamp_to_envelope(want, HOME, UNITS)
        self.assertTrue(reach_map.inside_envelope(got, UNITS))
        self.assertNotEqual(got, want)

    def test_clamp_keeps_inside_target(self):
        self.assertEqual(reach_map.clamp_to_envelope(HOME, HOME, UNITS), HOME)


class TargetTests(unittest.TestCase):
    def test_every_hand_input_gives_a_pose_inside_the_envelope(self):
        anchor = reach_map.tip_of(HOME, UNITS)[0]
        safe = {j: float(HOME[j]) for j in reach_map.USABLE}
        steps = [i / 4 for i in range(-4, 5)]
        for reach in steps:
            for height in steps:
                _, pose = reach_map.target(reach, height, anchor, UNITS, safe)
                self.assertTrue(reach_map.inside_envelope(pose, UNITS), (reach, height, pose))

    def test_fully_extended_hand_straightens_the_elbow_and_reaches_far(self):
        # 利用者の指摘（2026-11-22）: 腕を伸ばしても肘が浅く、遠くへ届かない。伸ばし切ると腕がほぼまっすぐ（まっすぐ＝肘 約 -75）になること
        anchor = reach_map.tip_of(HOME, UNITS)[0]
        safe = {j: float(HOME[j]) for j in reach_map.USABLE}
        (x, z), pose = reach_map.target(1.0, 0.0, anchor, UNITS, safe)
        self.assertGreaterEqual(x, 0.43)
        self.assertLessEqual(pose["elbow_flex"], -55.0)
        self.assertLessEqual(z - reach_map.Z_DESK, 0.02)             # 机の高さで届いている（宙に上がって稼いでいない）

    def test_extending_the_hand_moves_the_tip_forward_not_up(self):
        anchor = reach_map.tip_of(HOME, UNITS)[0]
        safe = {j: float(HOME[j]) for j in reach_map.USABLE}
        (x0, z0), _ = reach_map.target(0.0, 0.0, anchor, UNITS, safe)
        (x1, z1), _ = reach_map.target(1.0, 0.0, anchor, UNITS, safe)
        self.assertGreater(x1 - x0, 0.10)
        self.assertLess(z1 - z0, 0.05)

    def test_neutral_maps_input_range_around_the_base(self):
        self.assertEqual(reach_map.neutral(0, 0.0, 1.0, 0.4), 0.4)
        self.assertEqual(reach_map.neutral(1, 0.0, 1.0, 0.4), 1.0)
        self.assertEqual(reach_map.neutral(-1, 0.0, 1.0, 0.4), 0.0)


if __name__ == "__main__":
    unittest.main()
