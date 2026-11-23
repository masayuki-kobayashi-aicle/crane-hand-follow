# sim_assets

シミュレーション（`pickplace_sim.py`、`/sim`）が読む、SO-101 のロボットモデル。

| 場所 | 内容 |
|---|---|
| [`SO101/`](SO101/README.md) | SO-101 の URDF と MuJoCo（MJCF）の記述。`so101_new_calib.xml` と `scene.xml` を使う。出典とライセンスは `SO101/README.md` と `SO101/LICENSE`。 |

- `SO101/assets/`（3D メッシュ、約 19 MB）は Git の対象外。`python app/prepare.py` が、TheRobotStudio/SO-ARM100 の固定コミットから SHA-256 を検証して取得する。
- 公式モデルとして置いたもの。シミュレーション側の設定は `pickplace_sim.py`（`MODEL_XML` がここの `so101_new_calib.xml` を指す）。
