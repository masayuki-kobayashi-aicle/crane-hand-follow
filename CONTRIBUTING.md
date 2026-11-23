# Contributing

Thanks for your interest in crane-hand-follow. This project can move a real
robot arm, so the rules below are stricter than usual about safety and about what
has actually been tested.

## Ground rules

- **Safety first.** Do not add code that sends motion commands to the arm without
  the existing guards: per-joint speed and range limits, the stop on lost hand or
  lost input, and the same-origin checks on the server. Anything that can move
  the real arm needs a review by a maintainer and a description of how it was
  tested.
- **Say what you tested.** In a pull request, state whether you tested in
  simulation / mock mode only or on a real SO-101 (follower, firmware, how it was
  mounted). Behavior not confirmed on the real arm or in the browser must be
  marked "unverified" in the docs and in the UI.
- **No hardware or personal dumps.** Do not commit calibration files, `home.json`,
  `limits.json`, `palm.json`, `teach.json`, recorded videos, `debug/` logs,
  serial numbers, addresses of your network, tokens, or photos of your room.
  They are ignored by `app/.gitignore`; keep it that way.
- **Japanese or English** is fine for issues, pull requests and docs. Code
  comments in this repository are mostly Japanese; follow the language of the file
  you edit.
- **Small dependencies.** The server uses the Python standard library only. The
  simulation needs `numpy`, `mujoco` and `rerun-sdk` (see `requirements.txt`); the
  real arm needs `lerobot` (see `requirements-robot.txt`). Do not vendor third-party
  code or the SO-101 meshes into this repository; `app/prepare.py` fetches them
  with a pinned commit and SHA-256.

## Setup

Python 3.12 and Node 20 or newer.

```bash
git clone <this repository>
cd crane-hand-follow
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python app/prepare.py                  # downloads models, three.js and meshes (needs internet)
python app/server.py                   # mock mode: open http://127.0.0.1:8765/sim
```

## Tests

No robot, camera or `lerobot` is needed.

```bash
python -m unittest discover -s app -p "test_*.py"
node --test app/*.test.mjs app/test_sim_hand.mjs
```

## Pull requests

1. Open an issue first for anything larger than a small fix.
2. Keep the change focused. Add or update tests.
3. Make sure both test commands above pass.
4. Commit messages follow `<type>: <description>` (`feat`, `fix`, `refactor`,
   `docs`, `test`, `chore`, `perf`, `ci`).
5. By contributing you agree that your contribution is licensed under the MIT
   License of this project.

## Reporting security problems

Do not open a public issue. See [SECURITY.md](SECURITY.md).
