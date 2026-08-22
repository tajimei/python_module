# DataDeck — 抽象カードアーキテクチャ

**概要:** 抽象クラスとインターフェースを使ったPythonのデザインパターンを、モジュール式のカードシステムを構築しながら習得する。

**バージョン: 3.0**

## 目次

| 章 | タイトル | ページ |
|---|---|---|
| I | まえがき | 2 |
| II | AI利用に関する指示 | 3 |
| III | イントロダクション | 5 |
| IV | 全体的な指示 | 6 |
| V | 演習0: クリーチャーファクトリー | 7 |
| VI | 演習1: 能力（Capabilities） | 9 |
| VII | 演習2: 抽象ストラテジー | 11 |
| VIII | 提出 | 14 |

---

# 第I章 まえがき

すべてを捕まえろ。だが時に、本当の宝はその道中で身につけたスキルである。

---

# 第II章 AI利用に関する指示

### ● 背景

学習の過程で、AIはさまざまなタスクを手助けしてくれます。AIツールにどのような能力があり、それが自分の作業をどう支えてくれるのかを、時間をかけて探ってください。ただし、常に慎重に扱い、結果を批判的に評価すること。コード、ドキュメント、アイデア、技術的な説明のいずれであっても、自分の質問が適切だったか、生成された内容が正確かを完全に確信することはできません。仲間（ピア）は、誤りや盲点を避けるための貴重なリソースです。

### ● 主なメッセージ

- 反復的・退屈な作業を減らすためにAIを使う。
- コーディング／非コーディングの両面でプロンプトのスキルを磨く。これは将来のキャリアに役立つ。
- AIシステムの仕組みを学び、よくあるリスク・バイアス・倫理的問題を予測し回避できるようにする。
- 仲間と協働しながら、技術スキルとパワースキルの両方を伸ばし続ける。
- 完全に理解し、責任を持てるAI生成コンテンツのみを使用する。

### ● 学習者のルール

- AIツールを探究しその仕組みを理解する時間を取り、倫理的に使用し、潜在的なバイアスを減らせるようにすること。
- プロンプトを書く前に問題についてよく考えること。これにより、正確な語彙を用いた、より明確で詳細かつ的確なプロンプトが書けるようになります。
- AIが生成したものは、体系的に確認・レビュー・疑問視・テストする習慣を身につけること。
- 常にピアレビューを求めること。自分だけの検証に頼らないこと。

### ● フェーズの成果

- 汎用的なプロンプトスキルと、領域特化型のプロンプトスキルの両方を身につける。
- AIツールを効果的に使い、生産性を高める。
- 計算論的思考、問題解決力、適応力、協働力をさらに強化する。

### ● コメントと例

- 試験や評価など、本当に理解しているかを示さなければならない場面に定期的に遭遇します。準備を怠らず、技術面と対人面の両方のスキルを高め続けてください。
- 自分の推論を説明し、仲間と議論することで、理解の抜けが浮き彫りになることがよくあります。ピアラーニングを優先しましょう。
- AIツールはあなた固有の文脈を持たないことが多く、一般論的な回答をしがちです。同じ環境を共有する仲間のほうが、より適切で正確な洞察を与えてくれます。
- AIが「最もありそうな答え」を生成するのに対し、仲間は別の視点や有益なニュアンスを提供してくれます。品質のチェックポイントとして活用しましょう。

**✓ 良い実践**

AIに「ソート関数はどうテストすればいい?」と尋ねる。いくつかアイデアをもらう。それを試し、結果を仲間とレビューする。一緒にアプローチを改善する。

**✗ 悪い実践**

AIに関数まるごとを書かせ、プロジェクトにコピペする。ピア評価のとき、それが何をしているのか、なぜそうなのかを説明できない。信頼を失い、プロジェクトに落ちる。

**✓ 良い実践**

パーサーの設計をAIに手伝ってもらう。その後、ロジックを仲間と一緒にたどる。バグを2つ見つけ、一緒に書き直す。より良く、よりきれいで、完全に理解されたものになる。

**✗ 悪い実践**

プロジェクトの重要部分のコードをCopilotに生成させる。コンパイルは通るが、パイプをどう扱っているのか説明できない。評価の場で正当化できず、プロジェクトに落ちる。

---

# 第III章 イントロダクション

デッキアーキテクトを目指すあなた、DataDeckの世界へようこそ!

想像してみてください。あなたは、人気のモンスター収集ゲームに着想を得たクリーチャーカードゲームを設計しています。あなたのカードは単なる静的なオブジェクトではありません。ファミリー（系統）にグループ化でき、戦略的に使われる能力（capabilities）を持つ、動的なデータエンティティです。しかし、ここに課題があります。何千種類ものカードタイプを扱えるだけの柔軟性を持ちながら、クリーンで保守しやすいコードを保つシステムを、どうやって作るのか?

その秘訣は**抽象プログラミングパターン**にあります! 抽象クラスとポリモーフィズムは、以前のプロジェクトですでに扱いました。ここではさらに進んだパターン、すなわち**抽象ファクトリー**、**追加の能力（capabilities）**、そして**ストラテジーパターン**を使います。

このアクティビティでは、Creature（クリーチャー）の世界でカードを操作しながら、これらの高度なパターンを練習します。終わる頃には、進化・改善できるシステムを設計するシニアアーキテクトのように考えられるようになっているでしょう。

---

# 第IV章 全体的な指示

- プロジェクトは Python 3.10 以降で書くこと。
- プロジェクトは **flake8** のコーディング規約に準拠すること。
- すべてのコードに網羅的な型アノテーションを含めること。**mypy** で確認すること。
- 標準クラス・標準コレクション（int, str, list, dict など）とそのメソッドはすべて使用可。
- 組み込み関数はすべて使用可。ただし `eval()` と `exec()` は除く。
- クラッシュを避けるため、関数は例外を適切に処理すること。
- 外部ライブラリは禁止。

> **前提条件:** このアクティビティには、Pythonの継承、抽象クラス、ポリモーフィズム、import の習得が必要です。先に関連プロジェクトを完了しておくことを推奨します。

各演習フォルダには `__init__.py` ファイルが**必須**です。テスト用のコードはすべて、gitリポジトリのルートに配置します。

---

# 第V章 演習0: クリーチャーファクトリー

**ディレクトリ:** `ex0/`
**提出ファイル:** `battle.py`、および必要なファイルをすべて含むパッケージとしての `ex0/`
**使用許可:** 組み込み（builtins）、標準型、`import typing`、`import abc`

まずは基本的な Creature カードの作成からゲームを始めましょう。ただしご存知のとおり、Creature はさまざまなファミリーに分類され、進化することができます。この演習では**抽象ファクトリー**デザインパターンに焦点を当てます。`ex0/` フォルダに以下の要素を実装してください。

- **Creature** 抽象クラス。Creature の名前とタイプの属性、抽象メソッド `attack`、そして名前とタイプを使って定型メッセージを返す具象の汎用メソッド `describe` を持つ。
- Creature を継承する以下の具象クラス: **Flameling**、**Pyrodon**、**Aquabub**、**Torragon**。それぞれの `attack` メソッドは適切な文字列メッセージを返す（例を参照）。
- **CreatureFactory** 抽象クラス。抽象メソッド `create_base` と `create_evolved` を使って、同一ファミリーの基本 Creature と進化 Creature を生成できるようにする。
- CreatureFactory を継承する具象クラス **FlameFactory** と **AquaFactory**。各ファミリーの基本／進化 Creature の生成を担当する（FlameFactory は Flameling と Pyrodon、AquaFactory は Aquabub と Torragon）。
- `ex0` パッケージは具象 Creature を直接公開してはならない。ファクトリーのみを公開すること。

リポジトリのルートにある `battle.py` スクリプトが `ex0` パッケージをテストします。以下のシナリオを実装してください。

- Flameling と Aquabub のファクトリーをインスタンス化する。
- ファクトリーオブジェクトを受け取る単一の関数で、基本 Creature と進化 Creature を生成できること、そして各 Creature が describe でき attack できることを検証する。
- 両方のファクトリーを受け取り、基本 Creature 同士を戦わせる別の関数。

> 別の Creature を使っても構いませんが、扱う概念（ファミリーと抽象ファクトリー）は維持しなければなりません。

**例:**

```
$> python3 battle.py
Testing factory
Flameling is a Fire type Creature
Flameling uses Ember!
Pyrodon is a Fire/Flying type Creature
Pyrodon uses Flamethrower!

Testing factory
Aquabub is a Water type Creature
Aquabub uses Water Gun!
Torragon is a Water type Creature
Torragon uses Hydro Pump!

Testing battle
Flameling is a Fire type Creature
 vs.
Aquabub is a Water type Creature
 fight!
Flameling uses Ember!
Aquabub uses Water Gun!
```

---

# 第VI章 演習1: 能力（Capabilities）

**ディレクトリ:** `ex1/`
**提出ファイル:** `capacitor.py`、および必要なファイルをすべて含むパッケージとしての `ex1/`
**使用許可:** 組み込み（builtins）、標準型、`import typing`、`import abc`

いよいよ Creature に能力（capabilities）を追加します! しかしいつの日か、これらの能力は Creature 以外にも適用されるかもしれません。そこで、能力は分離しておきたい——**能力の抽象クラスは Creature 基底クラスを継承しません!**

`ex1/` フォルダ／パッケージに以下を実装してください。

- **HealCapability** 抽象クラス。抽象メソッド `heal` を定義する。このメソッドは、望むなら「target」パラメータを取っても構わない。
- **TransformCapability** 抽象クラス。抽象メソッド `transform` と `revert` を定義する。状態を永続化するための属性を持ち、それがこの能力を持つ Creature の `attack` の実装に影響する。
- シンプルに保ちましょう。これらのメソッドは、`attack` メソッドと同様に、動作を説明する単純な文字列を返します。
- Creature と HealCapability の**両方**を継承する以下の具象クラス: **Sproutling** と **Bloomelle**。これらは単一のファミリーを構成し、**HealingCreatureFactory**（CreatureFactory を継承）を通じて利用可能にする。
- Creature と TransformCapability の**両方**を継承する以下の具象クラス: **Shiftling** と **Morphagon**。これらは単一のファミリーを構成し、**TransformCreatureFactory**（CreatureFactory を継承）を通じて利用可能にする。
- 繰り返しますが、`ex1` パッケージは具象 Creature を直接公開してはならず、ファクトリーのみを公開すること。

> 当然ながら、`ex0` パッケージの内容を使い、その上にこの演習を構築しなければなりません。

次にテストシナリオを定義します。Gitリポジトリのルートにある `capacitor.py` スクリプトは、以下の手順で進みます。

- 回復（healing）Creature ファクトリーを作成する。
- 基本 Creature、続いて進化 Creature を作成し、それぞれに 1) describe させる、2) attack させる、3) heal させる。
- 変身（transforming）Creature ファクトリーを作成する。
- 基本 Creature、続いて進化 Creature を作成し、それぞれに 1) describe させる、2) attack させる、3) transform させる、4) 再度 attack させる、5) revert させる。

**例:**

```
$> python3 capacitor.py
Testing Creature with healing capability
 base:
Sproutling is a Grass type Creature
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
 evolved:
Bloomelle is a Grass/Fairy type Creature
Bloomelle uses Petal Dance!
Bloomelle heals itself and others for a large amount

Testing Creature with transform capability
 base:
Shiftling is a Normal type Creature
Shiftling attacks normally.
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
 evolved:
Morphagon is a Normal/Dragon type Creature
Morphagon attacks normally.
Morphagon morphs into a dragonic battle form!
Morphagon unleashes a devastating morph strike!
Morphagon stabilizes its form.
```

---

# 第VII章 演習2: 抽象ストラテジー

**ディレクトリ:** `ex2/`
**提出ファイル:** `tournament.py`、および必要なファイルをすべて含むパッケージとしての `ex2/`
**使用許可:** 組み込み（builtins）、標準型、`import typing`、`import abc`

前の演習で体験したとおり、異なる能力を持つ Creature は異なる振る舞いをします。今回の場合、回復ファミリーは攻撃の後に回復し、変身ファミリーは変身→攻撃→元に戻る、という流れになります。さまざまなファミリーから複数の Creature カードを引いてトーナメントで戦わせたいとき、各能力を把握したバトルコードが必要になります。……本当にそうでしょうか? **抽象ストラテジーパターン**を探究しましょう! そう、トーナメントの日がやってきたのです。

`ex2/` フォルダ／パッケージに以下を実装してください。

- **BattleStrategy** 抽象クラス。抽象メソッド `act` と `is_valid` を定義する。`is_valid` メソッドは、その Creature がそのストラテジーに適合するかを示す bool を返し、`act` メソッドはトーナメントスクリプトから呼び出される。
- BattleStrategy を継承する3つの具象クラス:
  - **NormalStrategy**: あらゆる Creature に適合し、トーナメント中は単に `attack` メソッドを使う。
  - **AggressiveStrategy**: 変身能力を持つ Creature に適合し、トーナメント中は transform → attack → revert を行う。
  - **DefensiveStrategy**: 回復能力を持つ Creature に適合し、トーナメント中は attack の後に heal を行う。
- 無効なストラテジーと Creature の組み合わせがテストされた場合、`is_valid` は `False` を返す。無効な組み合わせで `act` が呼ばれた場合は、明確なメッセージを持つ専用の例外を送出する。

いよいよトーナメントを作れます。Gitリポジトリのルートにある `tournament.py` スクリプトは、以下の手順で進みます。

- さまざまな Creature ファクトリーを作成する（ex0 と ex1 から）。
- 3つのストラテジーを作成する。
- 次のような単一のバトル関数を定義する:
  - トーナメントの対戦者リストを受け取る。各対戦者は、CreatureFactory と BattleStrategy からなるタプルとして定義される。
  - 各対戦者が他のすべての対戦者と一度ずつ戦うようにする。
  - 各 Creature に紐づいたストラテジーを使って各戦闘を進行させる。
  - 無効な Creature–ストラテジーのタプルを正しく処理する。

**例:**

```
$> python3 tournament.py
Tournament 0 (basic)
 [ (Flameling+Normal), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Flameling uses Ember!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

Tournament 1 (error)
 [ (Flameling+Aggressive), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy

Tournament 2 (multiple)
 [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]
*** Tournament ***
3 opponents involved

* Battle *
Aquabub is a Water type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Aquabub uses Water Gun!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

* Battle *
Aquabub is a Water type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Aquabub uses Water Gun!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.

* Battle *
Sproutling is a Grass type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
```

---

# 第VIII章 提出

いつものように、Gitリポジトリで課題を提出してください。ディフェンス（口頭評価）で評価されるのは、リポジトリ内の作業のみです。ファイル名が正しいか、必ず二重に確認してください。

> 評価の際、このプロジェクトで扱ったデザインパターンについて説明を求められることがあります。実装だけでなく、概念の理解に重点を置いてください。