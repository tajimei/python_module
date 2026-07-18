# The Codex — Mastering Python's Import Mysteries

Pythonのインポート機構を4つのパートに分けて体験的に学ぶプロジェクトです。

---

## 概要

このプロジェクトでは、Pythonの「4つの神聖な謎」を錬金術のメタファーを通じて学びます。

| パート | テーマ | 学ぶこと |
|--------|--------|----------|
| I. 蒸留器 (The Alembic) | インポートの基本形 | `import` と `from ... import` の違い、`__init__.py` の役割 |
| II. 蒸留 (Distillation) | ネストされたインポート | モジュール間の連携、パッケージエイリアス |
| III. 大変換 (The Great Transmutation) | 絶対 vs 相対インポート | `from alchemy.x import y` vs `from ..x import y` |
| IV. 爆発回避 (Avoid the Explosion) | 循環依存 | 循環インポートの原因と回避方法 |

---

## ディレクトリ構造

```
.
|-- alchemy/                          # メインパッケージ
|   |-- __init__.py                   # パッケージの窓口（公開APIを定義）
|   |-- elements.py                   # earth, air の生成関数
|   |-- potions.py                    # ポーション調合（他モジュールを組み合わせる）
|   |-- grimoire/                     # 呪文書サブパッケージ
|   |   |-- __init__.py
|   |   |-- light_spellbook.py        # 光の魔法（循環依存を回避）
|   |   |-- light_validator.py        # 光のバリデーター
|   |   |-- dark_spellbook.py         # 闇の魔法（循環依存で爆発）
|   |   '-- dark_validator.py         # 闇のバリデーター
|   '-- transmutation/                # 変換サブパッケージ
|       |-- __init__.py
|       '-- recipes.py                # 絶対・相対インポートの両方を使用
|-- elements.py                       # ルートレベルの要素（fire, water）
|-- ft_alembic_0.py ~ ft_alembic_5.py # パートI テストスクリプト（6本）
|-- ft_distillation_0.py ~ 1.py       # パートII テストスクリプト（2本）
|-- ft_transmutation_0.py ~ 2.py      # パートIII テストスクリプト（3本）
|-- ft_kaboom_0.py ~ 1.py             # パートIV テストスクリプト（2本）
'-- .gitignore
```

---

## 動作環境

- Python 3.10 以降
- flake8（コーディング規約チェック）
- mypy（型チェック）

---

## パートI: 蒸留器 (The Alembic)

### 目的

6種類のインポート方法を使い分け、それぞれの挙動を理解する。

### ファイル

**elements.py（ルート）** — `create_fire()` と `create_water()` を定義。

**alchemy/elements.py** — `create_earth()` と `create_air()` を定義。

**alchemy/\_\_init\_\_.py** — `create_air` のみを公開し、`create_earth` は意図的に非公開。

### テストスクリプトと使用するインポート形式

| スクリプト | インポート形式 | アクセス先 | 呼ぶ関数 |
|-----------|-------------|----------|---------|
| `ft_alembic_0.py` | `import elements` | ルートの elements.py | `create_fire()` |
| `ft_alembic_1.py` | `from elements import create_water` | ルートの elements.py | `create_water()` |
| `ft_alembic_2.py` | `import alchemy.elements` | alchemy/elements.py | `create_earth()` |
| `ft_alembic_3.py` | `from alchemy.elements import create_air` | alchemy/elements.py | `create_air()` |
| `ft_alembic_4.py` | `import alchemy` | \_\_init\_\_.py 経由 | `create_air()` ✅ / `create_earth()` ❌ |
| `ft_alembic_5.py` | `from alchemy import create_air` | \_\_init\_\_.py 経由 | `create_air()` |

### 学びのポイント

- `import X` はモジュールオブジェクトを取得し、`X.func()` でアクセスする
- `from X import func` は関数を直接取り出す
- `__init__.py` はパッケージの「窓口」として、外部に公開する名前を制御する
- `__init__.py` で公開していない名前（`create_earth`）にアクセスすると `AttributeError` になる
- ft_alembic_4.py の mypy エラーと実行時エラーは**意図的なもの**

### 実行例

```bash
$ python3 ft_alembic_0.py
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created

$ python3 ft_alembic_4.py
=== Alembic 4 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
AttributeError: module 'alchemy' has no attribute 'create_earth'.
```

---

## パートII: 蒸留 (Distillation)

### 目的

あるモジュールが別のモジュールの関数を呼び出す「ネストされたインポート」を理解する。

### ファイル

**alchemy/potions.py** — 4つの元素関数をインポートし、ポーションを調合する。

- `healing_potion()` → earth + air を組み合わせる
- `strength_potion()` → fire + water を組み合わせる

**alchemy/\_\_init\_\_.py の更新** — `heal = healing_potion` というエイリアスを追加。

### テストスクリプト

| スクリプト | インポート形式 | 内容 |
|-----------|-------------|------|
| `ft_distillation_0.py` | `from alchemy.potions import ...` | 直接アクセスで両ポーション調合 |
| `ft_distillation_1.py` | `import alchemy` | \_\_init\_\_.py 経由で `strength_potion` と `heal` エイリアス使用 |

### 学びのポイント

- モジュール内から別のモジュールをインポートするチェーン構造
- `alchemy/potions.py` は `alchemy/elements.py` と ルートの `elements.py` の両方を使う
- `__init__.py` でエイリアス（`heal = healing_potion`）を作ると、パッケージ利用者に便利なショートカットを提供できる

### 実行例

```bash
$ python3 ft_distillation_0.py
=== Distillation 0 ===
Direct access to alchemy/potions.py
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing healing_potion: Healing potion brewed with 'Earth element created' and 'Air element created'
```

---

## パートIII: 大変換 (The Great Transmutation)

### 目的

絶対インポートと相対インポートの違いを理解し、同じモジュール内で使い分ける。

### ファイル

**alchemy/transmutation/recipes.py** — 絶対インポートと相対インポートを**両方**使用。

```python
# 絶対インポート（フルパスで指定）
from alchemy.elements import create_air

# 相対インポート（.. で親パッケージを辿る）
from ..elements import create_air as _unused_air
```

### テストスクリプト

| スクリプト | インポート形式 | 内容 |
|-----------|-------------|------|
| `ft_transmutation_0.py` | `import alchemy.transmutation.recipes` | フルパスで直接アクセス |
| `ft_transmutation_1.py` | `import alchemy.transmutation` | transmutation モジュール経由 |
| `ft_transmutation_2.py` | `import alchemy` | alchemy モジュール経由 |

### 絶対インポート vs 相対インポート

| | 絶対インポート | 相対インポート |
|---|---|---|
| 書き方 | `from alchemy.elements import X` | `from ..elements import X` |
| メリット | 明確、どこから来たかすぐ分かる | 短い、パッケージ名変更に強い |
| デメリット | パッケージ名変更時に全修正が必要 | 深いネストだと `....` が読みにくい |
| 推奨場面 | 一般的にはこちらが推奨 | 同一パッケージ内の兄弟モジュール間 |

### 実行例

```bash
$ python3 ft_transmutation_0.py
=== Transmutation 0 ===
Using file alchemy/transmutation/recipes.py directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
```

---

## パートIV: 爆発回避 (Avoid the Explosion)

### 目的

循環依存（circular import）の原因を理解し、回避方法を学ぶ。

### 循環依存とは

モジュールAがモジュールBをインポートし、モジュールBがモジュールAをインポートすると、無限ループに陥り `ImportError` が発生する。

```
dark_spellbook.py → dark_validator.py → dark_spellbook.py → ...（無限ループ）
```

### 光の魔法（成功パターン）

**light_spellbook.py** は `light_spell_record()` の**関数内部**で遅延インポートを行う。

```python
def light_spell_record(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire.light_validator import validate_ingredients  # ← 関数内
    ...
```

モジュール読み込み時にはインポートが実行されないので、循環が起きない。

**light_validator.py** はモジュールトップレベルで `light_spellbook` をインポートするが、`light_spellbook` 側がトップレベルで `light_validator` をインポートしていないため問題なし。

### 闇の魔法（爆発パターン）

**dark_spellbook.py** と **dark_validator.py** が**モジュールのトップレベル**で互いをインポートする。

```python
# dark_spellbook.py（1行目）
from .dark_validator import validate_ingredients

# dark_validator.py（1行目）
from .dark_spellbook import dark_spell_allowed_ingredients
```

Python がどちらかを読み込もうとした瞬間に、もう一方が未完成のまま参照され `ImportError` になる。

### テストスクリプト

| スクリプト | 結果 | 説明 |
|-----------|------|------|
| `ft_kaboom_0.py` | ✅ 成功 | 光の呪文を記録。遅延インポートで循環回避 |
| `ft_kaboom_1.py` | ❌ ImportError | 闇の呪文を記録しようとして循環依存で爆発 |

### 循環依存の回避方法（複数あり）

1. **遅延インポート（このプロジェクトで採用）** — 関数内でインポートし、モジュール読み込み時のループを避ける
2. **モジュール統合** — 循環する2つのモジュールを1つにまとめる
3. **第3のモジュールに切り出す** — 共通部分を別モジュールに分離する
4. **設計の見直し** — 依存関係の方向を整理し、一方向にする

### 実行例

```bash
$ python3 ft_kaboom_0.py
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)

$ python3 ft_kaboom_1.py
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
ImportError: cannot import name 'dark_spell_allowed_ingredients'
from partially initialized module 'alchemy.grimoire.dark_spellbook'
(most likely due to a circular import)
```

---

## 制約事項

- Python 3.10 以降
- flake8 準拠
- mypy による型チェック（ft_alembic_4.py のエラーは意図的）
- `eval()` / `exec()` の使用禁止
- `sys.path` の変更禁止
- 外部ライブラリのインポート禁止（プロジェクト内ファイルのみ）

## チェックコマンド

```bash
# 全スクリプト実行
for f in ft_alembic_{0..5}.py ft_distillation_{0..1}.py ft_transmutation_{0..2}.py ft_kaboom_0.py; do
    echo "--- $f ---"
    python3 "$f"
    echo ""
done

# 爆発テスト（エラーが出るのが正解）
python3 ft_kaboom_1.py

# コーディング規約チェック
flake8

# 型チェック（ft_alembic_4.py の1件のエラーは意図的）
mypy .
```