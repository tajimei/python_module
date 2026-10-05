## 1. グローバルに `pip install` すると何が困るのか

**プロジェクト間でバージョンが衝突する。** グローバルの `site-packages` は1つしかないので、同じパッケージは1つのバージョンしか入れられません。たとえばプロジェクトAが `pandas 1.5`、プロジェクトBが `pandas 2.1` を必要とする場合、Bのために更新するとAが壊れます。venv ならプロジェクトごとに別の `site-packages` を持てるので、両方を共存させられます。

**システムやほかのツールを壊す危険がある。** OS や他のアプリが、グローバルの Python やそのパッケージに依存していることがあります。そこで勝手にパッケージを上書き・削除すると、関係ないツールが動かなくなることがあります。最近の Homebrew や Linux の Python では、これを防ぐために、グローバルへの `pip install` 自体がエラー(`externally-managed-environment`)になるようになっています。

**再現性がなくなる。** グローバルにはいろいろなプロジェクトのパッケージが混ざって溜まっていきます。すると「自分のPCでは動くのに、他人のPCでは動かない」が起きやすくなります。どのパッケージが本当に必要なのか分からなくなるからです。venv で必要なものだけを入れ、`requirements.txt` に書き出しておけば、誰でも同じ環境を作り直せます。ex1 の内容はまさにこの話です。

**後片付けが難しい。** venv なら、いらなくなったらフォルダごと消せば終わりです。グローバルに入れたものは、どれを消してよいか判断しにくくなります。

## 2. `activate` は実際に何をしているのか

`source matrix_env/bin/activate` は、今のシェルの設定を書き換えるだけのシェルスクリプトです。主にやっていることは次のとおりです。

- **`PATH` の先頭に `matrix_env/bin` を追加する。** これが本質です。シェルはコマンドを `PATH` の前から順に探すので、`python3` や `pip` と打つと venv 側のものが最初に見つかるようになります。
- **環境変数 `VIRTUAL_ENV` に venv のパスを設定する。**
- **プロンプトに `(matrix_env)` を表示する。** 今どの環境にいるかを分かりやすくするためです。
- **`deactivate` 関数を定義する。** 実行すると、上の変更を元に戻します。

`source` で実行するのは、今のシェル自体の `PATH` を書き換える必要があるからです。普通に `./activate` と実行すると、別のプロセスで書き換わるだけで、今のシェルには影響しません。

`activate` は「便利のための近道」にすぎません。`matrix_env/bin/python3 construct.py` のように venv 内の python を直接指定すれば、`activate` しなくても venv として動きます。実際の隔離は、python 自身が起動時に `pyvenv.cfg` を見つけることで実現されています。

`which python3` を `activate` の前後で実行すると、指している場所が変わるのを確認できます。

## 3. 自分のプログラムは venv をどうやって検出しているのか

`sys.prefix != sys.base_prefix` で判定しています。

- **`sys.prefix`** は、今動いている Python 環境のルートです。venv 内なら `matrix_env` のパスになります。
- **`sys.base_prefix`** は、元になったグローバルな Python のインストール先です。

venv の python は起動時に `pyvenv.cfg` を見つけると、`sys.prefix` を venv のフォルダに設定します。一方、`sys.base_prefix` は元の Python の場所のままです。グローバル環境ではこの2つが同じ値になり、venv 内では異なる値になるので、比較すれば判定できます。

**`VIRTUAL_ENV` を使わなかった理由**も聞かれたら答えられるようにしておきましょう。`VIRTUAL_ENV` は `activate` したときにしか設定されません。そのため、`matrix_env/bin/python3 construct.py` と直接実行すると、venv 内なのに空になり、誤判定します。`sys.prefix` を使う方法なら、Python 自身が知っている情報で判定するので、どちらの起動方法でも正しく動きます。

表示している値の取り方もあわせて説明できると完璧です。

- **環境名**は `os.path.basename(sys.prefix)` で、パスの最後の部分を取り出しています。
- **実行中の Python** は `sys.executable` です。
- **パッケージ置き場**は `site.getsitepackages()` です。

ピアレビューで説明を求められそうな点を、質問と答えの形でまとめます。

## pip と Poetry について

**Q. pip と Poetry の違いは?**
pip はパッケージをインストールするだけのツールです。仮想環境は自分で `python -m venv` で作って `activate` し、依存関係は `requirements.txt` に書いて管理します。
Poetry は、仮想環境の作成、依存関係の管理、バージョンの固定までをまとめて面倒を見るツールです。`poetry install` だけで専用の venv が作られ、パッケージがそこに入ります。

**Q. `requirements.txt` と `pyproject.toml` の違いは?**
`requirements.txt` は、インストールするパッケージ名を並べただけのリストです。
`pyproject.toml` は、プロジェクトの名前・バージョン・対応する Python のバージョン・依存関係などを1つにまとめた設定ファイルです。Poetry 専用ではなく、Python 公式の標準形式です。

**Q. `poetry.lock` は何のためにある?**
実際にインストールされた正確なバージョンを、依存の依存(pandas が内部で使うパッケージなど)まで含めてすべて記録するファイルです。これを共有すれば、誰がいつ `poetry install` しても完全に同じ環境になります。`requirements.txt` で `pandas>=2.0` と書いた場合、インストールする日によって入るバージョンが変わりえます。この違いが「再現性」の差です。

**Q. pip で同じように固定する方法は?**
`pip freeze > requirements.txt` で、今の環境に入っている全パッケージを `pandas==3.0.6` のような完全固定の形で書き出せます。ただし、自分が直接使うものと、それが内部で使うものの区別がつかなくなります。Poetry は `pyproject.toml`(直接の依存)と `poetry.lock`(全部の固定)を分けて管理できるのが利点です。

**Q. `poetry run python loading.py` の `poetry run` は何をしている?**
Poetry が作った venv の Python でコマンドを実行しています。`activate` しなくても、その venv の中で動かせます。ex0 で学んだ「venv の python を直接指定すれば venv として動く」と同じ仕組みです。

**Q. Poetry の venv はどこにある?**
デフォルトでは Mac なら `~/Library/Caches/pypoetry/virtualenvs/` の下に作られます。`poetry env info` で確認できます。プログラムの出力の `Prefix:` の行にもこのパスが表示されます。

**Q. `package-mode = false` は何?**
このプロジェクトは配布するライブラリではなく、ただのスクリプトだと Poetry に伝える設定です。これがないと、Poetry は自分のコードをパッケージとしてインストールしようとして、エラーになることがあります。

## プログラムの仕組みについて

**Q. 依存関係が足りないとき、どうやって落ちずに済ませている?**
ファイルの先頭で `import pandas` を書いていないからです。先頭に書くと、プログラムが始まった瞬間に `ImportError` で落ちてしまいます。代わりに次の順番で処理しています。

1. `importlib.metadata.version()` で、インストールされているかとバージョンを調べる。
2. 足りないものがあれば、インストール方法を表示して `sys.exit(1)` で終了する。
3. 全部揃っていたら、`importlib.import_module()` で読み込む。

**Q. `sys.exit(1)` の `1` は何?**
終了コードです。`0` が成功、0以外が失敗を意味します。依存関係が足りずに終わったときは「失敗」として外部に伝えるために `1` を返しています。`echo $?` で直前のコマンドの終了コードを確認できます。

**Q. flake8 や mypy の import エラーが出ないのはなぜ?**
静的な `import pandas` 文がなく、すべて `importlib.import_module()` で動的に読み込んでいるからです。サブジェクトの「エラーを回避する仕組みもある」というヒントへの答えがこれです。代わりに型は `Any` や `ModuleType` になるので、mypy による型チェックが効きにくくなるというトレードオフがあります。

**Q. バージョン比較の関数はどれ?**
`check_dependencies()` です。必要なパッケージごとに `get_version()` を呼んで、`[OK] pandas (3.0.6)` のように表示しています。pip 環境と Poetry 環境で実行して出力を並べれば、それぞれにどのバージョンが入ったかを比較できます。

**Q. データはどうやって作っている? なぜ `range()` ではダメ?**
`numpy.random.default_rng(42)` で乱数生成器を作り、正規分布の乱数を1000個生成しています。サブジェクトが numpy をデータの生成元にすることを求めているのは、numpy を本当に使っていること(依存関係として必要なこと)を示すためです。`42` はシード値で、毎回同じ乱数が出るので結果を再現できます。

**Q. `matplotlib.use("Agg")` は何?**
画面に表示せず、画像ファイルに描画するだけのモード(バックエンド)に切り替えています。画面のない環境でも動き、ウィンドウが開いて処理が止まることもありません。pyplot を読み込む前に呼ぶ必要があります。

## テストの仕方

レビューでは、実際に3パターンを見せられるようにしておきましょう。

```bash
# 1. 依存関係なし(空の venv で試す)
python3 -m venv empty_env
source empty_env/bin/activate
python3 loading.py      # MISSING と案内が出る
deactivate

# 2. pip
python3 -m venv matrix_env
source matrix_env/bin/activate
pip install -r requirements.txt
python3 loading.py      # PNG が生成される
deactivate

# 3. Poetry
poetry install
poetry run python loading.py
```

## 提出前のチェック

- 提出ファイルは `loading.py`、`requirements.txt`、`pyproject.toml` の3つです。
- `matrix_env/` などの venv や、生成された `matrix_analysis.png` はリポジトリに含めないようにしましょう。`.gitignore` に書いておくのがおすすめです。
- `poetry.lock` は提出指定にはありませんが、入れるかどうかを自分で決めて、その理由を説明できるようにしておきましょう。

Q. なぜ .env を .gitignore に入れる必要があるの?
.env には本物のパスワードや API キーが入るからです。一度 Git にコミットすると、あとでファイルを消しても履歴に残り続け、リポジトリを見られる人なら誰でも取り出せます。公開リポジトリなら、秘密情報を自動で探し回るボットにすぐ見つかって悪用されます。そのため、構造だけを伝える .env.example をリポジトリに入れ、本物の値は各自の手元の .env に置きます。

Q. なぜコードに直接書かないの?
秘密がコードと一緒に共有されてしまうからです。それに加えて、環境ごとに値を変えるたびにコードを書き換える必要が出てしまうからです。環境変数にすれば、同じコードのまま、開発と本番で違う設定を渡せます。