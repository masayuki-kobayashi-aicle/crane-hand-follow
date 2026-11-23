# Changelog

All notable changes are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0] - 2026-11-23

### Added
- Initial public version, extracted from a hackathon project.
- A local web desk that follows the hand seen by a webcam (MediaPipe Hand and
  Pose Landmarker, run in the browser) with an SO-101 arm: gripper, shoulder,
  elbow, base and wrist, with per-joint speed and range limits, a baseline
  taken at the start of following, and a stop on lost hand or lost input.
- A mock mode that needs no robot, and a MuJoCo pick-and-place simulation
  (`/sim`, and `/sim/camera` driven by the hand in front of the camera).
- `app/prepare.py`, which downloads the pinned models, three.js and the SO-101
  meshes and checks their SHA-256.

### Notes
- Parts are unverified on a real robot or in a browser. The guide and the UI
  say which. See the README, "What is verified".
