# 04 玩家、bot、特徵與 log

## 三種玩家

| kind | 現有類別 | 打牌 | 叫牌 | 摸牌後 |
| --- | --- | --- | --- | --- |
| `human` | `PlayerGUI` | 點手牌 | 點按鈕，多種吃法自己選 | 點按鈕 |
| `heuristic` | `BotPlayerGUI` + `Policy` | 下面的 heuristic | 下面的 heuristic | 見偏差說明；Godot 用建議規則 |
| `model` | `ModelPlayerGUI` + `ModelPolicy` | 有權重就用 discard MLP，否則退回 heuristic | 有權重就用對應 MLP，否則退回 heuristic | 同上 |

bot 在每次要決定前，把政策裡的局面更新成：

- 棄牌池（不含還在 buffer、尚未判定的那張，除非它已經被放進 pool）
- 自己的手牌
- 自己的副露
- 其他三家副露，順序固定是下家、對家、上家

`ModelPolicy.convert_to_dict` 也用這個順序。

## Heuristic

政策把牌記成四列計數：萬 9、筒 9、索 9、字 7。

主花色 `dominating_suit`：

1. 若已有副露，而且第一組副露的第一張是萬、筒或索，主花色就是那一張的花色。第一組是本局最早的副露，不是最後一組。
2. 否則看手牌的萬、筒、索張數，取最多的。平手時萬優先於筒，筒優先於索。字牌不能當主花色。

其他計數只看手牌，除非函式另外給了一份假設手牌：

| 名稱 | 定義 |
| --- | --- |
| `pair_count` | 某個 classId 張數 ≥ 2 的種類數。三張、四張也算一對 |
| `pong_kong_count` | 張數 ≥ 3 的種類數 |
| `consec_2_count` | 數牌裡，相鄰點數都至少一張的次數。只算萬筒索 |
| `alternating_consec_2_count` | 數牌裡，點數差 2 都至少一張的次數，例如 1 與 3、2 與 4 |

### 打牌 `decide_discard`

在「花色不是主花色」的手牌 index 裡隨機一張。若每張都是主花色，就在整手牌裡隨機。

### 碰 `decide_pong`

回傳 bool。

1. 若已有順子副露，而打出的牌是數牌、花色又和那組順子不同，不碰。
2. 若 `pair_count >= 5 - meld_count` 而且打出牌的花色就是主花色，碰。
3. 否則假設碰掉兩張（手牌若多於兩張，留一張），重算交替搭子。新的交替搭子比原來多，就不碰。否則碰。

### 槓 `decide_kong`

若已有順子副露，而這張是不同花色的數牌，不槓。否則槓。暗槓與加槓在 Godot 的摸牌決策裡用同一條。

### 吃 `decide_chow`

回傳 `(should, option)`。bot 外層只用 bool；真正拿走的兩張是 `get_chow_options()[0]`。

1. `pair_count >= 5 - meld_count` 時不吃，保留對對胡路線。
2. 字牌不吃。
3. 不是主花色不吃。
4. 已有數牌副露、而且花色不同，不吃。
5. 否則對每一種合法窗口算「吃完後的手牌」：
   - 打出點數 3–7：可試 n+1 n+2、n−2 n−1、n−1 n+1
   - 點數 2：可試 n+1 n+2、n−1 n+1
   - 點數 8：可試 n−2 n−1、n−1 n+1
   - 點數 1：只有 n+1 n+2
   - 點數 9：只有 n−2 n−1
   - 手牌沒有對應點數的那種窗口直接跳過
6. 在剩下的窗口裡，依 `(吃完後的 consec_2, 吃完後的 alternating)` 由大到小排，取第一個。
7. 若該窗口吃完後的 alternating **大於等於** 吃之前的 alternating，不吃。只有 alternating 嚴格變少才吃。

### 胡 `decide_win`

永遠 true。bot 的 `decide_call_action` 又比政策更早：offers 裡有 `win` 就直接胡，不再看碰槓吃。

沒有胡的時候，依序問吃、碰、槓的政策，不同意就從 offers 拿掉。offers 原本的順序是 `win`、`pong`、`kong`、`chow`、`pass`。最後取剩下的第一個。所以碰和槓都同意時會碰，不會槓。槓只在碰被否決、或根本沒有碰的選項時才會選到。

## Model

四個多層感知器，推論時 `eval`，dropout 不作用。門檻看的是最後一層的原始輸出，沒有 sigmoid。

| 模型 | 檔案 | 輸入 | 輸出 | 決定 |
| --- | --- | --- | --- | --- |
| discard | `models/discard_model.pth` | 426 | 34 個 logit，對應 classId 1–34 | 取 logit 最高的 5 個 classId，依手牌順序找第一張 classId 落在這 5 個裡的，打出它的 index。5 個都不在手牌就退回 heuristic |
| pong | `models/pong_model.pth` | 460 | 1 個 logit | `logit > 0.5` 才碰 |
| kong | `models/kong_model.pth` | 460 | 1 個 logit | `logit > 0.5` 才槓 |
| chow | `models/chow_model.pth` | 460 | 1 個 logit | `logit > 0.5` 才吃，吃哪兩張仍用選項列表第一組 |

結構都是 `Linear → ReLU → Dropout(0.2) → Linear → ReLU → Dropout(0.2) → Linear → ReLU → Linear`。隱藏層寬度 512、256、128。權重存在 checkpoint 的 `model_state_dict`。

呼叫模型之前仍先做規則過濾：

- 槓：和 heuristic 一樣，先拒絕「已有順子又去槓別的數牌花色」。
- 吃：字牌、非主花色、已有其他數牌花色的副露，直接不吃，不呼叫模型。
- 碰：已有順子又碰別的數牌花色，直接不碰。

權重不存在就整段退回 heuristic。Godot 不讀 `.pth`。要沿用訓練好的 bot，把四個網路匯出成 ONNX，用 `Godot-ONNX` 或在對局外用一個小推論程式。沒有這一步時，Godot 只要 heuristic 與人類就已經是完整遊戲。

Discard 的 426 維是 460 維特徵拿掉「動作牌 one-hot」那 34 維：`features[0:392] + features[426:460]`。碰、槓、吃用完整 460 維，而且 `action_tile` 是打出的那張。

## 460 維特徵

`encoder(state)` 回傳長度 460 的浮點陣列。欄位對應 `feature_list.md`。

| 切片 | 長度 | 內容 | 數值 |
| --- | --- | --- | --- |
| `[0]` | 1 | `current_wind / 3` | 0、1/3、2/3、1 |
| `[1]` | 1 | `round_position / 3` | 同上，這是行動者的門風 |
| `[2:36]` | 34 | 手牌各 classId 的張數 | 每張 `+1/4`，所以 0、0.25、0.5、0.75、1 |
| `[36:70]` | 34 | 自己的碰 | 該 classId 有一組就 +1 |
| `[70:104]` | 34 | 自己的槓 | 4 張的副露，該 classId +1 |
| `[104:125]` | 21 | 自己的吃 | 見下表，每組 `+1/4` |
| `[125:159]` | 34 | 對家的碰 | +1 |
| `[159:193]` | 34 | 對家的槓 | +1 |
| `[193:214]` | 21 | 對家的吃 | 應與自己的吃同一套 21 種編號 |
| `[214:248]` | 34 | 下家的碰 | +1 |
| `[248:282]` | 34 | 下家的槓 | +1 |
| `[282:303]` | 21 | 下家的吃 | 21 種編號 |
| `[303:337]` | 34 | 上家的碰 | +1 |
| `[337:371]` | 34 | 上家的槓 | +1 |
| `[371:392]` | 21 | 上家的吃 | 21 種編號 |
| `[392:426]` | 34 | 動作牌 | 該 classId 設成 1。沒有動作牌（自摸、暗槓、加槓、摸牌後的 pass）就全 0 |
| `[426:460]` | 34 | 棄牌池 | 每張 `+1/4`，不含這次還在 buffer 的牌 |

手牌、棄牌池、副露都用 classId，1 對到 index 0。

吃的 21 種，key 是順子裡最小的 classId：

| 順子 | key | index |
| --- | --- | --- |
| 123 萬到 789 萬 | 1–7 | 0–6 |
| 123 筒到 789 筒 | 10–16 | 7–13 |
| 123 索到 789 索 | 19–25 | 14–20 |

一組吃先排序，再用最小那張去查表。查不到就不要寫進這 21 維（字牌不該出現）。

Python 的對家吃牌寫錯了：它用 `最小 classId - 1` 直接加到 index 193，7 索的順子會寫出 21 維以外。自己、下家、上家用的是上面這張表。Godot 與往後的新訓練資料，四家都用這張表。舊 log 若要重放特徵，對家那 21 維才需要模仿舊 bug。

`state` 必備欄位：

```text
current_wind
round_position
hand                         # classId 陣列，含尚未打出的牌
called_tuples                # 行動者副露，每組是 classId 陣列
action                       # 字串，encoder 只檢查它存在，不寫進向量
action_tile                  # classId，或 null
discard_pool
opposite_player_called_tuples
next_player_called_tuples
previous_player_called_tuples
```

相對座位以行動者為準：next 是下家，opposite 是對家，previous 是上家。Python 在「食出」那一筆把這三家相對到打出者，而不是胡牌者。新 log 一律相對到 `player_id` 那位行動者。

## Action log

每一筆是動作發生前的快照。陣列存在 `{game_log_location}/game_log_{unix_seconds}.json`。

```json
{
  "player_id": "HeuristicBot1",
  "current_wind": 0,
  "round_position": 1,
  "hand": [1, 1, 2, 3, 5, 5, 5, 11, 12, 13, 19, 19, 28, 28],
  "called_tuples": [[6, 7, 8]],
  "action": "discard",
  "action_tile": 11,
  "discard_pool": [9, 34],
  "opposite_player_called_tuples": [],
  "next_player_called_tuples": [[29, 29, 29]],
  "previous_player_called_tuples": []
}
```

`action` 用這些字串：

| action | 何時寫 | `action_tile` | 快照裡的手牌 |
| --- | --- | --- | --- |
| `discard` | 打牌 | 打出的 classId | 還含這張牌 |
| `pass` | 人類放棄叫牌，或放棄摸牌後的動作 | 叫牌時是 buffer 的 classId；摸牌後的 pass 是 null | 真正的手牌 |
| `chow` | 吃成立 | 打出的 classId | 吃之前的手牌，不含打出的牌 |
| `pong` | 碰成立 | 打出的 classId | 碰之前 |
| `kong` | 明槓成立 | 打出的 classId | 槓之前 |
| `additional_kong` | 加槓成立 | null | 加槓之前，那張還在手牌 |
| `hidden_kong` | 暗槓成立 | null | 暗槓之前 |
| `win` | 食出成立 | 贏張 classId | 不含贏張 |
| `self_drawn` | 自摸成立 | null | 已含摸進來的贏張 |

bot 的 pass 在 Python 裡常常不寫 log。Godot 建議人類與 bot 的 pass 都寫，訓練時才知道負樣本。若要和舊檔的筆數一致，就只寫人類的 pass。

`called_tuples` 與三家副露都是「這個動作改牌之前」。打牌那一筆的 `discard_pool` 不含剛打出的牌。

## Winning log

有人胡才寫 `winning_log_{unix}.json`。同一秒的兩個檔用同一個時間戳。

```json
{
  "player_id": "HumanPlayer1",
  "current_wind": 0,
  "round_position": 0,
  "hand": [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 11, 11],
  "called_tuples": [[29, 29, 29]],
  "winning_faan": [["pure_suit", 7], ["no_call", 1]],
  "score": 1152,
  "win_from": null
}
```

- `winning_faan` 是互斥之後的 `[name, value]` 列表，順序沿番表定義順序。
- `score` 是胡牌者這手收到的總分，不是每家付的數。
- 食出時 `win_from` 是打出者的 `player_id`，`hand` 不含贏張。
- 自摸時 `win_from` 是 null，`hand` 含贏張。
- 流局不寫 winning log。

## 一筆特徵怎麼從 log 來

訓練 discard 模型時，取 `action == "discard"` 的紀錄，`action_tile` 先不要灌進 one-hot，編碼後丟掉 `[392:426]`，得到 426 維。標籤是打出的 classId（0-based index 是 `action_tile - 1`）。

訓練碰、槓、吃時，正樣本是該 action 的紀錄，`action_tile` 要編碼進去。負樣本是同一張牌有這個選項但選了 `pass` 的紀錄。門檻 0.5 是在 logit 上，不是機率。
