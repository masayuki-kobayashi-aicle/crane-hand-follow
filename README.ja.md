# crane-hand-follow

Web カメラの前の素手で、小型ロボットアーム（SO-101）を操作する。親指と人差し指をつまむとグリッパーが閉じ、手を動かすとアームが動く。
同じ手の認識で遊べる MuJoCo の「クレーンゲーム」シミュレーション（お菓子をつかんで、机の穴へ落とす）も入っている。ロボットは要らない。

English: [README.md](README.md)

> **警告: 実機のロボットアームを動かします。** 実機モードは実験的で、**安全は保証しません**。実機・ブラウザーで確かめていない部分があり、下の表と画面に「未確認」と書いてあります。電源をすぐ切れる位置で使い、グリッパーに指を入れないでください。実行する前に[セキュリティの考え方](#セキュリティの考え方)を読んでください。MIT ライセンスの「現状のまま」で提供します。

**非公式の個人プロジェクト**です。TheRobotStudio（SO-ARM100 / SO-101）、Hugging Face（LeRobot）、Google（MediaPipe）などとは無関係で、承認も受けていません。ハッカソンの試作から始まりました。

## できること

- **手に追従する。** MediaPipe の Hand / Pose Landmarker をブラウザーの中で動かす。映像は PC の外へ出ない。手の位置と親指・人差し指の距離を、アームの台座・高さ・前後・グリッパーに対応づける。モーターごとの速度・可動範囲の制限、追従開始時の基準、手や入力が途切れたときの停止つき。
- **ロボットなしで動く。** `--port` を付けなければ、サーバーが模擬アームで動く。
- **シミュレーション（`/sim`・`/sim/camera`）。** MuJoCo の SO-101 でお菓子をつかみ、机の穴へ落とす。キーボードでも、カメラの前の手でも操作できる。狙い補助・つかみ補助は切れる。
- **実機の SO-101（任意）。** LeRobot（Feetech）経由。校正は自分で行う。

## はじめかた（シミュレーション・ロボット不要）

Python 3.12 と、Chromium 系ブラウザー。Web カメラは `/sim/camera` だけに要る。

```bash
git clone <このリポジトリ>
cd crane-hand-follow
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python app/prepare.py          # 固定したモデル・three.js・SO-101 のメッシュを取得し、SHA-256 を検証
python app/server.py           # 127.0.0.1:8765 で待つ
```

<http://127.0.0.1:8765/sim>（キーボード）か <http://127.0.0.1:8765/sim/camera>（手の認識）を開く。起動直後は止まっているので「スタート」を押す。キーは `W` `S` 前後、`A` `D` 左右、`↑` `↓` 高さ、`Space` グリッパー、`R` やり直し。詳しくは[ガイド](docs/GUIDE.ja.md)。

`app/prepare.py` は約 50 MB を取得する。SO-101 のメッシュはこのリポジトリに入れず、[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)（Apache-2.0）の固定コミットから取る。

## 実機（任意・自己責任）

```bash
pip install -r requirements-robot.txt
# LeRobot の公式ツールで校正してから
python app/server.py --port /dev/ttyACM0 --robot-id <校正に使った ID>
```

<http://127.0.0.1:8765/> を開くと、４点の登録から追従まで画面が案内する。手順の全体は [docs/GUIDE.ja.md](docs/GUIDE.ja.md)。サーバーの接続時・終了時にトルクが切り替わるので、腕は安定した休止姿勢で支えてから繋ぐ。

## 確認できていること

2026-11-23 時点。

| 対象 | 状態 |
|---|---|
| 自動テスト | Python 288 件・Node 28 件が通る。ロボット・カメラ・LeRobot は不要。 |
| 手認識 → 模擬アーム → 録画 | Chrome で、手のテスト画像を模擬カメラに入れて確認（作者の Mac）。 |
| 実機（SO-101）の追従 | 作者の実機で、グリッパー・肩・肘・台座・手首の追従を動かして向きを確認。IK 追従（既定オフ）・手首の曲げの向きは**未確認**。 |
| シミュレーション（`/sim`・`/sim/camera`） | API とサーバー側は curl とテストで確認。**今回の公開準備では、ブラウザーでの目視確認をやり直していない。** |
| 骨格版（`/skeleton`）・教示（`/teach`） | **ブラウザーでの動作は未確認。** 教示データから関節値の対応を解く処理は未実装。 |
| やわらかモード | 実機で手で押しても動かず、**未解決**。 |

シミュレーションの物理（机・お菓子・穴）は仮置きの値で、実測ではない。デモでつかめるように調整してあり、現実的な接触モデルではない。

## セキュリティの考え方

- サーバーは `127.0.0.1` だけで待ち、認証も TLS もない。自分の PC の中で使う前提。ネットワークへ公開したり、ポート転送したりしないこと。
- `POST` は `Host` と `Origin` が一致し、期待する Content-Type のときだけ受ける。ブラウザーの別のページから動かされるのを防ぐ。動かす要求には、追従開始時に発行するセッションごとのトークンも付く。
- カメラ映像の処理はブラウザーの中。録画やログは、このPCの `app/debug/`（Git 管理外）にだけ書く。
- ソフトウェアの停止は、認証された安全機能ではない。

脆弱性は非公開で報告してください。[SECURITY.md](SECURITY.md) を参照。

## 構成

| パス | 内容 |
|---|---|
| `app/server.py` | HTTP サーバー、操作卓のロジック、`/sim` のサービス |
| `app/*.js`・`*.html` | 画面（操作卓・シミュレーション・カメラ操作・骨格・教示） |
| `app/ik_*.py`・`reach_map.py`・`pickplace_sim.py` | IK と MuJoCo のピック＆プレース |
| `app/prepare.py` | 固定したダウンロードと SHA-256 検証 |
| `app/sim_assets/` | SO-101 の MJCF / URDF（メッシュは取得） |
| `docs/` | ガイド（日本語）と第三者ライセンス |

## 開発

[CONTRIBUTING.md](CONTRIBUTING.md) を参照。テスト:

```bash
python -m unittest discover -s app -p "test_*.py"
node --test app/*.test.mjs app/test_sim_hand.mjs
```

## ライセンス

MIT。[LICENSE](LICENSE) を参照。第三者の部品と SO-101 のモデルは、それぞれのライセンスに従う。[docs/THIRD_PARTY.md](docs/THIRD_PARTY.md) を参照。
