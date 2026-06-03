# Code Cultivation: Object-Oriented Garden Systems

## 第3章 はじめに

CodeCultivationへようこそ！

最初のアクティビティでPythonの基礎を学んだ上で、今度はより複雑なプログラミングの課題に取り組みます。包括的なガーデンデータ管理システムを構築することで、Pythonを現実世界のシステムモデリングに活かす上級概念を学んでいきます。

取り組む内容：

- Pythonプログラムの構造と実行の仕組みを理解する
- オブジェクト指向アプローチによるデータの整理
- 再利用可能なコードコンポーネントの作成
- 適応・拡張できるシステムの構築
- 協働環境におけるデータの整合性の保護
- スケーラブルなソフトウェアアーキテクチャの設計

各演習は前の演習の上に積み重なっており、最終的には完全なデジタルガーデンエコシステムが完成します。

> **重要：** このモジュールはPythonプログラムの基本構造から始まり、オブジェクト指向プログラミングへと進んでいきます。各演習には要求された定義と必要なコードを含めてください。自分でテストするために、各ファイルの末尾に `if __name__ == "__main__":` ブロックを使ったシンプルなテストコードを含めることができます。

---

## 第4章 一般的な指示

- コードはPython 3.10以上で記述すること
- コードは`flake8`リンター基準に従うこと
- 各演習はそれぞれ独自のファイルとディレクトリに入れること
- 命名規則を守ること：クラスはPascalCase、関数と変数はsnake_case
- すべての関数とメソッドには型ヒントを含めること：`mypy`でコードを確認すること
- 明示的に指示がない限り、入力値のバリデーション処理は不要
- プログラミングの概念を明確に示すことに集中する
- プログラムは常にエラーなく動作すること

> **デジタルガーデンエコシステムについて：** このプロジェクトはPythonプログラミングの概念に焦点を当てており、基本的なプログラム構造からオブジェクト指向プログラミングへと進んでいきます。各演習では新しい機能を導入しながら、一貫したガーデン管理システムを構築します。後半の演習では前半の概念を再利用します。

> **オブジェクト指向プログラミングについて：** 演習1以降、このモジュールのすべての演習でクラスの使用が必要です。`class`や`def`などのPythonキーワードは言語の基本キーワードであるため、各演習の「使用許可関数」として列挙する必要はありません。

> 見やすい表示のために、文字列オブジェクトの`capitalize()`メソッドを使用することができます。これは「使用許可関数」には含まれませんが、必要であれば使用して構いません。

---

## 第5章 演習0：最初の種を植えよう

| | Exercise0 |
|---|---|
| | ft_garden_intro |
| ディレクトリ | ex0/ |
| 提出ファイル | ft_garden_intro.py |
| 使用許可 | print() |

複雑なガーデン管理システムを構築する前に、Pythonプログラムがどのように動作するかを理解する必要があります。

すべてのPythonプログラムには出発点、つまり実行が始まる場所が必要です。まるでガーデンに最初の種を植えるようなものです！

あなたのタスクは、ガーデンの植物に関する情報を表示する最初のPythonプログラムを作成することです。

**要件：**

- `python3 ft_garden_intro.py`で直接実行したときに動作するプログラムを作成すること
- 特別な`if __name__ == "__main__":` パターンを使用すること
- 以下の植物情報をシンプルな変数に格納すること：名前、高さ、樹齢
- `print()`を使って植物情報を表示すること
- 以下の出力例を模倣すること（評価時に厳密な出力チェックはありません）

**出力例：**
```
$> python3 ft_garden_intro.py
=== Welcome to My Garden ===
Plant: Rose
Height: 25cm
Age: 30 days
=== End of Program ===
```

> プログラムがどのように開始・実行されるかを理解することは、クラスなどのより複雑なオブジェクト指向の概念に進む前の基礎となります。

**注意：** この演習から以降のすべての演習（および将来のPythonプロジェクト）において、コードのテストに`if __name__ == "__main__":` ブロックを使用することが許可されています。このパターンは使用許可関数に明示されませんが、プロジェクト全体を通じて利用できます。

> `if __name__ == "__main__":` の行がなぜ重要なのかを説明できるようにしておく必要があります。これはインポートの概念につながるもので、今後のプロジェクトで取り上げられます。ただし、今のうちにこの良い習慣を身につけておくことが重要です。

> `#!`で始まる特別な行から始まるPythonファイルがあることに気づきましたか？この「シェバング」行が何をするのか、スクリプトを直接実行可能にするためになぜ有用なのかを調べてみましょう。評価ではスクリプトをその場でこの「シェバング」を使うように更新するよう求められます。

---

## 第6章 演習1：ガーデンデータオーガナイザー

| | Exercise1 |
|---|---|
| | ft_garden_data |
| ディレクトリ | ex1/ |
| 提出ファイル | ft_garden_data.py |
| 使用許可 | print() |

コミュニティガーデンでは、複数の植物の情報を管理する必要があります。いくつかの植物のデータを効率的に格納・表示する必要があります。

各植物には以下があります：
- 名前
- 高さ（センチメートル）
- 樹齢（日数）

少なくとも3種類の異なる植物のデータを管理し、整理された形で情報を表示するプログラムを作成してください。

**必須：** 各植物を個別に扱うのではなく、任意の植物のモデルとなる`Plant`クラスを作成する必要があります。すべてのprint()
    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 5 days]")
    for _ in range(5):
        tomato.grow()
        tomato.age()
    tomato.show()
    print("[statistics for Tomato]")
    display_stats(tomato)植物は上記の同じ属性（名前、高さ、樹齢）で記述されます。各植物についてクラスをインスタンス化し、その後属性に具体的な値をセットします。

植物情報を表示するための`show()`メソッドをクラス内に作成します。

**出力例：**
```
$> python3 ft_garden_data.py
=== Garden Plant Registry ===
Rose: 25cm, 30 days old
Sunflower: 80cm, 45 days old
Cactus: 15cm, 120 days old
```

> 現在、植物情報をどのように格納していますか？複数の方法があります。植物が増えるとどのような課題が生じるでしょうか？次の演習では、アプローチを発展させる必要が出てくるかもしれません。

> すでにPythonプログラミングやオブジェクト指向プログラミングの経験がある場合、直接高度な解法に進むでしょう。その場合、次のいくつかの演習が少し冗長に感じられるかもしれません。

---

## 第7章 演習2：植物成長シミュレーター

| | Exercise2 |
|---|---|
| | ft_plant_growth |
| ディレクトリ | ex2/ |
| 提出ファイル | ft_plant_growth.py |
| 使用許可 | print(), range(), round() |

ガーデンマネージャーは時間の経過に伴う植物の成長をシミュレートしたいと考えています。植物がどのように変化するかを追跡し、その状態を変更する操作を提供する必要があります。

**要件：**

- 演習1の`Plant`クラスを再利用する
- 植物が自分自身で`grow()`（成長）と`age()`（老化）できるようにする（つまり、これらはクラスのメソッドになります）
- ある植物の1週間の成長をシミュレートし、クラス内のデータにアクセスして最終的な高さを取得し、1週間の合計増加量を表示する
- `grow()`と`age()`を使ったときに植物がどのように変化すべきかを考える。異なる植物は異なる成長をしてもよい

プログラムは時間の経過とともに変化する植物を表示し、週末にサマリーを表示すること。植物に`grow()`の動作を変える「振る舞い」を与えることを考えてみましょう。

**出力例：**
```
$> python3 ft_plant_growth.py
=== Garden Plant Growth ===
Rose: 25.0cm, 30 days old
=== Day 1 ===
Rose: 25.8cm, 31 days old
（中略）
=== Day 7 ===
Rose: 30.6cm, 37 days old
Growth this week: 5.6cm
```

これを実現するための方法は複数あります。クラスへの属性の追加やメソッドへのパラメータ追加など、好きな方法で実装してください。

---

## 第8章 演習3：植物ファクトリー

| | Exercise3 |
|---|---|
| | ft_plant_factory |
| ディレクトリ | ex3/ |
| 提出ファイル | ft_plant_factory.py |
| 使用許可 | print(), range(), round() |

ガーデンセンターでは、`Plant`クラスを使って異なる初期値で多くの植物を素早く作成する必要があります。植物の作成プロセスを効率化し、新しい植物のクラスのインスタンス化と初期化を同時に行う必要があります。

**要件：**

- 植物を最初から初期情報（名前、初期高さ、初期樹齢）付きで直接作成できるようにする
- 各植物は構築直後にすぐに使用できる状態にする（例：`grow()`させたい場合など）
- 異なる特性を持つ少なくとも5種類の異なる植物を作成する
- 作成したすべての植物を整理された形式で表示する

前の演習からの`Plant`クラスを改善してください。なお、オブジェクト指向プログラミングをすでに知っていた場合は、演習1ですでに植物作成プロセスを効率化していたかもしれません。

**出力例：**
```
$> python3 ft_plant_factory.py
=== Plant Factory Output ===
Created: Rose: 25.0cm, 30 days old
Created: Oak: 200.0cm, 365 days old
Created: Cactus: 5.0cm, 90 days old
Created: Sunflower: 80.0cm, 45 days old
Created: Fern: 15.0cm, 120 days old
```

> `show()`メソッドをそのまま変更せずに上記の出力を表示できるようにしておく必要があります。

---

## 第9章 演習4：ガーデンセキュリティシステム

| | Exercise4 |
|---|---|
| | ft_garden_security |
| ディレクトリ | ex4/ |
| 提出ファイル | ft_garden_security.py |
| 使用許可 | print(), range(), round() |

ガーデンマネージャーはデータの整合性を心配しています。一部のボランティアが誤って無効な値（負の高さ、ありえない樹齢）を設定してしまい、植物データが破損しました。センシティブなデータを保護し、カプセル化する安全なシステムを作成する必要があります。

**要件：**

- `Plant`クラスを改善してデータが破損しないよう保護する
- 植物データを変更するための制御された方法を提供する：`set_height()`、`set_age()`
- 植物データに安全にアクセスする方法を提供する：`get_height()`、`get_age()`
- バリデーションによって植物の高さが負にならないようにする
- バリデーションによって植物の樹齢が負にならないようにする
- 無効な値が提供された場合、クラスからエラーメッセージを出力し、データをそのままにするかデフォルト値で植物を作成する
- カプセル化を使用する：「protected」規約（マングリングではない）を使用して、クラスの属性が直接使用されないようにする

データを格納する前に検証し、データの整合性を確保するシステムの作り方を考えてみましょう。

**出力例：**
```
$> python3 ft_garden_security.py
=== Garden Security System ===
Plant created: Rose: 15.0cm, 10 days old

Height updated: 25cm
Age updated: 30 days

Rose: Error, height can't be negative
Height update rejected
Rose: Error, age can't be negative
Age update rejected

Current state: Rose: 25.0cm, 30 days old
```

---

## 第10章 演習5：特化した植物タイプ

| | Exercise5 |
|---|---|
| | ft_plant_types |
| ディレクトリ | ex5/ |
| 提出ファイル | ft_plant_types.py |
| 使用許可 | super(), print(), range(), round() |

ガーデンでは今や異なる種類の植物（花、木、野菜）を扱う必要があります。各タイプは固有の特性を持ちながら、親カテゴリから共通の植物特性を継承します。

**要件：**

- 前の演習の`Plant`クラス（名前・高さ・樹齢の共通特性を持つ）から始める
- 特化したタイプを作成する：`Flower`、`Tree`、`Vegetable`
- 各特化タイプは基本的な植物特性を継承する
- `Flower`：`color`属性と`bloom()`能力が必要
- `Tree`：`trunk_diameter`属性と`produce_shade()`能力が必要
- `Vegetable`：`harvest_season`と`nutritional_value`属性が必要
- 特化した植物を作成する際は、`super()`を使って新しいクラスの内部から親メソッドを呼び出す（`__init__()`を含む任意のメソッドに適用可能）
- 特化クラスの`show()`を呼び出す際は、標準的な`Plant`の出力と特化した植物の追加特性を出力する。メソッドのオーバーライドでは、親クラスの既存コードを再利用できる
- 各植物タイプのインスタンスを少なくとも1つ作成する。花を咲かせる（bloom）。野菜の栄養価は0から始まり、`age()`と`grow()`メソッドが呼ばれるたびに増加させる
- 異なる特化タイプ間で共通の植物コードを重複させないようにする
- 3つの新しいクラスで新しい属性のバリデーションは不要

**出力例：**
```
$> python3 ft_plant_types.py
=== Garden Plant Types ===
=== Flower
Rose: 15.0cm, 10 days old
 Color: red
 Rose has not bloomed yet
[asking the rose to bloom]
Rose: 15.0cm, 10 days old
 Color: red
 Rose is blooming beautifully!

=== Tree
Oak: 200.0cm, 365 days old
 Trunk diameter: 5.0cm
[asking the oak to produce shade]
Tree Oak now produces a shade of 200.0cm long and 5.0cm wide.

=== Vegetable
Tomato: 5.0cm, 10 days old
 Harvest season: April
 Nutritional value: 0
[make tomato grow and age for 20 days]
Tomato: 47.0cm, 30 days old
 Harvest season: April
 Nutritional value: 20
```

> すべての植物タイプが共有する共通特性をどのように扱っていますか？これらの共通特性を処理するために異なるクラスで同じコードを繰り返さないことが推奨されます。

---

## 第11章 演習6：ガーデンアナリティクス

| | Exercise6 |
|---|---|
| | ft_garden_analytics |
| ディレクトリ | ex6/ |
| 提出ファイル | ft_garden_analytics.py |
| 使用許可 | super(), print(), range(), round(), staticmethod(), classmethod() |

前の演習のクラスを拡張してアナリティクスを表示します。複雑なデータの関係を扱い、ネストされたコンポーネントと継承チェーンを使用する必要があります。

**要件：**

- `Plant`クラスに、パラメータとして与えられた特定の樹齢が1年以上かどうかを確認する**スタティックメソッド**を作成する
- まだすべての情報がない場合に「匿名」の植物を直接作成できる**クラスメソッド**を作成する
- `Flower`を継承し、花が咲いたときの種の数を保持する`Seed`クラスを作成する。`show()`メソッドも対応して改善すること
- 各`Plant`には**ネストされたクラス**として実装された内部システムを持たせる。このシステムは統計データ（`grow()`の呼び出し回数、`age()`の呼び出し回数、`show()`の呼び出し回数）を保持する。カプセル化と表示関数が必要
- `Tree`には追加の統計データとして`produce_shade()`の呼び出し回数が必要
- 最後に、どんな種類の植物でも統計を表示する、クラスに属さない独自の関数を作成する

> スタティックメソッドとクラスメソッドのデコレータ構文も使用可能

**出力例：**
```
$> python3 ft_garden_analytics.py
=== Garden statistics ===
=== Check year-old
Is 30 days more than a year? -> False
Is 400 days more than a year? -> True

=== Flower
Rose: 15.0cm, 10 days old
 Color: red
 Rose has not bloomed yet
[statistics for Rose]
Stats: 0 grow, 0 age, 1 show
[asking the rose to grow and bloom]
Rose: 23.0cm, 10 days old
 Color: red
 Rose is blooming beautifully!
[statistics for Rose]
Stats: 1 grow, 0 age, 2 show
（以下省略）
```

> この演習はプロジェクト全体を通じて学んだすべてのプログラミングパターンを統合します。異なるコンポーネントが複雑なシステムの中でどのように相互作用し、組織化されるかの理解が評価されます。

---

## 第12章 提出について

通常通りGitリポジトリで課題を提出してください。評価（ディフェンス）ではリポジトリ内の作業のみが評価されます。ファイル名が正しいか必ず確認してください。また、`flake8`と`mypy`を使ってPythonの規約と型ヒントも確認してください。

> 評価時には、プログラミングの概念を説明したり、継承関係を示したり、新しい機能でコードを拡張するよう求められる場合があります。実装の背後にある原則を理解しておくようにしてください。

> 提出が必要なのは、このプロジェクトの課題で求められているファイルのみです。プログラミングの原則を明確に示す、クリーンでよくドキュメント化されたコードに集中してください。
 
---

# 1. `if __name__ == "__main__":` について

## `__name__` とは何か

Pythonはすべてのファイルに自動的に `__name__` という変数を用意します。

**値は実行方法によって変わります：**

| 実行方法 | `__name__` の値 |
|---|---|
| 直接実行 `python3 ファイル.py` | `"__main__"` |
| 別ファイルからインポート | ファイル名（例：`"ft_garden_intro"`） |

## 具体例で理解する

**`ft_garden_intro.py` を作ったとします：**
```python
print("=== Welcome to My Garden ===")
name = "Rose"
print("Plant:", name)
```

このまま書くと…

**直接実行した場合：** 意図通り動く ✅
```
$> python3 ft_garden_intro.py
=== Welcome to My Garden ===
Plant: Rose
```

**別のファイルからインポートした場合：** 勝手に実行されてしまう ❌
```python
# main.py
import ft_garden_intro  # インポートした瞬間に出力が走ってしまう！
```
```
=== Welcome to My Garden ===
Plant: Rose
```

---

## `if __name__ == "__main__":` で解決

```python
# ft_garden_intro.py
name = "Rose"

if __name__ == "__main__":
    print("=== Welcome to My Garden ===")
    print("Plant:", name)
```

| 実行方法 | 動作 |
|---|---|
| `python3 ft_garden_intro.py` | printが実行される ✅ |
| 別ファイルから `import ft_garden_intro` | printは実行されない ✅ |

**C言語で例えると：**
- C言語は `main()` 関数がエントリーポイントと決まっている
- Pythonにはそのルールがないので、`if __name__ == "__main__":` で自分でエントリーポイントを明示する

---
---

# 2. シェバング（`#!`）について

## シェバングとは

ファイルの**一番最初の行**に書く特別な記述です：

```python
#!/usr/bin/env python3
```

`#!` の2文字が「シェバング」と呼ばれます。

## 何をするのか

**シェバングなしの場合：**
```
$> python3 ft_garden_intro.py   # python3と明示する必要がある
```

**シェバングありの場合：**
```
$> ./ft_garden_intro.py   # python3を書かなくていい！
```

OS（Linux/Mac）がシェバングを読んで「このファイルはpython3で実行すればいいんだな」と自動判断してくれます。

## 使い方の手順

**① シェバングを1行目に書く：**
```python
#!/usr/bin/env python3

if __name__ == "__main__":
    name = "Rose"
    print("Plant:", name)
```

**② 実行権限を与える（これが必要）：**
```
$> chmod +x ft_garden_intro.py
```

**③ `./` で直接実行できる：**
```
$> ./ft_garden_intro.py
Plant: Rose
```

## `#!/usr/bin/env python3` の意味

| 部分 | 意味 |
|---|---|
| `#!` | シェバングの印 |
| `/usr/bin/env` | 環境からコマンドを探す命令 |
| `python3` | 使うインタープリター |

`/usr/bin/env python3` と書くことで、python3がどこにインストールされていても自動で見つけてくれます。

---

## まとめ

```python
#!/usr/bin/env python3        # ← シェバング：直接実行できるようにする

if __name__ == "__main__":    # ← インポート時に勝手に実行されないようにする
    name = "Rose"
    height = 25
    age = 30
    print("=== Welcome to My Garden ===")
    print("Plant:", name)
    print("Height:", str(height) + "cm")
    print("Age:", str(age) + " days")
    print("=== End of Program ===")
```

---

# `__main__` とは

## 一言で言うと

Pythonが「**このファイルが直接実行されたよ**」というサインとして自動的にセットする**文字列**です。

---

## `__` （ダンダー）について

まず名前の形に注目してください。

`__main__` のように**前後に `__` がついている**ものをPythonでは **「ダンダー（dunder）」** と呼びます。

これは **Python自身が内部で使う特別な名前** という意味です。自分で `__main__` という名前を作ったわけではなく、**Pythonが自動的に用意してくれるもの**です。

---

## 動きのイメージ

```python
# test.py を直接実行したとき
print(__name__)  # "__main__" と表示される
```

```python
# test.py を別ファイルからインポートしたとき
# → __name__ は "test" になる
```

Pythonは実行時に自動で `__name__` に値をセットします。

| 状況 | Pythonが自動でセットする値 |
|---|---|
| 直接実行 | `"__main__"` |
| インポートされた | `"ファイル名"` |

---

## C言語と比べると

C言語では `main()` 関数がエントリーポイントとして**言語のルールで決まっています**。

```c
int main(void)  // ← これがエントリーポイントとルールで決まっている
{
    return 0;
}
```

Pythonにはそのルールがないので、代わりに `__name__` の値を使って**自分でエントリーポイントを判断する**わけです。

```python
if __name__ == "__main__":  # ← 「直接実行されたとき」という意味
    # ここがエントリーポイント
```

---

## まとめ

- `__main__` は特別な**文字列**
- Pythonが「直接実行されたファイル」に自動でセットする
- `__` がついているのは「Pythonが内部で使う特別なもの」というサイン
- `if __name__ == "__main__":` は「このファイルが直接実行されたときだけ処理する」という意味

---
# `round()` の使い方

## 基本的な使い方

```python
round(数値, 小数点以下の桁数)
```

---

## 具体例

```python
round(27.400000000000002, 1)  # → 27.4
round(28.200000000000003, 1)  # → 28.2
round(29.000000000000004, 1)  # → 29.0
```

第2引数に `1` を渡すと**小数点以下1桁**に丸めます。

---

## 第2引数を変えると

```python
round(27.456, 0)  # → 27.0  （小数点以下0桁）
round(27.456, 1)  # → 27.5  （小数点以下1桁）
round(27.456, 2)  # → 27.46 （小数点以下2桁）
round(27.456, 3)  # → 27.456（小数点以下3桁）
```

---

## 第2引数を省略すると

```python
round(27.456)  # → 27 （整数に丸める）
```

---

## C言語との比較

C言語では`printf`のフォーマットで桁数を指定していました：

```c
printf("%.1f\n", 27.456);  // → 27.5
```

Pythonの`round()`は**値そのものを丸める**のに対して、C言語の`%.1f`は**表示だけを丸める**という違いがあります。

---

## 今回の使い方

```python
def show(self) -> None:
    height = round(self.height, 1)  # 表示用に1桁に丸める
    print(self.name + ": " + str(height) + "cm, "
          + str(self._age) + " days old")
```

`self.height`の値自体は変えずに、**表示するときだけ丸めています。**

----
# 演習4：ガーデンセキュリティシステム

## やること

**データを保護して、無効な値（負の数）が入らないようにする**

---

## 演習3からの変更点

| 演習3 | 演習4 |
|---|---|
| 属性に直接アクセスできる | 属性を保護する |
| 無効な値も入れられる | 無効な値を弾く |
| getter/setterなし | getter/setterを追加 |

---

## 「protected」規約とは

属性名の前に `_` を1つつけます：

```python
self._height = 0.0  # protectedな属性
self._age = 0       # protectedな属性
```

これは**「直接触らないでください」というサイン**です。C言語にはない概念ですが、Pythonではこの規約が慣習になっています。

---

## getter/setterとは

属性に**安全にアクセス・変更するためのメソッド**です。

```python
# setter：値をセットする（バリデーションあり）
def set_height(self, height: float) -> None:
    if height < 0:
        print(self._name + ": Error, height can't be negative")
    else:
        self._height = height
        print("Height updated: " + str(height) + "cm")

# getter：値を取得する
def get_height(self) -> float:
    return self._height
```
---

## 重要なポイント

演習3では属性に直接アクセスしていました：

```python
rose.height = 25.0  # 直接アクセス（演習3まで）
```

演習4からはsetterを通してアクセスします：

```python
rose.set_height(25.0)  # setterを通してアクセス（演習4から）
```

これが**カプセル化**の考え方です。データを守るために外から直接触れないようにします。

---
# `_Stats` はネストされたクラスです

## ネストされたクラスとは

**クラスの中にクラスを定義すること**です。

```python
class Plant:
    class _Stats:  # Plantの中にあるクラス
        def __init__(self) -> None:
            self._grow_count: int = 0
```

---

## なぜ`_`がついているのか

演習4で学んだ**protected規約**と同じです。

```python
class _Stats:   # 「外から直接使わないでください」というサイン
```

---

## なぜPlantの中に書くのか

`_Stats`は**Plantのためだけに存在するクラス**だからです。

```python
# 外に書く場合 → どこからでも使える
class Stats:
    pass

class Plant:
    pass

# 中に書く場合 → Plantのためだけのクラスと明示できる
class Plant:
    class _Stats:  # Plantに関係するものをまとめられる
        pass
```

---

## C言語で例えると

C言語では構造体の中に構造体を入れることができます：

```c
typedef struct s_stats
{
    int grow_count;
    int age_count;
    int show_count;
}   t_stats;

typedef struct s_plant
{
    char    *name;
    float   height;
    int     age;
    t_stats stats;  // 構造体の中に構造体
}   t_plant;
```

Pythonのネストされたクラスはこれに近いイメージです。

---

## 使い方

```python
class Plant:
    class _Stats:
        def __init__(self) -> None:
            self._grow_count: int = 0

    def __init__(self) -> None:
        self._stats = Plant._Stats()  # ← こうやってインスタンス化
```

`Plant._Stats()` と書くことで「Plantの中の_Statsクラス」を使えます。

---

```python
print()
    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 5 days]")
    for _ in range(5):
        tomato.grow()
        tomato.age()
    tomato.show()
    print("[statistics for Tomato]")
    display_stats(tomato)
```
