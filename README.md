# crane-hand-follow

Control a small robot arm (SO-101) with your bare hand in front of a webcam. Pinch
your thumb and index finger to close the gripper, move your hand to move the arm.
Includes a MuJoCo "crane game" simulation (pick up a snack and drop it in a hole)
that you can play with the same hand tracking, without any robot.

日本語: [README.ja.md](README.ja.md)

> **Warning: this can move a real robot arm.** The real-arm mode is experimental
> and **safety is not guaranteed**. Parts of it have not been tested on a real arm
> or in a browser; the table below and the UI say which. Keep the power switch
> within reach, keep your fingers out of the gripper, and read
> [Security model](#security-model) before running it. Everything is provided
> "as is" under the MIT License.

This is an **unofficial, personal project**. It is not affiliated with or endorsed
by TheRobotStudio (SO-ARM100 / SO-101), Hugging Face (LeRobot), Google (MediaPipe)
or any other third party. It started as a hackathon prototype.

## What it does

- **Follows a hand.** MediaPipe Hand / Pose Landmarker run in the browser; the video
  never leaves your machine. The hand position and the thumb-index distance are
  mapped to the arm's base, height, reach and gripper, with per-joint speed and
  range limits, a baseline taken when following starts, and a stop when the hand or
  the input is lost.
- **Runs without a robot.** With no `--port`, the server runs a mock arm.
- **Simulation (`/sim`, `/sim/camera`).** MuJoCo SO-101 picks up a snack and drops
  it through a hole in the table. Drive it with the keyboard, or with your hand in
  front of the camera. Optional aim and grab assists can be switched off.
- **Real SO-101 (optional).** Through LeRobot with a Feetech bus, after your own
  calibration.

## Quick start (simulation, no robot)

Python 3.12 and a Chromium-based browser with a webcam (the webcam is needed only
for `/sim/camera`).

```bash
git clone <this repository>
cd crane-hand-follow
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python app/prepare.py          # downloads pinned models, three.js and SO-101 meshes, checks SHA-256
python app/server.py           # listens on 127.0.0.1:8765
```

Open <http://127.0.0.1:8765/sim> (keyboard) or <http://127.0.0.1:8765/sim/camera>
(hand tracking). The simulation starts stopped; press "Start". Keys: `W` `S` forward
/ back, `A` `D` left / right, `↑` `↓` height, `Space` gripper, `R` restart. See the
[guide](docs/GUIDE.ja.md) (Japanese) for details.

`app/prepare.py` downloads about 50 MB. The SO-101 meshes are not stored in this
repository; they are fetched from a pinned commit of
[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) (Apache-2.0).

## Real arm (optional, at your own risk)

```bash
pip install -r requirements-robot.txt
# calibrate once with LeRobot's own tool, then:
python app/server.py --port /dev/ttyACM0 --robot-id <your calibration id>
```

Then open <http://127.0.0.1:8765/>. The page walks you through registering four
positions and then following. The full procedure (in Japanese) is in
[docs/GUIDE.ja.md](docs/GUIDE.ja.md). Support the arm in a stable rest pose before
connecting: torque is switched when the server connects and exits.

## What is verified

Status as of 2026-11-23.

| Area | Status |
|---|---|
| Automated tests | Python 288 and Node 28 tests pass. No robot, camera or LeRobot needed. |
| Hand detection to mock arm to recording | Checked in Chrome with a test image fed as a fake camera (author's Mac). |
| Following a real SO-101 | Gripper, shoulder, elbow, base and wrist following were run on the author's arm and the directions checked. IK following (off by default) and the wrist-bend direction are **unverified**. |
| Simulation (`/sim`, `/sim/camera`) | API and server side checked with curl and tests. **Not re-checked by eye in a browser for this release.** |
| Skeleton (`/skeleton`) and teaching (`/teach`) pages | **Unverified in a browser.** Solving the joint mapping from teaching data is not implemented. |
| "Soft mode" | Did not move when pushed by hand on the real arm. **Unresolved.** |

Simulation physics (table, snack, hole) use placeholder values, not measurements.
The grip is tuned so the demo works, so it is not a realistic contact model.

## Security model

- The server binds to `127.0.0.1` only and has no authentication and no TLS. It is
  meant for your own machine. Do not expose it to a network or port-forward it.
- `POST` requests are accepted only with matching `Host` and `Origin` headers and
  the expected content type, which blocks other web pages in your browser. Motion
  requests also carry a per-session token issued when following starts.
- Camera video is processed in the browser. Optional recordings and logs are
  written under `app/debug/` (git-ignored) only on your machine.
- The software stop is not a certified safety function.

Report vulnerabilities privately; see [SECURITY.md](SECURITY.md).

## Layout

| Path | Contents |
|---|---|
| `app/server.py` | HTTP server, desk logic, `/sim` service |
| `app/*.js`, `*.html` | Browser UIs: desk, simulation, camera control, skeleton, teaching |
| `app/ik_*.py`, `reach_map.py`, `pickplace_sim.py` | IK and the MuJoCo pick-and-place |
| `app/prepare.py` | Pinned downloads with SHA-256 checks |
| `app/sim_assets/` | SO-101 MJCF / URDF (meshes are fetched) |
| `docs/` | Guide (Japanese) and third-party notices |

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md). Tests:

```bash
python -m unittest discover -s app -p "test_*.py"
node --test app/*.test.mjs app/test_sim_hand.mjs
```

## License

MIT, see [LICENSE](LICENSE). Third-party components and the SO-101 model are
covered by their own licenses; see [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md).
