# Data Quest - Python コレクション習得（5ページ目以降の翻訳）

---

## 第III章　はじめに

デジタルの世界へ戻ってきたデータエンジニアの皆さん！

Pythonの基礎を学んできた皆さんはしっかりと準備ができています。デジタルガーデンを動かす基本構文をマスターし、現実世界のシステムをモデル化するクラス階層を構築し、例外処理で予期しない事態に優雅に対応する方法を学びました。次はデータエンジニアリングの核心に挑みます：**コレクションとデータ構造**です。ゲームの環境を通して探求していきましょう。

こんな場面を想像してみてください：1980年、パックマンのゲーム状態全体（すべてのドット、ゴーストの位置、スコア）はわずか16KBのRAMに収まっていました。開発者たちは効率の魔術師でなければなりませんでした！彼らはデータの整理がメモリ節約だけでなく、ゲームの魔法を解き放つことでもあると気づきました。現代に目を向けると、フォートナイトは1000万人以上の同時接続プレイヤーを処理し、それぞれが毎秒数千のデータポイントを生成しています。原則は同じ、スケールが違うだけです！

Pythonのコレクション型はさまざまなユースケース向けに設計されており、それぞれ固有の特徴があります：**リスト**（順序付き・インデックスあり・拡張可能）、**タプル**（順序付き・不変・ハッシュ可能）、**セット**（ユニークな要素の順序なしコレクション）、**辞書**（キーと値のペア）。

これらに加えて**ジェネレーター**と**内包表記**があり、強力な構文と動作を提供します。

このクエストでは、ゲーム分析プラットフォームを支えるコンポーネントを構築します。各演習で新しいデータ型が解放され、最終的にはデータエンジニアとしてPythonのコレクションを自在に使いこなせるようになります！

> 💡 このプロジェクトから、各演習で適切に紹介されたPythonのデータ構造と、それに関連するすべてのクラスメソッドを使用できるようになります。

---

## 第IV章　共通ルール

### IV.1　基本ルール

- プロジェクトは **Python 3.10以降** で記述すること
- **flake8** コーディング標準に準拠すること
- すべての関数・メソッドに型ヒントを付けること（`mypy` で確認）
- 関数はクラッシュしないよう例外を適切に処理すること
- コマンドライン引数へのアクセスには `sys` モジュールを `import` 機構で使用すること（importの詳細は今後のプロジェクトで扱います）
- ファイルI/O操作は禁止。データはすべてメモリ上またはコマンドライン引数で処理すること
- コレクションの使用パターンを明確に示すこと
- 各データ構造の基本操作と応用テクニックの両方を示すこと

> 💡 以下の標準型とそれに関連するすべてのメソッド・コンストラクタが使用可能です：`str`、`int`、`float`

### IV.2　追加ガイドライン

- 指定されたGitリポジトリに提出すること
- リポジトリ内のコンテンツのみが評価対象となります

---

## 第V章　演習0：コマンドクエスト

| | Exercise0 |
|---|---|
| ディレクトリ | ex0/ |
| 提出ファイル | ft_command_quest.py |
| 使用可能 | `import sys`、`sys.argv`、`len()`、`print()` |

**データ冒険者よ、ようこそ！** すべての壮大なクエストはツールを理解することから始まります。デジタルの世界では、プログラムは外部から命令を受け取る必要があります。最初のミッションは、プログラムがユーザーからメッセージを受け取る仕組みを探ることです！

いよいよ**リスト**の登場です。自分でリストを作る前に、すでに存在するリストを操作しましょう：`sys` モジュールから利用できるコマンドライン引数です。構造はCのものと似ており、文字列の配列です。リスト要素へのアクセスと操作を探求してください。

コマンドライン引数として受け取ったデータを表示するシンプルなスクリプトを作成してください。以下の例を参考にしてください。

```
$> python3 ft_command_quest.py
=== Command Quest ===
Program name: ft_command_quest.py
No arguments provided!
Total arguments: 1

$> python3 ft_command_quest.py hello world 42
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: hello
Argument 2: world
Argument 3: 42
Total arguments: 4

$> python3 ft_command_quest.py "Data Quest"
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 1
Argument 1: Data Quest
Total arguments: 2
```

> 💡 `sys.argv` リストにアクセスするには、スクリプトの先頭に `import sys` と書くだけです。

> ℹ️ 引数にプログラム名を再度表示しないようにする方法は複数あります。評価の際に代替ソリューションについて議論できるよう準備しておきましょう。

---

## 第VI章　演習1：スコアクランチャー

| | Exercise1 |
|---|---|
| ディレクトリ | ex1/ |
| 提出ファイル | ft_score_analytics.py |
| 使用可能 | `import sys`、`sys.argv`、`len()`、`sum()`、`max()`、`min()`、`print()` |

**ミッション概要**：コマンド通信をマスターしたところで、今度はデータのクリーンアップです！コマンドを送るユーザーは人間であり、ミスをすることがあります。

この演習では、スコアを格納するためにリストを使い、無効な入力（数値以外の値など）を適切に処理するために `try/except` ブロックを使用します。

ゲームスコアをコマンドライン引数として受け取り、以下を行ってください：

- コマンドライン引数を処理する
- 各エラーケース（引数なし、数値以外の値）を適切なメッセージで処理する
- スコアを格納・整理するための新しい**リスト**を作成する
- ゲームプレイヤーが喜ぶ基本統計を計算する（件数、合計、平均、最大、最小、レンジ）
- ゲーム仲間に自慢できるカッコいい出力にする（例を参考に）
- 有効・無効な入力が混在する場合、無効なものを除外して有効なものだけで処理を続ける（有効なものが一つもない場合を除く）

```
$> python3 ft_score_analytics.py 1500 2300 1800 2100 1950
=== Player Score Analytics ===
Scores processed: [1500, 2300, 1800, 2100, 1950]
Total players: 5
Total score: 9650
Average score: 1930.0
High score: 2300
Low score: 1500
Score range: 800

$> python3 ft_score_analytics.py
=== Player Score Analytics ===
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...

$> python3 ft_score_analytics.py ab ac
=== Player Score Analytics ===
Invalid parameter: 'ab'
Invalid parameter: 'ac'
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
```

---

## 第VII章　演習2：ポジショントラッカー

| | Exercise2 |
|---|---|
| ディレクトリ | ex2/ |
| 提出ファイル | ft_coordinate_system.py |
| 使用可能 | `import math`、`math.sqrt()`、`input()`、`round()`、`print()` |

**レベルアップ！** 3D座標をマスターする時が来ました！ゲームで特定の場所にテレポートしたり、3D空間の2点間の距離を求めたりした経験はありますか？まさにそれを構築します！

この演習では、3D座標（x, y, z）を格納するために**タプル**を使用します。

まず、`get_player_pos()` 関数を作成してください。この関数は：

- `x,y,z` 形式で新しいプレイヤー座標をユーザーに入力させる
- 不正な入力を処理する
- 有効な座標セットが入力されるまで再試行する
- プレイヤーの現在の3D座標を含むタプルを返す

次にコードで以下を行います：

- 最初の座標セットを取得する
- タプルを表示し、各座標を個別に表示する
- 3Dの中心（0, 0, 0）までの距離を計算する（下記参照）
- 新しい座標セットを取得する
- 2番目と最初の座標セット間の距離を計算する

**距離の公式**：2つの3D点間の距離はユークリッド距離公式 $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$ を使用します。これはピタゴラスの定理を3Dに拡張したものです！

```
$> python3 ft_coordinate_system.py
=== Game Coordinate System ===
Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': hello world
Invalid syntax
Enter new coordinates as floats in format 'x,y,z': 1.0 , 2.5, 3.0
Got a first tuple: (1.0, 2.5, 3.0)
It includes: X=1.0, Y=2.5, Z=3.0
Distance to center: 4.0311
Get a second set of coordinates
Enter new coordinates as floats in format 'x,y,z': 4,abc,5
Error on parameter 'abc': could not convert string to float: 'abc'
Enter new coordinates as floats in format 'x,y,z': 4,5,6
Distance between the 2 sets of coordinates: 4.9244
```

> 💡 `math.sqrt()` を使うにはスクリプトの先頭に `import math` と書くだけです。

> ℹ️ タプルは石に刻まれたデータのようなものです。一度作成したら変更できません。

---

## 第VIII章　演習3：アチーブメントハンター

| | Exercise3 |
|---|---|
| ディレクトリ | ex3/ |
| 提出ファイル | ft_achievement_tracker.py |
| 使用可能 | `len()`、`print()`、`import random`、`random.*`、`set()`、`set.union()`、`set.intersection()`、`set.difference()` |

**実績解除！** 最高にクールな実績システムを構築する時が来ました！レアな実績を解除した時の達成感を覚えていますか？今度はそれを追跡するシステムを構築します！

この演習では、ユニークな実績を格納し、プレイヤー間の実績コレクションを分析するために（和集合・積集合・差集合などの）操作を行うために**セット**を使用します。

`gen_player_achievements()` 関数を作成してください。大きな固定の実績リストからプレイヤーにランダムに実績を割り当てます。ランダムな数の実績を選び、そのリストから実績をピックしてセットとして返してください。

次にコードで以下を行います：

- 最低4人の異なるプレイヤーの実績セットを生成する
- 全プレイヤーのユニークな実績を追跡する
- 全プレイヤーに共通する実績を見つける
- 各プレイヤーについて、他の誰も持っていない実績を特定する
- 各プレイヤーについて、コンプリートに必要な不足実績をリストアップする

```
$> python3 ft_achievement_tracker.py
=== Achievement Tracker System ===
Player Alice: {'Crafting Genius', 'World Savior', ...}
...
All distinct achievements: {...}
Common achievements: {'Untouchable'}
Only Alice has: set()
...
Alice is missing: {'Strategist', 'Speed Runner', ...}
...
```

> 💡 実績の総数と各プレイヤーへの割り当て数を調整して、要求されるセットが空にならないようにしましょう。ところで、Pythonは空のセットをどのように表示しますか？そしてなぜでしょうか？

---

## 第IX章　演習4：インベントリマスター

| | Exercise4 |
|---|---|
| ディレクトリ | ex4/ |
| 提出ファイル | ft_inventory_system.py |
| 使用可能 | `import sys`、`sys.argv`、`len()`、`print()`、`sum()`、`list()`、`round()`、`dict.keys()`、`dict.values()`、`dict.update()` |

**ルート獲得！** RPGでインベントリを整理した経験はありますか？あの伝説の剣を持っているか確認する場面を。究極のインベントリシステムを構築しましょう！

この演習では、インベントリデータを格納するために**辞書**を使用します。

コードはまずコマンドライン引数を解析してインベントリを埋めます。各引数は `<アイテム名>:<数量>` の形式に従う必要があります。無効な引数（構文エラー、重複）はエラーメッセージとともに除外し、有効なものを辞書に格納します。辞書内の `<数量>` 値は後で計算できるよう `int` として保存します。

インベントリに対して以下の操作を行ってください：

- インベントリを表示する
- インベントリ内の全アイテムのリストを作成・表示する
- インベントリ内の全アイテムの合計数量を計算・表示する
- 各アイテムがインベントリに占める数量の割合を表示する
- 最も多いアイテムと最も少ないアイテムを報告する（同数の場合はコマンドラインで最初のものを選ぶ）
- 最後に新しいアイテムをインベントリに追加して再表示する

```
$> python3 ft_inventory_system.py sword:1 potion:5 shield:2 armor:3 helmet:1 sword:2 hello key:value
=== Inventory System Analysis ===
Redundant item 'sword' - discarding
Error - invalid parameter 'hello'
Quantity error for 'key': invalid literal for int() with base 10: 'value'
Got inventory: {'sword': 1, 'potion': 5, 'shield': 2, 'armor': 3, 'helmet': 1}
Item list: ['sword', 'potion', 'shield', 'armor', 'helmet']
Total quantity of the 5 items: 12
Item sword represents 8.3%
...
Item most abundant: potion with quantity 5
Item least abundant: sword with quantity 1
Updated inventory: {'sword': 1, 'potion': 5, 'shield': 2, 'armor': 3, 'helmet': 1, 'magic_item': 1}
```

> 💡 ゲームの最初、インベントリは通常空っぽです ;)

---

## 第X章　演習5：ストリームウィザード

| | Exercise5 |
|---|---|
| ディレクトリ | ex5/ |
| 提出ファイル | ft_data_stream.py |
| 使用可能 | `next()`、`range()`、`len()`、`print()`、`import typing`、`typing.Generator`、`import random`、`random.*` |

**魔法の時間！** ゲームがクラッシュせずに何百万ものイベントを処理できる仕組みを考えたことがありますか？Pythonのメモリ節約の秘密兵器、**ジェネレーター**の世界へようこそ！

この演習では、`yield` キーワードを使ったジェネレーターを使ってデータストリームをオンザフライで作成します。すべてをメモリに格納するのではなく、値をオンデマンドで生成するジェネレーター関数を実装する必要があります。

プレイヤーのリストからランダムな名前を、アクションのリストからランダムなアクションを選ぶ無限ジェネレーター関数 `gen_event()` を作成してください。このジェネレーターに対して `next()` が呼ばれるたびに、新しいイベントをタプル `(名前, アクション)` として返します。

スクリプトのメイン部分では、1000回ループして `gen_event()` から取得した1000個のイベントをすべて表示してください。

次に `gen_event()` で生成した10個のタプルのリストを作成してください。

最後に、前に作成したリストを受け取る新しいジェネレーター関数 `consume_event` を作成してください。リストが空になるまで、ランダムに要素を一つ選び、リストから削除してyieldします。このジェネレーターは `for .. in ..` 構文で直接使用してください。

---

## 第XI章　演習6：データアルケミスト

| | Exercise6 |
|---|---|
| ディレクトリ | ex6/ |
| 提出ファイル | ft_data_alchemist.py |
| 使用可能 | `import random`、`random.*`、`print()`、`len()`、`sum()`、`round()` |

**ラスボス戦！** すべてのデータ構造をマスターしました。今度はエレガントで凝縮された形でそれらを発見する時です！ここで真のデータアルケミストになりましょう！

この演習では、データを効率的に変換・フィルタリングするためにリストと辞書の**内包表記**を使用します。これはデータ処理における基本的なPythonの機能です。

一部が大文字で始まり、他はそうでないプレイヤー名のリストを作成してください。2つのリスト内包表記を作成してください：最初のものはすべての名前を大文字にした新しいリストを作成し、2番目のものは元のリストから大文字で始まる名前だけの新しいリストを作成します。

次に、完全に大文字化したプレイヤー名のリストから辞書を作成します。名前がキーとなり、値は定義された範囲でランダムに生成されたスコアです。もちろん内包表記で辞書を構築します。次に平均より高いスコアを持つ2番目の辞書を内包表記で作成します。

```
$> python3 ft_data_alchemist.py
=== Game Data Alchemist ===
Initial list of players: ['Alice', 'bob', 'Charlie', 'dylan', 'Emma', 'Gregory', 'john', 'kevin', 'Liam']
New list with all names capitalized: ['Alice', 'Bob', 'Charlie', 'Dylan', 'Emma', 'Gregory', 'John', 'Kevin', 'Liam']
New list of capitalized names only: ['Alice', 'Charlie', 'Emma', 'Gregory', 'Liam']
Score dict: {'Alice': 263, 'Bob': 666, 'Charlie': 907, ...}
Score average is 410.11
High scores: {'Bob': 666, 'Charlie': 907, 'Emma': 568, 'Gregory': 446, 'Kevin': 527}
```

> ℹ️ セットに対しても内包表記を使用することができます。

> ⚠️ 各内包表記は1行に収めること（行の長さを超える場合を除く）。

---

## 第XII章　提出について

いつも通りGitリポジトリに課題を提出してください。評価時にはリポジトリ内のコンテンツのみが評価されます。ファイル名が正しいかどうか必ず確認してください。

> ℹ️ 評価中は、データ構造の選択理由の説明、コレクション操作のデモ、分析システムの新機能追加などを求められる場合があります。各データ構造の背後にある原則をしっかり理解しておきましょう。

> ⚠️ 提出するのはこのプロジェクトで求められているファイルのみです。Pythonのコレクション型とデータ処理技術の習得を明確に示す、クリーンで適切にドキュメント化されたコードに集中してください。

---

# 演習0：コマンドクエスト解説

## 何をするか？

`sys.argv` というリストを使って、コマンドライン引数を表示するスクリプトを作ります。

---

## sys.argv とは？

```
python3 ft_command_quest.py hello world 42
```

このコマンドを実行すると、`sys.argv` の中身はこうなります：

```python
['ft_command_quest.py', 'hello', 'world', '42']
#  インデックス0          1        2        3
```

- `sys.argv[0]` → プログラム名
- `sys.argv[1]` 以降 → 引数

---

## 出力パターンの整理

引数なし（`len(sys.argv) == 1`）の場合：
```
=== Command Quest ===
Program name: ft_command_quest.py
No arguments provided!
Total arguments: 1
```

引数ありの場合：
```
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: hello
...
Total arguments: 4
```

---

## コード

```python
import sys


def main() -> None:
    args = sys.argv
    print("=== Command Quest ===")
    print(f"Program name: {args[0]}")

    if len(args) == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args) - 1}")
        for i, arg in enumerate(args[1:], start=1):
            print(f"Argument {i}: {arg}")

    print(f"Total arguments: {len(args)}")


main()
```

---

## ポイント解説

**`args[1:]` とは？**
リストのスライスです。インデックス1以降の要素を取り出します。
```python
args = ['ft_command_quest.py', 'hello', 'world']
args[1:]  # → ['hello', 'world']
```

**`enumerate(args[1:], start=1)` とは？**
リストをループしながら番号も取れます。
```python
for i, arg in enumerate(['hello', 'world'], start=1):
    print(i, arg)
# 1 hello
# 2 world
```

**`len(args) - 1` で引数の個数を出す理由は？**
`sys.argv[0]` はプログラム名なので、それを除いた数が「引数の数」になります。

---

## 動作確認

```bash
python3 ft_command_quest.py
python3 ft_command_quest.py hello world 42
python3 ft_command_quest.py "Data Quest"
```
