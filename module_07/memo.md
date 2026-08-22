# DataDeck — レビュー・ディフェンス用まとめ

Module 7 / Abstract Card Architecture の全体像、検証手順、説明すべき概念、想定質問。

---

## 1. 課題要件チェックリスト

### 全体の制約

| 項目 | 要件 | 状態 |
|---|---|---|
| Python バージョン | 3.10 以降 | ✅ `tuple[...]` / `list[str]` 記法を使用 |
| コーディング規約 | flake8 準拠 | ✅ 全17ファイル クリーン |
| 型アノテーション | 網羅的、mypy で確認 | ✅ `mypy --strict` 通過 |
| 外部ライブラリ | 禁止 | ✅ `abc` と組み込みのみ |
| `eval()` / `exec()` | 禁止 | ✅ 未使用 |
| 例外処理 | クラッシュしないこと | ✅ 各スクリプトの `main` で捕捉 |
| `__init__.py` | 各演習フォルダに必須 | ✅ ex0 / ex1 / ex2 すべてに存在 |
| テストコードの位置 | リポジトリのルート | ✅ 3スクリプトともルート |

### 演習ごとの提出物

| 演習 | 提出物 |
|---|---|
| ex0 | `battle.py` + パッケージ `ex0/` |
| ex1 | `capacitor.py` + パッケージ `ex1/` |
| ex2 | `tournament.py` + パッケージ `ex2/` |

### 明示された設計要件

- **ex0:** `ex0` パッケージは具象 Creature を直接公開してはならない。ファクトリーのみを公開する。
- **ex1:** 能力の抽象クラスは `Creature` 基底クラスを**継承しない**。
- **ex1:** `TransformCapability` は状態を永続化する属性を持ち、それが `attack` の実装に影響する。
- **ex1:** `ex1` も具象 Creature を公開してはならない。
- **ex2:** 無効な組み合わせで `act` が呼ばれたら、明確なメッセージを持つ**専用の例外**を送出する。
- **ex2:** `battle` は**単一の関数**で、対戦者リストを受け取り総当たりを行う。

---

## 2. ファイル構成

```
リポジトリのルート/
├── battle.py                 ← ex0 テスト: test_factory / test_battle / main
├── capacitor.py              ← ex1 テスト: test_healing / test_transforming / main
├── tournament.py             ← ex2 テスト: battle（総当たり）/ main
│
├── ex0/
│   ├── __init__.py           ← 公開: CreatureFactory, FlameFactory, AquaFactory
│   ├── creature.py           ← Creature（抽象）
│   ├── factory.py            ← CreatureFactory（抽象）
│   ├── flame.py              ← Flameling, Pyrodon, FlameFactory
│   └── aqua.py               ← Aquabub, Torragon, AquaFactory
│
├── ex1/
│   ├── __init__.py           ← 公開: HealCapability, TransformCapability,
│   │                             HealingCreatureFactory, TransformCreatureFactory
│   ├── capability.py         ← HealCapability, TransformCapability（Creature 非継承）
│   ├── heal.py               ← HealingCreature, Sproutling, Bloomelle,
│   │                             HealingCreatureFactory
│   └── transform.py          ← TransformingCreature, Shiftling, Morphagon,
│                                TransformCreatureFactory
│
└── ex2/
    ├── __init__.py           ← 公開: BattleStrategy, InvalidCombinationError,
    │                             NormalStrategy, AggressiveStrategy, DefensiveStrategy
    ├── strategy.py           ← BattleStrategy（抽象）, InvalidCombinationError
    ├── normal.py             ← NormalStrategy
    ├── aggressive.py         ← AggressiveStrategy
    └── defensive.py          ← DefensiveStrategy
```

**構成の3原則**

1. 抽象と具象を別ファイルに分ける（`creature.py` / `factory.py` / `capability.py` / `strategy.py` が抽象側）
2. 具象はファミリー単位でまとめ、そのファミリーのファクトリーも同じファイルに置く
3. `__init__.py` は公開するものだけを import する

---

## 3. クラス階層

```
Creature (ABC)                        CreatureFactory (ABC)
├── Flameling                         ├── FlameFactory
├── Pyrodon                           ├── AquaFactory
├── Aquabub                           ├── HealingCreatureFactory
├── Torragon                          └── TransformCreatureFactory
├── HealingCreature (ABC) ────────┐
│   ├── Sproutling                │  多重継承
│   └── Bloomelle                 │
└── TransformingCreature (ABC) ───┤
    ├── Shiftling                 │
    └── Morphagon                 │
                                  │
HealCapability (ABC) ─────────────┤   ← Creature を継承しない
TransformCapability (ABC) ────────┘   ← Creature を継承しない

BattleStrategy (ABC)
├── NormalStrategy       （全 Creature に有効）
├── AggressiveStrategy   （TransformCapability を要求）
└── DefensiveStrategy    （HealCapability を要求）

InvalidCombinationError (Exception)
```

---

## 4. テスト方法

すべて**リポジトリのルート**で実行する（`ex0/` などの中に入らない。パッケージとして import させるため）。

### 実行

```bash
python3 battle.py
python3 capacitor.py
python3 tournament.py
```

出力は subject の例と**完全一致**することを確認済み。

### 規約・型チェック

```bash
pip3 install flake8 mypy          # 初回のみ
flake8 ex0/ ex1/ ex2/ battle.py capacitor.py tournament.py
mypy   ex0/ ex1/ ex2/ battle.py capacitor.py tournament.py --strict
```

### 個別の検証コマンド

**具象クラスが漏れていないか（ex0 / ex1 の必須要件）**

```bash
python3 -c "import ex0; print(ex0.__all__); print(hasattr(ex0, 'Flameling'))"
# → ['CreatureFactory', 'FlameFactory', 'AquaFactory'] / False

python3 -c "import ex1; print(hasattr(ex1, 'Sproutling'))"
# → False
```

**抽象クラスがインスタンス化できないか**

```bash
python3 -c "from ex0.creature import Creature; Creature('x','y')"
# → TypeError: Can't instantiate abstract class Creature ...
```

**変身の状態がインスタンスごとに独立しているか**

```bash
python3 -c "
from ex1 import TransformCreatureFactory
f = TransformCreatureFactory()
a, b = f.create_base(), f.create_base()
a.transform()
print(a.transformed, b.transformed)   # True False
"
```

**ストラテジー × クリーチャーの全組み合わせ**

```bash
python3 -c "
from ex0 import FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import NormalStrategy, AggressiveStrategy, DefensiveStrategy
from ex2 import InvalidCombinationError
cs = [f().create_base() for f in
      (FlameFactory, HealingCreatureFactory, TransformCreatureFactory)]
for s in (NormalStrategy(), AggressiveStrategy(), DefensiveStrategy()):
    for c in cs:
        try:
            s.act(c); r = 'ok'
        except InvalidCombinationError:
            r = 'raise'
        print(f'{s.label:11} {c.name:11} is_valid={s.is_valid(c)} {r}')
"
```

期待される結果:

| | Flameling | Sproutling | Shiftling |
|---|---|---|---|
| normal | ✅ | ✅ | ✅ |
| aggressive | ❌ 例外 | ❌ 例外 | ✅ |
| defensive | ❌ 例外 | ✅ | ❌ 例外 |

`is_valid` が `False` を返す組み合わせと、`act` が例外を投げる組み合わせが**完全に一致**していることが要点。

### 提出前の最終確認

```bash
git status          # __pycache__ / .mypy_cache が混ざっていないか
ls ex0/__init__.py ex1/__init__.py ex2/__init__.py   # 必須ファイルの存在
```

---

## 5. 理解すべき用語

### 抽象クラス（Abstract Base Class / ABC）

インスタンス化できないクラス。`abc.ABC` を継承し、`@abstractmethod` を付けたメソッドを持つ。サブクラスがそのメソッドを実装するまでインスタンス化しようとすると `TypeError` になる。

**このプロジェクトでの例:** `Creature`, `CreatureFactory`, `HealCapability`, `TransformCapability`, `BattleStrategy`

### 抽象メソッド vs 具象メソッド

抽象クラスは両方を持てる。`Creature` では `attack` が抽象（種類ごとに違う）、`describe` が具象（全種共通なので一度書けばよい）。**共通部分を親に、差分だけを子に**書くのが原則。

### ポリモーフィズム（多態性）

同じ呼び出しが、実際のオブジェクトの型に応じて違う振る舞いをすること。`creature.attack()` という1行が、Flameling なら Ember、Aquabub なら Water Gun を返す。

### 抽象ファクトリー（Abstract Factory）パターン

**関連するオブジェクト群を、具象クラスを指定せずに生成するためのインターフェース。**

- `CreatureFactory` が「base と evolved を作れる」という契約だけを定義
- `FlameFactory` / `AquaFactory` が実際に何を作るかを決める
- 呼び出し側（`test_factory`）は `CreatureFactory` としか話さないので、ファミリーが増えても変更不要

**「ファクトリーメソッド」との違い:** ファクトリーメソッドは1個のオブジェクトを作る。抽象ファクトリーは**関連する複数のオブジェクト（ここでは base と evolved のペア）**を、一貫したファミリーとして作る。

### ストラテジー（Strategy）パターン

**アルゴリズムを個別のクラスに切り出し、実行時に差し替え可能にする。**

- `BattleStrategy` が「行動できる」という契約を定義
- 3つの具象ストラテジーが、それぞれ違う行動手順を持つ
- `battle` 関数は `strategy.act(creature)` と呼ぶだけ。手順を知らない

**これがなければ:** `battle` の中に `if isinstance(creature, HealCapability): ... elif isinstance(creature, TransformCapability): ...` が並ぶ。能力が増えるたびに `battle` を書き換えることになる。

### 能力（Capability）とミックスイン

`HealCapability` / `TransformCapability` は `Creature` を継承しない**独立した抽象クラス**。「何であるか（is-a）」ではなく「何ができるか（can-do）」を表す。

Creature 以外のエンティティ（アイテム、トレーナー、罠カードなど）にも同じ能力を付けられる、という拡張性が狙い。

### 多重継承と MRO（Method Resolution Order）

Python はクラスの継承順序から線形の探索順（MRO）を計算する。`Shiftling.__mro__` で確認できる。

```
Shiftling → TransformingCreature → Creature → TransformCapability → ABC → object
```

**注意点:** `Creature.__init__` は `super().__init__()` を呼ばないため、`TransformCapability.__init__` は自動では実行されない。だから `TransformingCreature` の中で両方を明示的に呼んでいる。

### 共変な戻り値（Covariant return type）

オーバーライドしたメソッドは、親より**狭い**型を返してよい。

```python
class CreatureFactory:
    def create_base(self) -> Creature: ...

class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> HealingCreature: ...   # OK（狭める方向）
```

親の契約（Creature を返す）を破っていないので安全。逆に**広げる**（`object` を返す）のは型エラーになる。

### カプセル化 / 情報隠蔽

`ex0/__init__.py` でファクトリーだけを import することで、`ex0.Flameling` という経路を塞いでいる。利用者は「何が作られるか」を知らずに済み、内部の具象クラス名を自由に変更できる。

### 開放閉鎖原則（Open/Closed Principle）

**拡張に対して開き、修正に対して閉じている。** 新しいファミリーを追加するとき、新規ファイルを1つ足すだけで既存ファイルは一切変更しない——このプロジェクト全体がその実演になっている。

---

## 6. 想定質問と答え方

### Q. なぜ `create_base()` の戻り値の型が `Flameling` ではなく `Creature` なのか

具象型を返すと宣言してしまうと、呼び出し側が `Flameling` に依存してしまい、ファクトリーで隠した意味がなくなる。`Creature` を返すと宣言することで、`test_factory` は「何か Creature が返ってくる」としか知らない状態を保てる。これが抽象ファクトリーの目的そのもの。

### Q. なぜ `describe` は抽象メソッドにしなかったのか

全クリーチャーで文言が同じだから。抽象にすると全サブクラスで同じコードを繰り返すことになる。差分がある `attack` だけを抽象にしている。

### Q. `type` という属性名を使わなかった理由は

`type` は Python の組み込み関数で、シャドーイングすると混乱の元になる（flake8 でも指摘される）。`creature_type` にしている。

### Q. なぜ能力クラスを `Creature` から継承させないのか

subject の明示要件であると同時に、設計上も正しい。能力は「できること」であって「何であるか」ではない。継承させると、将来アイテムやトレーナーに回復能力を付けたくなったとき、それらを Creature にしなければならなくなる。

### Q. `TransformingCreature` という中間クラスを挟んだ理由は

多重継承の初期化問題を1箇所に閉じ込めるため。`Creature.__init__` は `super().__init__()` を呼ばないので、`Shiftling` から素朴に `super().__init__(...)` としても `TransformCapability.__init__` に到達せず、`_transformed` が未定義になって `AttributeError` が出る。中間クラスで両方の `__init__` を明示的に呼ぶことで、`Shiftling` と `Morphagon` は普通に `super().__init__()` を書くだけで済む。

**代替案:** `Creature.__init__` の末尾に `super().__init__()` を足して協調的多重継承にする方法もある。より Python 的だが、ex0 に手を入れる必要があり、MRO を理解していないと壊れやすい。明示的に呼ぶほうが読み手に意図が伝わると判断した。

### Q. `transformed` の状態はどこに持っているのか。インスタンスごとに独立しているか

`TransformCapability.__init__` で `self._transformed = False` としているのでインスタンス属性。クラス属性ではないので、同じファミリーの2体を作っても状態は混ざらない（検証コマンドあり）。

### Q. `attack` はどうやって変身状態を知るのか

`attack` の中で `self.transformed` を見て返す文字列を分岐している。呼び出し側は同じ `attack()` を呼んでいるだけで、`transform()` の前後で出力が変わる。状態を持つオブジェクトとポリモーフィズムの組み合わせ。

### Q. `is_valid` と `act` で `isinstance` を二重に書いているのは冗長では

役割が違う。`is_valid` は「事前に聞くための公開述語」で、呼び出し側が実行前に確認できる。`act` の中のチェックは自己防衛であり、同時に**型チェッカに型を絞り込ませる唯一の手段**でもある。`is_valid` を通しただけでは mypy は `creature` が `TransformCapability` だと判断できず、`creature.transform()` が型エラーになる。

### Q. なぜ `act` は文字列のリストを返すのか。直接 print しないのは

表示とロジックの分離。ストラテジーは「何が起きたか」を返すだけで、それをどう出すか（標準出力、ログ、GUI）は `battle` 側の責任にしてある。テストもしやすい。

### Q. `battle` 関数に `isinstance` が1つもないのはなぜ成立するのか

各対戦者が自分のストラテジーを持って来ているから。`battle` は `strategy.act(creature)` と呼ぶだけで、回復ファミリーなら「攻撃→回復」、変身ファミリーなら「変身→攻撃→戻る」が実行される。分岐はストラテジーのクラス階層が肩代わりしている。**これがストラテジーパターンの主張そのもの。**

### Q. 新しい能力（例: 毒）を追加するとしたら、どこを変更するか

1. `ex1/capability.py` に `PoisonCapability` を追加
2. `ex1/poison.py` に `PoisoningCreature` + 具象2体 + ファクトリーを追加
3. `ex1/__init__.py` に export を追加
4. `ex2/poisonous.py` に `PoisonStrategy` を追加、`ex2/__init__.py` に export

**既存のファイルはどれも変更しない。** `battle` も `Creature` も `CreatureFactory` も無傷。これが開放閉鎖原則。

### Q. 例外はなぜ専用クラスにしたのか

`InvalidCombinationError` を定義することで、呼び出し側が「無効な組み合わせ」だけを狙って捕捉できる。`Exception` をそのまま投げると、無関係なバグまで一緒に握りつぶしてしまう。`tournament.py` の `except InvalidCombinationError` は、まさにこの1種類だけを捕まえている。

### Q. トーナメントの総当たりはどう実装しているか

`for index, first in enumerate(fighters)` の内側で `fighters[index + 1:]` を回す。各ペアがちょうど1回ずつ対戦し、自分自身とは戦わない。n体なら n×(n-1)/2 試合（3体なら3試合）。

### Q. なぜクリーチャーはトーナメント開始時に1回だけ生成しているのか

「対戦者」は試合ごとに使い捨てではなく、トーナメントを通じて同一の個体だから。変身ストラテジーは最後に `revert()` するので、次の試合には通常状態で臨める（状態が漏れない）ことも確認済み。

---

## 7. 詰まりやすいポイント

| 症状 | 原因 |
|---|---|
| `ModuleNotFoundError: No module named 'ex0'` | ルート以外から実行している、または `__init__.py` がない |
| `AttributeError: '_transformed'` | 多重継承で `TransformCapability.__init__` が呼ばれていない |
| `TypeError: Can't instantiate abstract class` | 抽象メソッドの実装漏れ（正しく出る場合もある。抽象クラスを直接インスタンス化しようとしたときは正常な動作） |
| mypy: `"Creature" has no attribute "heal"` | 戻り値の型を狭めていない、または `isinstance` で絞り込んでいない |
| flake8: E501 | 79文字超え。`print()` の引数や `battle([...])` の呼び出しで起きやすい |
| 出力が例と微妙に違う | 行頭の半角スペース（` vs.` ` fight!` ` base:`）と空行の位置。`diff` で確認するのが確実 |

---

## 8. 一言でまとめると

- **ex0（抽象ファクトリー）** — 何を作るかを、使う側から隠す
- **ex1（能力）** — 「である」と「できる」を分けて、組み合わせで表現する
- **ex2（ストラテジー）** — どう振る舞うかを、使う側から隠す

3つとも「**呼び出し側が具体を知らなくて済むようにする**」という同じ目的に向かっていて、隠す対象が「生成」「性質」「アルゴリズム」と違うだけ。ここを説明できれば、このプロジェクトの意図は伝わる。

# DataDeck — 演習別の要件比較とコードリーディング

ex0 / ex1 / ex2 が「何を要求していて、どこが違うのか」と、実際のコードが**どう動くのか**を実行順に追った解説。

---

## 第1部: 3演習の要件比較

### 1.1 一覧表

| 観点 | ex0 | ex1 | ex2 |
|---|---|---|---|
| **主題のパターン** | 抽象ファクトリー | 能力（ミックスイン） | ストラテジー |
| **隠すもの** | 何を**生成**するか | 何が**できる**か | どう**振る舞う**か |
| **新しく作る抽象** | `Creature`, `CreatureFactory` | `HealCapability`, `TransformCapability` | `BattleStrategy` |
| **新しく作る具象** | 4体 + 2ファクトリー | 4体 + 2ファクトリー | 3ストラテジー |
| **状態を持つか** | ❌ 持たない | ✅ `_transformed` | ❌ 持たない |
| **例外を扱うか** | ❌ | ❌ | ✅ 専用例外を定義 |
| **多重継承** | ❌ | ✅ Creature + Capability | ❌ |
| **前の演習に依存** | — | ex0 に依存 | ex0 + ex1 に依存 |
| **具象の公開禁止** | ✅ 必須 | ✅ 必須 | （規定なし） |
| **テストスクリプト** | `battle.py` | `capacitor.py` | `tournament.py` |

### 1.2 段階的に何が増えていくか

```
ex0  「Creature を作る」
      ↓ 生成の責任をファクトリーに移す
      ↓ 呼び出し側は具象クラス名を知らない

ex1  「Creature に能力を足す」
      ↓ 能力は Creature とは別系統の抽象として定義
      ↓ 状態（変身中かどうか）が attack の結果を変える
      ↓ 結果、ファミリーごとに「行動の手順」が異なってしまう

ex2  「異なる手順を、分岐なしで統一的に扱う」
      ↓ 手順そのものをクラスにする
      ↓ 呼び出し側は act() を呼ぶだけ
```

**ex1 が ex2 の問題を作り、ex2 がそれを解く**という関係になっている。ex1 の時点では `capacitor.py` が「回復用のテスト関数」と「変身用のテスト関数」を別々に持っていた（＝呼び出し側が手順を知っていた）。ex2 ではその区別が `battle` 関数から消える。

### 1.3 要件の細かい違い

#### 公開制限

| | 公開するもの | 隠すもの |
|---|---|---|
| ex0 | `CreatureFactory`, `FlameFactory`, `AquaFactory` | Flameling, Pyrodon, Aquabub, Torragon |
| ex1 | 能力ABC2つ + ファクトリー2つ | Sproutling, Bloomelle, Shiftling, Morphagon |
| ex2 | `BattleStrategy`, 例外, ストラテジー3つ | （隠すべき具象がない） |

ex2 だけ制限がないのは、**ストラテジーは呼び出し側が明示的に選ぶもの**だから。ファクトリーと違い「隠して差し替える」対象ではなく、`tournament.py` が `AggressiveStrategy()` と名指しでインスタンス化する。

#### 継承関係の制約

- **ex0:** 素直な単一継承。`Flameling(Creature)`。
- **ex1:** 「能力ABC は `Creature` を継承してはならない」という**禁止の要件**。結果として具象クラスが多重継承になる。
- **ex2:** `BattleStrategy` は Creature 階層と完全に無関係。`Creature` を**引数として受け取る**だけ（継承ではなく合成）。

#### テストシナリオの複雑さ

| | シナリオ |
|---|---|
| ex0 | ファクトリーを2つ試す → base 同士を戦わせる |
| ex1 | 回復系を2体試す → 変身系を2体試す（手順が違う） |
| ex2 | 3つのトーナメント（正常 / エラー / 3者総当たり） |

ex2 だけ**エラーケースを明示的にテストする**よう指定されている。これは「無効な組み合わせで専用例外を投げる」という要件とセット。

---

## 第2部: ex0 のコードリーディング

### 2.1 `ex0/creature.py` — 全ての土台

```python
class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self._name = name
        self._creature_type = creature_type

    @property
    def name(self) -> str:
        return self._name

    def describe(self) -> str:
        return f"{self._name} is a {self._creature_type} type Creature"

    @abstractmethod
    def attack(self) -> str:
        """Return the message describing this creature's attack."""
```

**読み方のポイント**

- `ABC` を継承しているので `Creature(...)` は直接インスタンス化できない。試すと `TypeError`。
- `describe` は**具象**。全クリーチャーで文言が同じなので、ここで一度書けば全サブクラスが継承する。
- `attack` は**抽象**。本体がなく docstring だけ。サブクラスが必ず実装する。
- `_name` はアンダースコア付き（内部用）で、読み取りは `@property` の `name` 経由。外から書き換える手段を用意していない。

**なぜ `attack` だけ抽象なのか:** 差分があるものだけを抽象にする、という原則。`describe` まで抽象にすると全サブクラスに同じコードを4回書くことになる。

### 2.2 `ex0/factory.py` — 生成の契約

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        """Return a new base-stage creature of this family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Return a new evolved-stage creature of this family."""
```

**この10行が抽象ファクトリーの本体。** 中身は空で、契約だけを宣言している。

注目すべきは**戻り値の型が `Creature`** であること。`Flameling` ではない。この1点が「呼び出し側に具象を知らせない」という要件を型レベルで保証している。

### 2.3 `ex0/flame.py` — 具象とファクトリーの同居

```python
class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()
```

**名前とタイプは `__init__` の中に埋め込む。** `Flameling()` は引数を取らない——「Flameling である」という事実に名前とタイプが含まれているから、外から渡させる理由がない。

**ファクトリーを同じファイルに置いた理由:** `FlameFactory` の唯一の仕事は「Fire ファミリーの具象クラスを知っていること」。同居させると、`Flameling` を import する行が `ex0` の外に一切現れなくなる。カプセル化がファイル構成で強制される。

### 2.4 `ex0/__init__.py` — 公開の絞り込み

```python
from ex0.aqua import AquaFactory
from ex0.factory import CreatureFactory
from ex0.flame import FlameFactory

__all__ = ["CreatureFactory", "FlameFactory", "AquaFactory"]
```

`ex0.Flameling` は **`AttributeError`** になる。`__init__.py` が import していないから。

> `__all__` は `from ex0 import *` の対象を決めるだけで、アクセス自体を禁止する機能ではない。今回は import していないクラスがそもそも属性として存在しないので、実質的な隠蔽が成立している。

### 2.5 `battle.py` の実行を追う

```python
def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())
    print()
```

`python3 battle.py` を実行したときの流れ:

```
main()
 └─ flame = FlameFactory()          ← 具象ファクトリーを1つ作る
 └─ test_factory(flame)
     │  引数の型は CreatureFactory。この関数は Flameling を知らない
     ├─ print("Testing factory")
     ├─ factory.create_base()       → FlameFactory.create_base() → Flameling()
     │   └─ Flameling.__init__ → super().__init__("Flameling", "Fire")
     │       └─ Creature.__init__ が _name / _creature_type を設定
     ├─ creature.describe()         → Creature.describe（継承した具象メソッド）
     │                                 "Flameling is a Fire type Creature"
     ├─ creature.attack()           → Flameling.attack（オーバーライド）
     │                                 "Flameling uses Ember!"
     ├─ factory.create_evolved()    → Pyrodon()
     └─ 同様に describe / attack
```

**ここが ex0 の核心:** `test_factory` の中には `Flameling` も `Pyrodon` も一文字も出てこない。にもかかわらず正しく動く。ファミリーが100個に増えても、この関数は1行も変わらない。

`describe()` は `Creature` のコードが、`attack()` は `Flameling` のコードが実行される——同じ変数 `creature` に対する2つの呼び出しが、片方は親、片方は子で解決される。これがポリモーフィズム。

---

## 第3部: ex1 のコードリーディング

### 3.1 `ex1/capability.py` — Creature を知らない能力

```python
class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str: ...


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._transformed = False

    @property
    def transformed(self) -> bool:
        return self._transformed

    @abstractmethod
    def transform(self) -> str: ...

    @abstractmethod
    def revert(self) -> str: ...
```

**このファイルには `from ex0 import ...` が1行もない。** これが「能力は Creature を継承しない」という要件の実体。

`TransformCapability` だけ `__init__` を持つ理由は、**状態を持つ能力だから**。`_transformed` は「今、変身しているか」を記録する。`HealCapability` は状態が不要なので `__init__` がない。

> `@property` で `transformed` を読み取り専用にしてあるが、`transform()` / `revert()` の中では `self._transformed = True/False` と内部変数を直接書き換えている。外からは読めるだけ、内部からは書ける、という設計。

### 3.2 `ex1/transform.py` — 多重継承の配線

```python
class TransformingCreature(Creature, TransformCapability, ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        Creature.__init__(self, name, creature_type)
        TransformCapability.__init__(self)
```

**この3行が ex1 で一番説明を求められる箇所。**

なぜ `super().__init__()` ではダメなのか。MRO を見る:

```
Shiftling → TransformingCreature → Creature → TransformCapability → ABC → object
```

`super().__init__(name, type)` を呼ぶと `Creature.__init__` に届く。しかし `Creature.__init__` は `super().__init__()` を呼んでいないので、**そこで連鎖が止まる**。`TransformCapability.__init__` は実行されず、`_transformed` が設定されない。

結果:

```python
c = Shiftling()
c.attack()      # AttributeError: 'Shiftling' object has no attribute '_transformed'
```

そこで両方の `__init__` を**明示的に**呼んでいる。この配線を中間クラスに閉じ込めたので、`Shiftling` 側は普通に書ける:

```python
class Shiftling(TransformingCreature):
    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")
```

### 3.3 状態が `attack` を変える仕組み

```python
class Shiftling(TransformingCreature):
    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self._transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self._transformed = False
        return f"{self.name} returns to normal."
```

実行を追う:

```python
c = Shiftling()
c.attack()      # _transformed = False → "Shiftling attacks normally."
c.transform()   # _transformed を True にして "shifts into a sharper form!"
c.attack()      # _transformed = True  → "Shiftling performs a boosted strike!"
c.revert()      # _transformed を False に戻して "returns to normal."
```

**同じ `c.attack()` という呼び出しが、2回目は違う文字列を返す。** 呼び出し側は何も変えていない。オブジェクトが状態を持ち、それが振る舞いを決めている。

`_transformed` はインスタンス属性なので、2体作れば状態は独立している:

```python
a, b = f.create_base(), f.create_base()
a.transform()
a.transformed   # True
b.transformed   # False
```

### 3.4 `ex1/heal.py` — 戻り値の型を狭める

```python
class HealingCreature(Creature, HealCapability, ABC):
    """A creature that also owns the healing capability."""


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> HealingCreature:
        return Sproutling()
```

`HealingCreature` は**中身が空のクラス**。存在意義は「Creature でもあり HealCapability でもある型」に名前を付けること。

なぜ必要か。もし親と同じ `-> Creature` と書くと:

```python
creature = factory.create_base()   # 型は Creature
creature.heal()                    # mypy: "Creature" has no attribute "heal"
```

`HealingCreature` を返すと宣言すれば、`describe()` も `attack()` も `heal()` も型エラーなく呼べる。親の `-> Creature` より**狭い**型を返すのは安全（共変）なので、オーバーライドとして正しい。

> `HealCapability` は `__init__` を持たないので、`HealingCreature` に配線コードは不要。`Sproutling.__init__` の `super().__init__("Sproutling", "Grass")` は `Creature.__init__` に届いてそれで完結する。`TransformingCreature` と非対称なのはこの理由。

### 3.5 `capacitor.py` — 「呼び出し側が手順を知っている」状態

```python
def test_healing(creature: HealingCreature) -> None:
    print(creature.describe())
    print(creature.attack())
    print(creature.heal())


def test_transforming(creature: TransformingCreature) -> None:
    print(creature.describe())
    print(creature.attack())
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())
```

**ここに ex2 への伏線がある。** 関数が2つに分かれているのは、手順が違うから。回復系は3行、変身系は5行。

もしこのまま「いろんなファミリーを混ぜて戦わせたい」となったら、呼び出し側にこう書くことになる:

```python
# ex2 で避けたい未来のコード
if isinstance(creature, HealCapability):
    print(creature.attack()); print(creature.heal())
elif isinstance(creature, TransformCapability):
    print(creature.transform()); print(creature.attack()); print(creature.revert())
else:
    print(creature.attack())
```

能力が増えるたびにこの `if` が伸びる。**これを消すのが ex2。**

---

## 第4部: ex2 のコードリーディング

### 4.1 `ex2/strategy.py` — 行動の契約とエラー

```python
class InvalidCombinationError(Exception):
    """Raised when a strategy is applied to an unsuitable creature."""


class BattleStrategy(ABC):
    def __init__(self, label: str) -> None:
        self._label = label

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...

    @abstractmethod
    def act(self, creature: Creature) -> list[str]: ...

    def _invalid(self, creature: Creature) -> InvalidCombinationError:
        return InvalidCombinationError(
            f"Invalid Creature '{creature.name}' "
            f"for this {self._label} strategy"
        )
```

**構造上の注意:** `BattleStrategy` は `Creature` を**継承していない**。`Creature` を引数で受け取っているだけ。「戦略は生き物ではない」——継承（is-a）ではなく合成（has-a / uses-a）の関係。

`_label` は `"normal"` `"aggressive"` `"defensive"` という文字列で、エラーメッセージの組み立てにだけ使う。`_invalid` を親に置いたので、3つのストラテジーが同じ書式のエラーを作れる。

**`_invalid` が例外を `raise` せず `return` している点**に注目。呼び出し側は `raise self._invalid(creature)` と書く。こうすると「例外を投げる」という制御フローが呼び出し側のコードに見えるので、読み手が流れを追いやすい。

### 4.2 3つのストラテジー — 同じ形、違う中身

```python
class NormalStrategy(BattleStrategy):
    def __init__(self) -> None:
        super().__init__("normal")

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise self._invalid(creature)
        return [creature.attack()]
```

```python
class AggressiveStrategy(BattleStrategy):
    def __init__(self) -> None:
        super().__init__("aggressive")

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise self._invalid(creature)
        return [
            creature.transform(),
            creature.attack(),
            creature.revert(),
        ]
```

```python
class DefensiveStrategy(BattleStrategy):
    def __init__(self) -> None:
        super().__init__("defensive")

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, HealCapability):
            raise self._invalid(creature)
        return [creature.attack(), creature.heal()]
```

**`capacitor.py` にあった `if` が、ここに移動してきた**のが見て取れる。ただし移動先では:

- 分岐が**1つのクラスにつき1つ**に分解されている（`elif` の連鎖がない）
- 新しい能力を足すときは**新しいクラスを追加するだけ**で、既存のクラスを触らない

**`act` の中で `isinstance` を書き直している理由:** `is_valid(creature)` を通しただけでは、型チェッカは `creature` が `TransformCapability` だと判断できない。`isinstance` を直接書くことで mypy が型を絞り込み、`creature.transform()` が型エラーにならなくなる。`is_valid` は「事前に聞くための公開述語」、`act` の中のチェックは「自己防衛 + 型の絞り込み」と役割が違う。

**`act` が `list[str]` を返す理由:** 表示とロジックの分離。ストラテジーは「何が起きたか」を返すだけ。どう出力するかは呼び出し側の責任。

### 4.3 `tournament.py` の `battle` — 分岐がない総当たり

```python
Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    print()

    fighters = [(factory.create_base(), s) for factory, s in opponents]
    for index, (first, first_strategy) in enumerate(fighters):
        for second, second_strategy in fighters[index + 1:]:
            print("* Battle *")
            print(first.describe())
            print(" vs.")
            print(second.describe())
            print(" now fight!")
            try:
                for message in first_strategy.act(first):
                    print(message)
                for message in second_strategy.act(second):
                    print(message)
            except InvalidCombinationError as error:
                print(f"Battle error, aborting tournament: {error}")
                print()
                return
            print()
```

**この関数に `isinstance` が1つもない。** `heal` も `transform` も登場しない。`strategy.act(creature)` を呼ぶだけ。

#### 総当たりの仕組み

```python
for index, (first, ...) in enumerate(fighters):
    for second, ... in fighters[index + 1:]:
```

`fighters[index + 1:]` で「自分より後ろの対戦者」だけを見る。これで:

- 自分自身とは戦わない
- 同じペアが2回対戦しない
- n体なら n×(n-1)/2 試合（3体 → 3試合）

3体 `[A, B, C]` の場合:

| index | first | 対戦相手 |
|---|---|---|
| 0 | A | B, C |
| 1 | B | C |
| 2 | C | （なし） |

#### エラー時の中断

`try` が囲んでいるのは `act` の呼び出しだけ。`describe()` や `" now fight!"` の印字は `try` の外にあるので、**エラーが起きても対戦カードは表示される**。これが subject の例と一致する:

```
* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

`return` でトーナメント全体を打ち切る（"aborting tournament"）。`main` は次のトーナメントに進む。

### 4.4 実行トレース — Tournament 2 の1試合目

`python3 tournament.py` の Tournament 2、`Aquabub+Normal` vs `Sproutling+Defensive`:

```
battle([(AquaFactory(), normal),
        (HealingCreatureFactory(), defensive),
        (TransformCreatureFactory(), aggressive)])
 │
 ├─ print("*** Tournament ***")
 ├─ print("3 opponents involved")
 │
 ├─ fighters = [...]
 │   ├─ AquaFactory().create_base()            → Aquabub()
 │   ├─ HealingCreatureFactory().create_base() → Sproutling()
 │   └─ TransformCreatureFactory().create_base() → Shiftling()
 │
 └─ index=0: first=Aquabub, first_strategy=normal
     └─ second=Sproutling, second_strategy=defensive
         ├─ print("* Battle *")
         ├─ Aquabub.describe()    → "Aquabub is a Water type Creature"
         ├─ print(" vs.")
         ├─ Sproutling.describe() → "Sproutling is a Grass type Creature"
         ├─ print(" now fight!")
         │
         ├─ normal.act(Aquabub)
         │   ├─ isinstance(Aquabub, Creature) → True
         │   └─ return ["Aquabub uses Water Gun!"]
         │
         └─ defensive.act(Sproutling)
             ├─ isinstance(Sproutling, HealCapability) → True
             │   （Sproutling → HealingCreature → HealCapability なので成立）
             └─ return ["Sproutling uses Vine Whip!",
                        "Sproutling heals itself for a small amount"]
```

**注目:** `battle` は Aquabub に対して1行、Sproutling に対して2行が返ってくることを事前に知らない。返ってきたリストをそのまま印字しているだけ。手順の差はストラテジーの中で吸収されている。

### 4.5 エラーケースのトレース — Tournament 1

`Flameling+Aggressive` の組み合わせ:

```
aggressive.act(Flameling)
 ├─ isinstance(Flameling, TransformCapability) → False
 │   （Flameling → Creature のみ。TransformCapability を継承していない）
 └─ raise self._invalid(Flameling)
     └─ InvalidCombinationError(
            "Invalid Creature 'Flameling' for this aggressive strategy")
         │
         └─ battle の except が捕捉
             ├─ print("Battle error, aborting tournament: " + str(error))
             └─ return  ← トーナメント全体を打ち切り
```

`_label` が `"aggressive"` なので、メッセージの中に戦略名が入る。3つのストラテジーが同じ `_invalid` を使っているので、書式が自動的に揃う。

---

## 第5部: 3演習を貫くもの

### 5.1 同じ問いの3つの答え

すべての演習が「**呼び出し側が具体を知らなくて済むようにするには?**」という同じ問いに答えている。

| 演習 | 呼び出し側が知らなくて済むこと | 実現手段 |
|---|---|---|
| ex0 | どのクラスがインスタンス化されるか | ファクトリーが `Creature` 型で返す |
| ex1 | そのクリーチャーが変身中かどうか | オブジェクトが状態を持ち `attack` が分岐 |
| ex2 | どんな手順で行動するか | ストラテジーが `list[str]` で結果を返す |

### 5.2 新しいファミリー「毒」を追加するとしたら

| 演習 | 追加するもの | 変更するファイル |
|---|---|---|
| ex0 相当 | `poison.py`（具象2体 + `PoisonFactory`） | `ex0/__init__.py` に1行 |
| ex1 相当 | `PoisonCapability` + `PoisoningCreature` + 具象2体 + ファクトリー | `ex1/__init__.py` に export |
| ex2 相当 | `PoisonStrategy` | `ex2/__init__.py` に export |

**`battle`、`test_factory`、`Creature`、`CreatureFactory`、`BattleStrategy` は1行も変わらない。** 既存の抽象と、それに依存する汎用コードが無傷のまま拡張できる——これが開放閉鎖原則の実演。

### 5.3 逆に、パターンを使わなかったら

```python
# ex0 なし: 呼び出し側が具象を名指し
if family == "fire":
    c = Flameling()
elif family == "water":
    c = Aquabub()

# ex1 なし: 能力を Creature の属性フラグで表現
if creature.can_heal:
    ...

# ex2 なし: battle の中に手順の分岐
if isinstance(creature, HealCapability):
    ...
elif isinstance(creature, TransformCapability):
    ...
```

どれも動くが、**新しい種類を足すたびに既存のコードを書き換える**ことになる。書き換えるということは、既に動いていたコードを壊すリスクを毎回背負うということ。抽象化のコストは、この書き換えを避けるために払っている。