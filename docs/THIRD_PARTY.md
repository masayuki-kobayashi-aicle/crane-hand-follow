# Third-party components

This repository's own code is MIT-licensed. The components below are **not** part
of the MIT grant; they keep their own licenses. Nothing here is vendored except the
text model files under `app/sim_assets/SO101/`. Everything else is downloaded by
`app/prepare.py` or `pip` on your machine.

| Component | Use | License | Source |
|---|---|---|---|
| SO-ARM100 / SO-101 model (MJCF, URDF, STL meshes) | Simulation model | Apache-2.0 | <https://github.com/TheRobotStudio/SO-ARM100> (commit `141aea7`) |
| MediaPipe Tasks Vision (JS and WASM runtime) | Hand / pose detection in the browser | Apache-2.0 | <https://github.com/google-ai-edge/mediapipe> (npm `@mediapipe/tasks-vision` 0.10.22-rc.20250304) |
| MediaPipe Hand Landmarker and Pose Landmarker models | Hand / pose detection | See the model cards | <https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker> |
| three.js r160 | 3D view of `/sim` | MIT | <https://github.com/mrdoob/three.js> |
| MuJoCo | Physics simulation | Apache-2.0 | <https://github.com/google-deepmind/mujoco> |
| NumPy | Numerics | BSD-3-Clause | <https://numpy.org> |
| Rerun SDK | Replay of recorded runs (`sim_replay.py`, `replay.py`) | MIT or Apache-2.0 | <https://github.com/rerun-io/rerun> |
| LeRobot (optional) | Driving a real SO-101 | Apache-2.0 | <https://github.com/huggingface/lerobot> |

## Notes

- The SO-101 files in `app/sim_assets/SO101/` are copied from SO-ARM100 and keep its
  Apache-2.0 license; the license text is `app/sim_assets/SO101/LICENSE`.
  The STL meshes are not stored here.
- `app/prepare.py` writes the MediaPipe runtime, models and three.js to
  `app/assets/`, which is git-ignored. Each file is checked against a SHA-256 hash
  recorded in `prepare.py`. These files are not redistributed by this repository,
  and their license terms apply to you when you download them.
- Names such as SO-101, LeRobot, MediaPipe and MuJoCo belong to their owners and
  are used only to say what this project works with.
