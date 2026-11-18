# 05 Godot 專案

用 Godot 4.x，腳本用 GDScript。畫面與規則分開：規則腳本不參考 `Sprite2D` 或滑鼠，測試才能不開視窗跑。

## 目錄

```text
res://
  project.godot
  assets/tiles/          # 1m.png … 7z.png，沿用現有檔名
  data/match_config.json
  scenes/
    main.tscn            # 根節點，掛 Match
    table.tscn           # 桌面、四個座位、棄牌池、分數
    tile.tscn            # 一張牌的 Sprite
    action_bar.tscn      # 胡、碰、槓、吃、過、自摸
  scripts/
    autoload/config.gd
    core/tile_catalog.gd
    core/tile.gd
    core/player.gd
    core/match.gd
    core/calls.gd
    core/win_checker.gd
    core/faan_calculator.gd
    core/score_table.gd
    ai/heuristic_policy.gd
    ai/feature_encoder.gd
    ai/model_policy.gd
    log/match_logger.gd
    ui/table_view.gd
    ui/seat_view.gd
    ui/action_bar.gd
  tests/                 # Gut 或 Godot 內建測試，移植 TestFaanCal 的手牌
  logs/
```

`project.godot` 的主場景是 `scenes/main.tscn`。視窗先設 1920×1080，拉伸用 `canvas_items`，這樣牌的相對位置和舊版接近。四方桌是呈現層的選擇，不要寫進 `Match`。

## 場景怎麼分

`main.tscn` 只有 `Match` 與 `TableView`。`Match` 在規則狀態改變時發出信號，`TableView` 聽信號改畫面。

```text
Main
  Match                 # scripts/core/match.gd
  TableView
    Background          # Color(34/255, 139/255, 34/255)
    DiscardRow
    Seat0 .. Seat3      # 每家：Hand、Melds、NameScore
    Hud                 # 圈風、局數、總分
    ActionBar
    ChowPicker
```

建議信號：

| 信號 | 參數 | 誰來畫 |
| --- | --- | --- |
| `state_changed` | 新狀態名稱 | 顯示除錯用的狀態文字即可 |
| `hands_changed` | 無，畫面再向 Match 要快照 | 重排四家手牌與副露 |
| `discard_changed` | 無 | 重畫棄牌池與 buffer |
| `offers_changed` | seat、動作字串陣列 | 人類才顯示按鈕 |
| `chow_options_changed` | seat、選項（每項兩張牌） | 人類點其中一項 |
| `round_ended` | 胡牌摘要或流局 | 短暫停，再讓 Match 開下一局 |
| `match_ended` | 四家分數 | 結束畫面 |

人類輸入用信號回 `Match`：`tile_clicked(tile_id)`、`action_clicked(name)`、`chow_clicked(option_index)`。bot 不走這些信號，`Match` 在狀態裡直接叫政策。

牌的畫面 id 用實例 id，不要只用 classId。同一種有四張，點擊必須對到那一張。

## 腳本職責

### `tile_catalog.gd`

常數陣列，長度 35，index 0 空著。每一項有 `class_id`、`code`（`1m`）、`suit`、`number`、`texture_path`。提供 `suit_of(class_id)` 與 `number_of(class_id)`。這是純資料，沒有節點。

### `tile.gd`

`class_name Tile`。欄位只有 `class_id` 與一個給 log 用的 `uid`。不繼承 `Node`。畫面要另做 `TileView`，裡頭引用這個資源或物件。

### `player.gd`

`class_name Player`。欄位見 [02-turn-flow.md](02-turn-flow.md)。方法：

- `draw_tiles(tiles, wall_empty_after)`
- `check_on_draw_action() -> Array`
- `check_possible_calls(tile, chow_allowed) -> Array`
- `get_chow_options(tile) -> Array`，每項是兩張 `Tile`
- `discard_at(index) -> Tile`
- `pong(tile)`、`kong(tile)`、`chow(tile, pair)`、`hidden_kong()`、`additional_kong()`
- `win(tile_or_null) -> Array`，回傳 `[[name, value], ...]`
- `clear_round()` 清手牌與旗標，不清分數
- `snapshot_class_ids() -> Dictionary` 給 log

叫牌判定在 `calls.gd`，胡牌與番在另外兩個檔。`Player` 只負責持有牌與呼叫它們，避免和 Python 一樣把同一段拆牌複製兩份。

### `calls.gd`

`check_tuple_type`、`chow_options`、`can_pong`、`can_exposed_kong`、`can_hidden_kong`、`can_added_kong`。吃的選項用 [01-rules.md](01-rules.md) 的規則，不要只檢查排序後相鄰的兩種、卻漏掉「手牌同時有中間那張」的吃法。Python 的 `check_possible_calls` 有這個漏洞，`get_chow_options` 沒有。兩邊都用後者的結果來決定「能不能吃」。

### `win_checker.gd`

`is_winning(hand, melds) -> bool`，演算法照 [03-winning-and-scoring.md](03-winning-and-scoring.md) 的 `count_tuples` 與十三么。用牌的實例身份來移除，不要用 classId 一次扣掉所有相同的牌。

### `faan_calculator.gd`

`class_name FaanCalculator`。`evaluate(hand, melds, context) -> Array`。`context` 含 `wind`、`seat`、四個旗標。互斥放在這個函式的最後，呼叫端只加總。`wind` 每局寫入，不要固定 0。

### `score_table.gd`

`score_for(faan: int, self_drawn: bool) -> float`。把 [03-winning-and-scoring.md](03-winning-and-scoring.md) 的表寫成常數。自摸分帳用這個總分除以 3。

### `match.gd`

狀態機，一個 `step()` 推進一個狀態。人類在等點擊時 `step()` 直接返回。收到輸入信號才再 `step()`。

bot 對局若要快轉，用一個「每幀最多推進 N 步」的迴圈，不要把 16 局塞在同一個函式呼叫裡。這樣畫面看得到牌，log 也不會因為中途 return 少掉後面三家的回答。

`Match` 不 `preload` 畫面。測試腳本 `new()` 一個 `Match`，灌入手牌，就能測胡牌分。

### `heuristic_policy.gd` 與 `feature_encoder.gd`

逐項對照 [04-players-ai-logs.md](04-players-ai-logs.md)。encoder 做完後用一個固定局面斷言：

- 東圈、東位：`[0] == 0`，`[1] == 0`
- 手牌兩張一萬：`features[2] == 0.5`
- 碰了白板：`features[36 + 31] == 1`
- 吃了 123 萬：`features[104] == 0.25`
- 棄牌池一張中：`features[426 + 33] == 0.25`

### `model_policy.gd`

介面和 heuristic 相同：`choose_discard(player) -> int`、`allow_pong(tile) -> bool`、`allow_kong(tile) -> bool`、`allow_chow(tile) -> bool`。ONNX 模型沒載入就委派給 heuristic。載入路徑放在 `match_config.json`，不要寫進程式。

### `match_logger.gd`

`record_action(dict)` 與 `record_win(dict)`。結束時用 `FileAccess` 寫 JSON。時間戳用秒。欄位名稱與 [04-players-ai-logs.md](04-players-ai-logs.md) 的 JSON 一致，包含底線，這樣舊的訓練程式還讀得懂。

### `table_view.gd`

只讀 `Match` 的公開快照：

```gdscript
{
  "wind": int,
  "round": int,
  "current": int,
  "seats": [
    {
      "id": String,
      "kind": String,
      "seat": int,
      "score": float,
      "hand": Array,      # 人類或全開模式才給；否則空陣列
      "melds": Array,
      "reveal_hand": bool
    }
  ],
  "discard_pool": Array,
  "discard_buffer": Variant
}
```

有任何人類時，`reveal_hand` 只對人類為 true。全 bot 時四家都 true。

座位列的 y 可以用舊座標當第一版：座位 i 在畫面下方往上排。牌圖尺寸依素材，x 從 50 起。副露從第 14 張的位置開始。棄牌池最後 80 張、每行 20 張。

按鈕放在該家手牌右側。吃的選項用兩張牌圖橫排，不要只寫文字。

## 設定

`data/match_config.json`：

```json
{
  "heuristic_bot_count": 2,
  "model_bot_count": 0,
  "human_count": 2,
  "game_log_location": "user://logs",
  "min_faan": 3,
  "max_faan": 10,
  "reveal_bot_hands": false
}
```

三者人數之和不是 4 就拒絕開始。`reveal_bot_hands` 是 Godot 新增的觀察開關；訓練收資料時打開，給人玩時關掉。舊版沒有這個鍵，行為是「有人類就隱藏 bot 手牌」。

## 移植清單

依這個順序做，每一項都可以單獨驗證。

1. `tile_catalog` 與 136 張洗牌。洗 1000 次，每種 classId 都是 4 張。
2. `win_checker`。把 `TestFaanCal.py` 裡每一個 `is_valid_winning_hand` 的手牌做成測資，包含十三么、四副露單騎、有副露的順子與刻子。
3. `faan_calculator`。同一檔的番種正例與反例都搬過來。特別確認：混一色必須有字牌、清一色不能有字牌、小三元在大三元時為假、九子連環多出的那張可以是 1–9 任一張、互斥會拿掉自摸與對對胡。
4. `score_table`。3 番食出是 64，3 番自摸是 96，10 番食出是 1024，11 番仍是 1024。
5. `calls`。下家才能吃；字牌不能吃；手牌 3 張才能明槓；牆裡少於 2 張不能明槓；同一張打出牌的多種吃法都列出來。
6. `heuristic_policy`。主花色平手時選萬；已有順子就不碰別的花色；`pair_count` 夠高時不吃。
7. `feature_encoder`。用上一節的斷言。
8. `match` 狀態機。寫一個腳本對局：四個 heuristic，固定隨機種子，確認打完正好 16 局（4 圈 × 4 局），流局或胡牌都會進入下一局，分數有增減。
9. 人類輸入。一個人類加三個 heuristic，能打牌、碰、在多種吃法裡選、自摸、pass。
10. log。打完一場，JSON 能被現有的 Python `encoder()` 讀取。用一筆 `discard` 紀錄在 Python 裡編碼，和 Godot 的 426 維逐格比對。
11. 畫面。確認隱藏手牌、副露公開、棄牌池、圈風局數、分數。有人類時走一遍食出與自摸的計分顯示。

第 8 步不要用「看一張截圖」當成完成。至少自動打完一場，並用手點完一次吃與一次胡。

## 與 Python 對得上的隨機

洗牌與 heuristic 的隨機打牌都用 Godot 的 `RandomNumberGenerator`，種子放進設定。需要和某一次 Python 對局逐張相同時，不要期望 `random.shuffle` 和 Godot 產生一樣的序列。對得上的是規則與特徵，不是同一串牌。

## 最小可玩範圍

若時間只夠一版：

- 人類與 heuristic bot
- 完整胡牌、三番、分數、16 局
- 吃碰明槓暗槓加槓、流局
- action log 與 winning log
- 四方或直排的牌桌都可以

model bot、搶槓、天胡、地胡可以排在這版之後。它們的欄位與番種 key 先留在計番器裡，判定回 false，就不會影響已完成的對局。
