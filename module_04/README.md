# Data Archivist — 5ページ以降の和訳

---

## 第III章　共通ルール

### III.1　一般ルール

- すべてのプログラムはPython 3.10以降で記述すること。
- コードはflake8リンター標準に準拠すること。
- すべての関数・メソッドには型ヒントを付けること。確認にはmypyを使用すること。
- 関数はクラッシュを避けるため、例外を適切に処理すること。
- 指定されたGitリポジトリに提出すること。
- リポジトリ内のコンテンツのみが評価対象となる。

> ⚠️ **上級者向け注意：** `with` 文は演習3で導入されます。それ以前には使用してはいけません。

> ℹ️ 使用が許可されている標準型とコレクション（関連するメソッド・コンストラクタを含む）：`str`, `int`, `float`, `list`, `dict`, `set`, `tuple`

### III.2　出力仕様

各演習には、推奨される出力フォーマットを示すターミナル例があります。基本的な構造は維持しなければなりませんが、ファイル操作への理解を反映させたメッセージにカスタマイズしても構いません（必須情報が保持されている限り）。

---

## 第IV章　演習0：古代テキストの復元

| | Exercise0 |
|---|---|
| 関数名 | ft_ancient_text |
| ディレクトリ | ex0/ |
| 提出ファイル | ft_ancient_text.py |
| 使用許可 | `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.close()`, `print()` |

**ミッション説明：** アーカイブは保管庫7に古いデータの断片を発見しました。データアーキビストとしてのあなたの最初の任務は、さらに劣化する前にこの貴重な情報を復元することです。

コマンドラインからファイル名を取得し、`cat` コマンドのようにファイルの内容を読み込んで表示してください。例に示すようにヘッダーとフッターを追加してください。また、様々な失敗ケース（存在しないファイル、アクセス不可なファイルなど）を処理する必要があります。

> ℹ️ `open()` が返すデータの型は何ですか？

**実行例：**
```
$> python3 ft_ancient_text.py
Usage: ft_ancient_text.py <file>

$> python3 ft_ancient_text.py foo
=== Cyber Archives Recovery ===
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'

$> python3 ft_ancient_text.py ancient_fragment.txt
=== Cyber Archives Recovery ===
Accessing file 'ancient_fragment.txt'
---
[FRAGMENT 001] ...
---
File 'ancient_fragment.txt' closed.
```

---

## 第V章　演習1：アーカイブの作成

| | Exercise1 |
|---|---|
| 関数名 | ft_archive_creation |
| ディレクトリ | ex1/ |
| 提出ファイル | ft_archive_creation.py |
| 使用許可 | `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.write()`, `io.close()`, `print()`, `input()` |

**ミッション説明：** データ復元お疲れ様でした！次の任務は、新しいアーカイブエントリを作成することで、新しい保存プロトコルを確立することです。

前の演習で作成したコードを使用し、スクリプトの末尾に以下の改良を加えてください：

- 各行の末尾に特別なアーカイブ文字（`#`）を追加する（2087年互換のため）
- 新しい内容を表示する
- 保存先のファイル名をユーザーに入力させる（空のままにすると保存しない）
- ファイル名が入力された場合は新しい内容を保存し、終了メッセージを表示する

> ℹ️ ファイルが既に存在する場合は作成または上書きすること。

---

## 第VI章　演習2：ストリーム管理

| | Exercise2 |
|---|---|
| 関数名 | ft_stream_management |
| ディレクトリ | ex2/ |
| 提出ファイル | ft_stream_management.py |
| 使用許可 | `import sys`, `sys.argv`, `sys.stdin`, `sys.stdout`, `sys.stderr`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.readline()`, `io.write()`, `io.flush()`, `io.close()`, `print()` |

**ミッション説明：** アーカイブはデジタル文明の創設以来稼働し続けている3つの神聖なデータチャンネルを通じて運営されています。インターネットよりも古いこれらのチャンネルをマスターしましょう！

前の演習のコードを更新して以下を実装してください：

- 例外によるエラーメッセージを標準出力ではなく**エラー出力ストリーム**に出力する（明確なプレフィックス付き、例参照）
- `input()` 組み込み関数を使わずにユーザー入力を取得する

**実行例（エラー時）：**
```
[STDERR] Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

---

## 第VII章　演習3：ヴォールトセキュリティ

| | Exercise3 |
|---|---|
| 関数名 | ft_vault_security |
| ディレクトリ | ex3/ |
| 提出ファイル | ft_vault_security.py |
| 使用許可 | `open()`, `read()`, `write()`, `print()` |

**ミッション説明：** チーフアーキビストはあなたの才能に気づき、ヴォールトセキュリティ部門に昇進させます。ここが本物のアーキビストが実力を証明する場所です。

この演習では、適切なファイル処理を保証するために `with` 文（コンテキストマネージャ）の使用が必須です。`with` 文はエラーが発生した場合でも自動的にファイルを閉じ、リソースのリークを防ぎます。

任意のファイルへの安全なアクセスを提供する `secure_archive()` 関数を作成してください。この関数は操作が成功したかどうか（真偽値）と関連する内容（ファイルの内容またはエラーメッセージ）を示す `(True|False, str)` のタプルを返します。関数のパラメータは：必須のファイル名、実行するアクション（読み取りまたは書き込み）を示すオプションの `int` または `str`、ファイルに書き込む内容を含むオプションの文字列です。

> 評価時には、上記の要件に合致しているかコードの構造が確認されます。

**実行例：**
```
=== Cyber Archives Security ===

Using 'secure_archive' to read from a nonexistent file:
(False, "[Errno 2] No such file or directory: '/not/existing/file'")

Using 'secure_archive' to read from a regular file:
(True, '[FRAGMENT 001] ...\n...')

Using 'secure_archive' to write previous content to a new file:
(True, 'Content successfully written to file')
```

---

## 第VIII章　提出について

通常通り、Gitリポジトリに課題を提出してください。評価時に採点されるのはリポジトリ内のコンテンツのみです。ファイル名が正しいか必ず確認してください。

> ℹ️ 評価中は、ファイル操作の説明、エラーハンドリングのデモ、または `with` 文の動作説明を求められる場合があります。各演習の背後にある概念を必ず理解しておいてください。

> ⚠️ 提出するのはプロジェクト仕様が要求するファイルのみです。ファイル操作への理解を明確に示す、シンプルでクリーンなコードに集中してください。

# 演習0「古代テキストの復元」の解き方

## 課題の目標

コマンドライン引数でファイル名を受け取り、`cat` コマンドのように内容を表示するスクリプトを作ること。

---

## ステップごとの解説

### ステップ1：引数のチェック

```python
import sys

if len(sys.argv) != 2:
    print("Usage: ft_ancient_text.py <file>")
    sys.exit()
```

`sys.argv` はコマンドライン引数のリストです。
- `sys.argv[0]` = スクリプト名
- `sys.argv[1]` = ファイル名（ユーザーが渡すもの）

引数が2つ（スクリプト名＋ファイル名）でなければ使い方を表示して終了します。

---

### ステップ2：ヘッダーを表示する

```python
print("=== Cyber Archives Recovery ===")
print(f"Accessing file '{sys.argv[1]}'")
```

---

### ステップ3：ファイルを開いて読む（例外処理付き）

ここが核心です。`open()` はファイルが存在しない・権限がないとき例外を投げます。

```python
filename: str = sys.argv[1]
file: typing.IO = None

try:
    file = open(filename, "r")
except OSError as e:
    print(f"Error opening file '{filename}': {e}")
    sys.exit()
```

`OSError` は以下を両方カバーします：
- `FileNotFoundError`（Errno 2：ファイルが存在しない）
- `PermissionError`（Errno 13：アクセス権限なし）

---

### ステップ4：内容を表示してファイルを閉じる

```python
content: str = file.read()
print("---")
print(content, end="")
print("---")
file.close()
print(f"File '{filename}' closed.")
```

---

## 完成イメージ

```python
import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    file: typing.IO = None

    try:
        file = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    content: str = file.read()
    print("---")
    print(content, end="")
    print("---")
    file.close()
    print(f"File '{filename}' closed.")


main()
```

---

## 重要なポイントまとめ

| ポイント | 説明 |
|---|---|
| `sys.argv` | コマンドライン引数を受け取るリスト |
| `open(filename, "r")` | ファイルを読み取りモードで開く |
| `file.read()` | ファイル全体を文字列として読む |
| `file.close()` | ファイルを必ず閉じる（演習0・1・2では`with`禁止） |
| `OSError` | ファイル関連のエラーをまとめて捕捉できる |
| 型ヒント | `filename: str`、`typing.IO` など必須 |

---

## チェックリスト

- [ ] 引数なし → Usageメッセージ表示
- [ ] 存在しないファイル → エラーメッセージ表示
- [ ] 権限のないファイル → エラーメッセージ表示
- [ ] 正常なファイル → 内容を`---`で囲んで表示
- [ ] `file.close()` を呼んでいる
- [ ] 型ヒントがすべてついている
- [ ] flake8でエラーが出ない

## `file: typing.IO = None` の意味

これは**型ヒント付きの変数宣言**です。2つの部分に分けて説明します。

---

### 1. `file = None`

単純に「`file` という変数を `None` で初期化する」という意味です。

まだファイルを開いていない状態を表しています。

---

### 2. `: typing.IO` の部分

「この変数には `typing.IO` 型の値が入りますよ」という**型ヒント**です。

`typing.IO` は `open()` が返すファイルオブジェクトの型です。

```python
file = open("test.txt", "r")
# ↑ このfileの型が typing.IO
```

---

### なぜ `None` で初期化するの？

`try` の外で宣言しておかないと、エラーが起きたときに変数が未定義になってしまうからです。

```python
# ❌ 悪い例
try:
    file = open(filename, "r")
except OSError as e:
    print(e)

file.close()  # tryが失敗するとfileが存在しないのでクラッシュ！
```

```python
# ✅ 良い例
file: typing.IO = None  # 先にNoneで初期化

try:
    file = open(filename, "r")
except OSError as e:
    print(e)
    return  # ← returnで抜けるのでcloseは呼ばれない
```

ただし今回の解答例では `except` の中で `return` しているので、厳密には `None` 初期化がなくても動きます。**mypy（型チェッカー）を通すために書いている**という側面が強いです。

---

### まとめ

| 部分 | 意味 |
|---|---|
| `file` | 変数名 |
| `: typing.IO` | 型ヒント（ファイルオブジェクト型） |
| `= None` | とりあえずNullで初期化 |

## `"r"` の意味

`open()` の第2引数に渡す**ファイルを開くモード**です。

```python
file = open(filename, "r")
#                     ↑ これ
```

---

### 主なモード一覧

| モード | 意味 | 用途 |
|---|---|---|
| `"r"` | read（読み取り） | ファイルを読むとき |
| `"w"` | write（書き込み） | ファイルを新規作成・上書きするとき |
| `"a"` | append（追記） | ファイルの末尾に追加するとき |

---

### `"r"` の特徴

```python
# ✅ 読み取りのみOK
file = open("test.txt", "r")
content = file.read()

# ❌ 書き込みはエラーになる
file.write("hello")  # エラー！
```

また、**ファイルが存在しない場合はエラーになります**（`"w"` は存在しなくても新規作成します）。

---

### ちなみに省略もできる

```python
file = open(filename)      # "r" を省略
file = open(filename, "r") # 上と同じ意味
```

`"r"` はデフォルト値なので省略可能ですが、**明示的に書いた方が読みやすい**のでおすすめです。

# 演習1「アーカイブの作成」の解き方

## 演習0との違い

演習1は**演習0のコードを拡張**します。追加する機能は3つです。

1. 各行の末尾に `#` を追加
2. 変換後の内容を表示
3. ユーザーにファイル名を入力させて保存

---

## 追加ステップの解説

### ステップ1：各行の末尾に `#` を追加

```python
# 読み込んだcontentを行ごとに分割して#を追加
lines: list = content.splitlines()
new_lines: list = []

for line in lines:
    new_lines.append(line + "#")

new_content: str = "\n".join(new_lines) + "\n"
```

`splitlines()` で改行ごとにリスト化し、各行に `#` を追加してから `"\n".join()` で再結合します。

---

### ステップ2：変換後の内容を表示

```python
print("Transform data:")
print("---")
print(new_content, end="")
print("---")
```

---

### ステップ3：ファイル名を入力させて保存

```python
save_filename: str = input("Enter new file name (or empty): ")

if save_filename == "":
    print("Not saving data.")
else:
    print(f"Saving data to '{save_filename}'")
    
    save_file: typing.IO = None
    try:
        save_file = open(save_filename, "w")  # "w"で新規作成・上書き
    except OSError as e:
        print(f"Error opening file '{save_filename}': {e}")
        return

    save_file.write(new_content)
    save_file.close()
    print(f"Data saved in file '{save_filename}'.")
```

---

## 完成イメージ

```python
import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    file: typing.IO = None

    try:
        file = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    content: str = file.read()
    print("---")
    print(content, end="")
    print("---")
    file.close()
    print(f"File '{filename}' closed.")

    # ここから演習1の追加部分
    lines: list = content.splitlines()
    new_content: str = "\n".join([line + "#" for line in lines]) + "\n"

    print("Transform data:")
    print("---")
    print(new_content, end="")
    print("---")

    save_filename: str = input("Enter new file name (or empty): ")

    if save_filename == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{save_filename}'")

    save_file: typing.IO = None

    try:
        save_file = open(save_filename, "w")
    except OSError as e:
        print(f"Error opening file '{save_filename}': {e}")
        return

    save_file.write(new_content)
    save_file.close()
    print(f"Data saved in file '{save_filename}'.")


main()
```

---

## 演習0からの変更点まとめ

| 項目 | 演習0 | 演習1 |
|---|---|---|
| ヘッダー | `Recovery` | `Recovery & Preservation` |
| 読み込み | そのまま表示 | `#`を追加して表示 |
| 保存 | なし | ユーザー入力で保存 |
| `open()`モード | `"r"` のみ | `"r"` と `"w"` |

---

## チェックリスト

- [ ] 各行の末尾に `#` が追加されている
- [ ] 変換後の内容が `---` で囲まれて表示される
- [ ] 空のまま入力 → `Not saving data.` と表示
- [ ] ファイル名を入力 → ファイルが保存される
- [ ] 保存時のエラー（権限なしなど）も処理されている
- [ ] `"w"` モードで既存ファイルを上書きできる