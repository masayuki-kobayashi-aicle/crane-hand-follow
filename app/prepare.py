"""Cache the pinned Google Hand / Pose Landmarkers, three.js (for /sim), their browser runtime and the SO-101 meshes (for MuJoCo)."""
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

PACKAGE = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22-rc.20250304/"
ASSETS = {"vision_bundle.mjs": PACKAGE + "vision_bundle.mjs"}
for variant in ("vision_wasm_internal", "vision_wasm_nosimd_internal"):
    for ext in ("js", "wasm"):
        name = f"{variant}.{ext}"
        ASSETS[name] = PACKAGE + "wasm/" + name
ASSETS["hand_landmarker.task"] = ("https://storage.googleapis.com/mediapipe-models/"
                                  "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
ASSETS["pose_landmarker_full.task"] = ("https://storage.googleapis.com/mediapipe-models/"
                                       "pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task")

ASSETS["three.module.min.js"] = "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js"

SHA256 = {
    "three.module.min.js": "3e690ac7d180b0aadf0891bea39eec643e29e2d3e75c99b18689518665f69ba6",
    "hand_landmarker.task": "fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1",
    "pose_landmarker_full.task": "5134a3aad27a58b93da0088d431f366da362b44e3ccfbe3462b3827a839011b1",
    "vision_bundle.mjs": "3252b10e0fd26c4095e4b6ee545c1c898120b3a3813388ecd4876abe6f1399a9",
    "vision_wasm_internal.js": "4a97e2520ba506c680ecd6ba6acfb146888afa0e2746d57f205352bc6ebb82eb",
    "vision_wasm_internal.wasm": "f00ec4731faa23b3e714d00e88d4d10e2df5c0a427d3a2b4ae6e3526fdd14ef7",
    "vision_wasm_nosimd_internal.js": "927def7b465c51b86e4b3060f93646aca4e27121f4b8fc0483786e407ea9cf1f",
    "vision_wasm_nosimd_internal.wasm": "3821ea9b1f7fb8c549ef2a064ef5c85750bf375c545a49fd6eea0df44a95f1f4",
}

# SO-101 の 3D メッシュ（TheRobotStudio/SO-ARM100、Apache-2.0）。コミットを固定して取得する。
SO_ARM_COMMIT = "141aea7bcac2744d92998e30268c413202a56f96"
MESH_URL = f"https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/{SO_ARM_COMMIT}/Simulation/SO101/assets/"
MESH_SHA256 = {
    "base_motor_holder_so101_v1.stl": "8cd2f241037ea377af1191fffe0dd9d9006beea6dcc48543660ed41647072424",
    "base_so101_v2.stl": "bb12b7026575e1f70ccc7240051f9d943553bf34e5128537de6cd86fae33924d",
    "motor_holder_so101_base_v1.stl": "31242ae6fb59d8b15c66617b88ad8e9bded62d57c35d11c0c43a70d2f4caa95b",
    "motor_holder_so101_wrist_v1.stl": "887f92e6013cb64ea3a1ab8675e92da1e0beacfd5e001f972523540545e08011",
    "moving_jaw_so101_v1.stl": "785a9dded2f474bc1d869e0d3dae398a3dcd9c0c345640040472210d2861fa9d",
    "rotation_pitch_so101_v1.stl": "9be900cc2a2bf718102841ef82ef8d2873842427648092c8ed2ca1e2ef4ffa34",
    "sts3215_03a_no_horn_v1.stl": "75ef3781b752e4065891aea855e34dc161a38a549549cd0970cedd07eae6f887",
    "sts3215_03a_v1.stl": "a37c871fb502483ab96c256baf457d36f2e97afc9205313d9c5ab275ef941cd0",
    "under_arm_so101_v1.stl": "d01d1f2de365651dcad9d6669e94ff87ff7652b5bb2d10752a66a456a86dbc71",
    "upper_arm_so101_v1.stl": "475056e03a17e71919b82fd88ab9a0b898ab50164f2a7943652a6b2941bb2d4f",
    "waveshare_mounting_plate_so101_v2.stl": "e197e24005a07d01bbc06a8c42311664eaeda415bf859f68fa247884d0f1a6e9",
    "wrist_roll_follower_so101_v1.stl": "4b17b410a12d64ec39554abc3e8054d8a97384b2dc4a8d95a5ecb2a93670f5f4",
    "wrist_roll_pitch_so101_v2.stl": "6c7ec5525b4d8b9e397a30ab4bb0037156a5d5f38a4adf2c7d943d6c56eda5ae",
}


def fetch(url, dest, expected):
    """expected と SHA-256 が一致するものだけ dest に置く。すでに一致していれば何もしない。"""
    if dest.is_file() and sha256(dest.read_bytes()).hexdigest() == expected:
        return
    print(f"取得中 {dest.name}", flush=True)
    with urlopen(url, timeout=60) as response:
        body = response.read()
    if sha256(body).hexdigest() != expected:
        raise RuntimeError(f"取得内容が不正: {url}")
    tmp = dest.with_suffix(".part")
    tmp.write_bytes(body)
    tmp.replace(dest)


def run():
    here = Path(__file__).resolve().parent
    folder = here / "assets"
    folder.mkdir(exist_ok=True)
    for name, url in ASSETS.items():
        fetch(url, folder / name, SHA256[name])
    print("カメラ用ファイルの準備完了")
    meshes = here / "sim_assets" / "SO101" / "assets"
    meshes.mkdir(parents=True, exist_ok=True)
    for name, expected in MESH_SHA256.items():
        fetch(MESH_URL + name, meshes / name, expected)
    print("SO-101 のメッシュの準備完了")


if __name__ == "__main__":
    run()
