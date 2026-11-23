"""試験用の定数。実機で測った値ではない。

HOME は「グリッパーが机に接した、肘を曲げた姿勢」の代用で、reach_map の可動域の内側にある（高さは机の面とほぼ同じ）。
実機の初期姿勢はユーザーごとに違い、`home.json`（Git の対象外）に保存される。
"""

HOME = {"shoulder_pan": 0.0, "shoulder_lift": -35.0, "elbow_flex": 70.0, "wrist_flex": 45.0, "wrist_roll": 0.0}
