# 香港麻將環境：Godot 重製規格

這份文件描述現有 Python / Pygame 環境實際在玩的遊戲，目標是讓另一個人只靠這份規格，就能用 Godot 4 重做同一套對局、計番、分數、bot 與訓練紀錄。

程式識別名稱、JSON 欄位、番種 key、牌 id 保持英文，與現有 `FaanCalculator.py`、`Encoder.py`、`MahjongGUIEnv.py` 對得上。

## 先讀哪一份

| 文件 | 內容 |
| --- | --- |
| [01-rules.md](01-rules.md) | 牌張、座位、一局結構、吃碰槓胡、流局 |
| [02-turn-flow.md](02-turn-flow.md) | 狀態機、每個動作如何改手牌與牌牆、呼叫優先權 |
| [03-winning-and-scoring.md](03-winning-and-scoring.md) | 胡牌形、三番起糊、番種、互斥、分數表 |
| [04-players-ai-logs.md](04-players-ai-logs.md) | 人類 / heuristic bot / model bot、460 維特徵、log 格式 |
| [05-godot-project.md](05-godot-project.md) | Godot 專案結構、場景、腳本職責、移植清單 |
| [06-python-deviations.md](06-python-deviations.md) | Python 版未完成或與規則不一致的地方 |

## 重製時採哪一套行為

對局規則、胡牌、計番、分數、log 欄位，以 01 到 04 為準。那是這套環境設計要玩的香港麻將。

[06-python-deviations.md](06-python-deviations.md) 列出目前 Python 沒有做完的行為。Godot 版預設不要複製那些 bug。若目的是逐筆對上舊的 `raw_logs`，再依該文件把對應項目改回舊行為。影響最大的三項是：

- heuristic / model bot 在摸牌後永遠不自摸、不暗槓、不加槓
- `FaanCalculator.round` 從來沒有跟著圈風更新，圈風番實際永遠當東
- 搶槓、天胡、地胡有條目，但對局裡不會發生

## 遊戲一句話

四人香港麻將，無花牌，136 張。三番起糊，上限 10 番。食出由打出者一家付清，自摸由三家分付。一場比賽是東南西北四圈，每圈四局，莊家每局輪流，胡牌不連莊。分數從 0 累計，可以是負數。

## 名詞

| 中文 | 程式用字 | 意思 |
| --- | --- | --- |
| 番 | faan | 胡牌後的番數 |
| 食糊 / 胡 | `win` | 食出別人打的牌 |
| 自摸 | `self_drawn` | 摸牌胡 |
| 吃 | `chow` | 上家打出的牌，用手牌兩張組成順子 |
| 碰 | `pong` | 三張相同 |
| 明槓 | `kong` | 手牌已有三張，槓別人打出的第四張 |
| 暗槓 | `hidden_kong` | 手牌四張相同，自行槓出 |
| 加槓 | `additional_kong` | 已碰的刻子，再補第四張 |
| 門清 | `no_call` | 沒有任何副露（含暗槓、加槓） |
| 下家 | next | `(seat + 1) % 4` |
| 對家 | opposite | `(seat + 2) % 4` |
| 上家 | previous | `(seat + 3) % 4` |
| 流局 | draw | 牌牆摸完仍無人胡，分數不變 |
| 副露 | called tuple | 吃、碰、槓後公開的一組牌 |

座位與圈風都用 `0 東、1 南、2 西、3 北`。
