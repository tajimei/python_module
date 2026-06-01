# Garden Guardian - 課題内容

---

## 第IV章　全般的な指示

- プログラムはPython 3.10以上で記述すること
- コードはflake8リンター基準に準拠すること
- すべての関数・メソッドにtype hintsを記述すること：`mypy`でコードをチェックすること
- 各課題は独自のファイルに記述すること
- 基本的なエラーハンドリングの概念を明確に示すこと
- 正常な動作とエラーのシナリオの両方を示すこと
- 組み込みの例外を適切に使用すること
- シンプルで学習に集中したソリューションを維持すること
- **プログラムは絶対にクラッシュしてはならない**

**データエンジニアリングに関する注意：** このプロジェクトは農業システム向けの耐障害性データパイプライン設計を教えます。実世界の農業シナリオを優雅に処理する、フォールトトレラントな監視システムを構築する方法をコードで示すこと。

> **Exception Handling：** このモジュールのすべての課題では、エラーハンドリングに`try/except`ブロックの使用が必須です。`try`、`except`、`finally`、`raise`などのPythonキーワードは言語の基本機能であり、authorized functionsに列挙する必要はありません。

> 課題を完了するために必要な組み込み例外型はすべて使用可能です。`ValueError`、`TypeError`、`ZeroDivisionError`、`FileNotFoundError`、`KeyError`、`IndexError`、`AttributeError`、基底クラスの`Exception`などが含まれますが、これらに限りません。各課題の説明には、その課題に最も適した例外型が記載されている場合があります。

---

## 第V章　Exercise 0：Agricultural Data Validation

| | Exercise0 |
|---|---|
| | ft_first_exception |
| Directory: | `ex0/` |
| Files to Submit: | `ft_first_exception.py` |
| Authorized: | `int()`、`print()` |

スマート農業データパイプラインは、フィールドセンサーから気温の読み取り値を受信します。センサーが破損したデータを送信したり、農家がモバイルアプリから無効な値を入力したりすることがあります。農業分析を汚染する前に不正なデータをフィルタリングするデータ検証レイヤーを作成する必要があります。

`input_temperature(temp_str)` という関数を作成してください：

- 文字列を引数として受け取る
- 数値に変換する
- 気温を整数として返す

次に、`input_temperature()` に対して以下のテストを実行する `test_temperature()` 関数を作成してください：

- 有効な入力（`"25"`）を使用する
- 無効な入力（`"abc"`）を使用する
- `input_temperature()` が失敗した場合を処理し、エラーメッセージを表示する
- エラーが発生してもプログラムが動作し続けることを示す

**実行例：**
```
$> python3 ft_first_exception.py
=== Garden Temperature ===
Input data is '25'
Temperature is now 25°C
Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'
All tests completed - program didn't crash!
```

> 基底クラスの`Exception`を使用するか、`input_temperature()`が発生させうる例外を調べることができます。

> これら2つの関数のtype hintsを適切に設定するのはあなた次第です。この情報はすべての課題および今後のプロジェクトにも有効です。

---

## 第VI章　Exercise 1：Agricultural Data Validation Pipeline

| | Exercise1 |
|---|---|
| | ft_raise_exception |
| Directory: | `ex1/` |
| Files to Submit: | `ft_raise_exception.py` |
| Authorized: | `int()`、`print()` |

データをより細かく制御する必要があります。気温が有効な数値であっても、寒すぎたり暑すぎたりすると植物は育ちません。

Exercise 0のコードを使用し、`input_temperature()` と `test_temperature()` を以下のように改良してください：

**`input_temperature` の改良：**
- 気温が植物にとって適切な範囲かチェックする（摂氏0〜40度、両端含む）
- 有効な場合は気温を返す、そうでない場合は例外を`raise`する

**`test_temperature` の改良：**
- 極端な値（`"100"`、`"-50"`）を使った新しいテストを追加する

ファイルの`main`部分で `test_temperature()` を呼び出すこと。

**実行例：**
```
$> python3 ft_raise_exception.py
=== Garden Temperature Checker ===
Input data is '25'
Temperature is now 25°C
Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'
Input data is '100'
Caught input_temperature error: 100°C is too hot for plants (max 40°C)
Input data is '-50'
Caught input_temperature error: -50°C is too cold for plants (min 0°C)
All tests completed - program didn't crash!
```

---

## 第VII章　Exercise 2：Different Types of Problems

| | Exercise2 |
|---|---|
| | ft_different_errors |
| Directory: | `ex2/` |
| Files to Submit: | `ft_different_errors.py` |
| Authorized: | `print()`、`open()`、`int()` |

ガーデンプログラムはさまざまな種類の問題に遭遇する可能性があります。Pythonには状況に応じた異なる種類のエラーがあり、それらを個別に、またはまとめてキャッチできます。

`garden_operations(operation_number)` という関数を作成してください。この関数には意図的に欠陥のあるコードを含めます。`operation_number` が0〜3の各値に対して、異なる欠陥コードが以下のいずれかの例外を発生させます：

- `ValueError` — 不正なデータが提供された場合（例：`int()`に数値の代わりに`"abc"`を渡す）
- `ZeroDivisionError` — ゼロで割り算しようとした場合
- `FileNotFoundError` — 存在しないファイルを開こうとした場合（開いていなければ`close()`不要）
- `TypeError` — 混合できない異なる型を混合しようとした場合（文字列と数値を足し算しようとするなど）

`operation_number` の他の値では欠陥コードを含まず、単純にreturnします。

`test_error_types()` 関数を作成してください：

- 各種エラーが発生することを示す
- 各エラーをキャッチして何が問題だったか説明する
- 各エラーの後もプログラムが動作し続けることを示す
- 1つの`try:`ブロックで複数のエラー型をキャッチする方法を示す

**実行例：**
```
$> python3 ft_different_errors.py
=== Garden Error Types Demo ===
Testing operation 0...
Caught ValueError: invalid literal for int() with base 10: 'abc'
Testing operation 1...
Caught ZeroDivisionError: division by zero
Testing operation 2...
Caught FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'
Testing operation 3...
Caught TypeError: can only concatenate str (not "int") to str
Testing operation 4...
Operation completed successfully
All error types tested successfully!
```

> Pythonにはなぜ異なる種類のエラーがあるのか？1つの`try:`だけで複数の型のエラーをキャッチするにはどうすればよいか？なお、`type()`は使用不可です。

> `TypeError`を発生させる欠陥コードに対して、mypyはエラーを表示します。それはmypyの仕事です！そのため、この例外をテストするには、このエラーを意図的に残す必要があります。

> `open()`はCですでに使ったことがあります。Pythonでの使い方はとても簡単です。

---

## 第VIII章　Exercise 3：Making Your Own Error Types

| | Exercise3 |
|---|---|
| | ft_custom_errors |
| Directory: | `ex3/` |
| Files to Submit: | `ft_custom_errors.py` |
| Authorized: | `print()` |

Pythonの組み込みエラーがガーデンプログラムには具体的でない場合があります。独自のエラー型を作成することで、コードをより明確で役立つものにできます。

以下のシンプルなカスタム例外クラスを作成してください：

- `GardenError` — ガーデンの問題に関する基本エラー
- `PlantError` — 植物の問題用（`GardenError`を継承）
- `WaterError` — 水やりの問題用（`GardenError`を継承）

各カスタム例外は以下の要件を満たすこと：

- `Exception`（または`GardenError`）を継承するシンプルなクラスであること
- メッセージが提供されない場合のデフォルトエラーメッセージを持つこと（例：`"Unknown plant error"`）

以下を行う関数を作成してください：

- 異なる状況でカスタムエラーを`raise`する
- 特定のエラー型をキャッチする方法を示す
- `GardenError`をキャッチするとすべてのガーデン関連エラーがキャッチされることを示す

**実行例：**
```
$> python3 ft_custom_errors.py
=== Custom Garden Errors Demo ===
Testing PlantError...
Caught PlantError: The tomato plant is wilting!
Testing WaterError...
Caught WaterError: Not enough water in the tank!
Testing catching all garden errors...
Caught GardenError: The tomato plant is wilting!
Caught GardenError: Not enough water in the tank!
All custom error types work correctly!
```

> Pythonの組み込みエラーの代わりに独自のエラー型を作成すべきなのはどんな場合か？継承はどのように異なる種類のエラーを整理するのに役立つか？

---

## 第IX章　Exercise 4：Finally Block - Always Clean Up

| | Exercise4 |
|---|---|
| | ft_finally_block |
| Directory: | `ex4/` |
| Files to Submit: | `ft_finally_block.py` |
| Authorized: | `print()`、`str.capitalize()` |

ガーデンプログラムはエラーが発生した場合でもリソースをクリーンアップする必要があります。`finally`ブロックはこのために最適です — エラーがあってもなくても、常に実行されます。

`water_plant(plant_name)` という関数を作成してください：

- 植物に水をやろうとする
- 植物名が大文字始まり（capitalized）の場合は成功する
- 植物名が大文字始まりでない場合はエラーを`raise`する（前の課題の`PlantError`例外を使用）
- 成功時にメッセージを表示する

`test_watering_system()` 関数を作成してください：

- 散水システムを起動する（メッセージを表示するだけ）
- `water_plant()` を使って複数の植物に水をやる
- `try/except/finally` 構造を使用する
- 植物名が無効で水をやれない場合のエラーを処理する。その場合はテストを中止し、すぐに`main`に返る
- `finally`ブロックで必ず散水システムを閉じる
- エラーがあっても必ずクリーンアップが実行されることを示す

**実行例：**
```
$> python3 ft_finally_block.py
=== Garden Watering System ===
Testing valid plants...
Opening watering system
Watering Tomato: [OK]
Watering Lettuce: [OK]
Watering Carrots: [OK]
Closing watering system
Testing invalid plants...
Opening watering system
Watering Tomato: [OK]
Caught PlantError: Invalid plant name to water: 'lettuce'
.. ending tests and returning to main
Closing watering system
Cleanup always happens, even with errors!
```

> エラーが発生した場合でもリソースをクリーンアップすることが重要なのはなぜか？`finally`ブロックはクリーンアップが必ず実行されることをどのように保証するのか？

---

## 第X章　提出について

課題をいつも通りGitリポジトリに提出してください。評価時に採点されるのはリポジトリ内の作業のみです。ファイル名が正しいかどうか必ず確認してください。

> 評価中は、エラーハンドリングの概念の説明、ガーデンプログラムにおける例外の動作のデモ、またはシステムが異なる種類の問題をどのように処理するかの説明を求められる場合があります。コードの背後にある原則を理解していることを確認してください。

> このプロジェクトの課題で要求されたファイルのみを提出してください。エラーハンドリングと防衛的プログラミングの概念を明確に示す、きれいで読みやすいコードに集中してください。

---

# Python 例外処理の基本概念

## 1. try / except — エラーをキャッチする

```python
try:
    # エラーが起きるかもしれないコード
    result = int("abc")
except ValueError:
    # エラーが起きたときの処理
    print("変換できません")
```

`try` の中でエラーが発生すると、即座に `except` に飛びます。プログラムはクラッシュせず続行されます。

---

## 2. except の種類

### 特定のエラーをキャッチ
```python
except ValueError:      # 値が不正
except TypeError:       # 型が不正
except ZeroDivisionError:  # ゼロ除算
```

### エラーメッセージも取得
```python
except ValueError as e:
    print(e)  # エラーの詳細メッセージが見られる
```

### 複数まとめてキャッチ
```python
except (ValueError, TypeError) as e:
    print(e)
```

### すべてのエラーをキャッチ
```python
except Exception as e:
    print(e)
```

---

## 3. raise — 意図的にエラーを発生させる

```python
def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    if temp > 40:
        raise ValueError("40度を超えています")  # 自分でエラーを起こす
    return temp
```

`raise` は「このデータはおかしい」と判断したときに、自分でエラーを投げるために使います。

---

## 4. finally — 必ず実行される

```python
try:
    result = int("abc")
except ValueError:
    print("エラー発生")
finally:
    print("これは必ず実行される")  # エラーがあってもなくても
```

ファイルのクローズなど「後片付け」に使います。

---

## 5. 独自の例外クラス — カスタムエラー

```python
class GardenError(Exception):
    pass

class PlantError(GardenError):
    pass

raise PlantError("トマトが枯れています")
```

継承を使うことで、エラーを階層的に整理できます。

```
Exception
  └── GardenError
        ├── PlantError
        └── WaterError
```

`GardenError` をキャッチすれば `PlantError` も `WaterError` もまとめてキャッチできます。

---

## 全体の流れイメージ

```
try
 │
 ├─ 正常 ──────────────────────→ finally → 続行
 │
 └─ エラー発生
       │
       ├─ except で一致 ────────→ finally → 続行
       │
       └─ except で一致しない →  finally → クラッシュ
```

---

## この課題で学ぶ順番

| Exercise | 学ぶこと |
|---|---|
| Ex0 | `try/except` の基本 |
| Ex1 | `raise` で自分でエラーを投げる |
| Ex2 | 複数の例外型を使い分ける |
| Ex3 | 独自の例外クラスを作る |
| Ex4 | `finally` で後片付けをする |
