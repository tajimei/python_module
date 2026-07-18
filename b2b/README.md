*This project has been created as part of the 42 curriculum by mtajima.*

---

## Description（プロジェクト説明）

### プロジェクトの目的

Born2beRootは、仮想マシンを使ったサーバー構築を通じて、Linuxシステム管理の基礎を学ぶプロジェクトです。VirtualBoxを使用してDebianをインストールし、セキュリティポリシー・ユーザー管理・ファイアウォール・SSH設定など、実際のサーバー運用に必要な知識を習得します。

### 仮想マシンとは

仮想マシン（Virtual Machine / VM）とは、物理的なコンピュータ上でソフトウェアによって再現された「仮想のコンピュータ」です。1台の物理マシンの上で、複数の独立したOSを同時に動かすことができます。

**仮想マシンの利点：**
- 本番環境を壊さずに安全に設定を試せる
- 異なるOSを同一ハードウェアで動かせる
- スナップショットで状態を保存・復元できる
- 不要になれば簡単に削除できる

---

## OSの選択：DebianとRocky Linuxの比較

**Debianを選んだ理由：**
- システム管理初心者に推奨されている
- ドキュメントやコミュニティが充実しており、問題解決がしやすい
- パッケージの安定性が高く、サーバー用途に適している
- aptによるパッケージ管理が直感的で使いやすい

---

## 主要技術の比較

### aptとaptitudeの違い

| 項目 | apt | aptitude |
|------|-----|----------|
| 種類 | コマンドラインツール | コマンドライン＋対話型UIツール |
| 用途 | 日常的なパッケージ操作 | より高度な依存関係の解決 |
| 依存解決 | 基本的な解決 | より賢い依存関係の解決 |
| インターフェース | CLIのみ | CLIと対話型UI両方 |
| デフォルト | Debianに標準搭載 | 別途インストールが必要 |

**使い分けの例：**
- `apt install パッケージ名` → 通常のインストール
- `aptitude` → 依存関係の競合が発生したときに解決策を提示してくれる

### AppArmorとSELinuxの比較

| 項目 | AppArmor | SELinux |
|------|----------|---------|
| 採用OS | Debian / Ubuntu | Rocky / RHEL / Fedora |
| 設定方式 | プロファイルベース（パスで管理） | ラベルベース（全ファイルにラベル） |

**AppArmorとは：**
プログラムごとに「何のファイルにアクセスできるか」「何のネットワーク操作ができるか」を制限するセキュリティモジュール。プロファイルという設定ファイルでプログラムの権限を管理する。

起動確認コマンド：
```bash
systemctl status apparmor
aa-status
```

### UFWとfirewalldの比較

| 項目 | UFW | firewalld |
|------|-----|-----------|
| 採用OS | Debian / Ubuntu | Rocky / RHEL / Fedora |

**UFWとは：**
Uncomplicated Firewallの略で、iptablesを簡単に操作するためのフロントエンド。ポートの開閉を直感的なコマンドで管理できる。

### VirtualBoxとUTMの比較

| 項目 | VirtualBox | UTM |
|------|------------|-----|
| 対応OS | Windows / Mac / Linux | macOS専用 |
| 仮想化技術 | x86仮想化 | QEMU / Apple Hypervisor |
| ディスク形式 | .vdi | .qcow2 |

---

## 主な設計上の選択

### パーティション構成

LVM（Logical Volume Manager）を使用した暗号化パーティションを構築した。

```
lsblk での実際の構成：
sda                          12G   disk
├─sda1                       791M  part   /boot
├─sda2                       1K    part
└─sda5                       11.2G part
  └─sda5_crypt               11.2G crypt        ← LUKS暗号化レイヤー
    ├─mtajima42--vg-root     7.1G  lvm    /
    ├─mtajima42--vg-swap_1   620M  lvm    [SWAP]
    └─mtajima42--vg-home     3.4G  lvm    /home
```

- `/boot` は暗号化外（起動に必要なため）
- `sda5_crypt` がLUKSによる暗号化パーティションで、その中にLVMを構築
- `/` と `/home` を分離することで、課題要件の「最低2つの暗号化パーティション」を満たしている

**LVMとは：**
Logical Volume Managerの略で、物理ディスクを抽象化して柔軟にパーティションを管理する仕組み。後からサイズ変更が容易で、複数のディスクをまとめて管理できる。

**暗号化を使用した理由：**
ディスクを物理的に抜き取られた場合でもデータを保護するため。

### セキュリティポリシー

**パスワードポリシー（/etc/login.defs および /etc/pam.d/common-password）：**
- パスワードの有効期限：30日
- パスワード変更の最小間隔：2日
- 有効期限7日前に警告
- 最小文字数：10文字
- 大文字・小文字・数字を必須
- 同一文字の連続：3文字まで
- ユーザー名をパスワードに含めることを禁止
- 新パスワードは旧パスワードと7文字以上異なること

**sudo設定（/etc/sudoers.d/sudoconfig）：**
- パスワード誤入力は3回まで（`passwd_tries=3`）
- 誤入力時にカスタムメッセージを表示（`badpass_message`）
- 全操作を /var/log/sudo/sudo.log に記録（`logfile` / `log_input` / `log_output`）
- 入出力の詳細ログを /var/log/sudo/ に保存（`iolog_dir`）
- TTYモードを必須化（`requiretty`）
- 使用可能なパスを制限（`secure_path`）

### ユーザー管理

- rootユーザー：直接ログインを制限
- 一般ユーザー（mtajima）：`user42`グループと`sudo`グループに所属
- SSHからのrootログインを禁止

### インストールしたサービス

| サービス | 用途 |
|---------|------|
| openssh-server | SSHリモートアクセス（ポート4242） |
| ufw | ファイアウォール管理 |
| sudo | 権限昇格の管理 |
| libpam-pwquality | パスワードポリシーの強化 |

---

## Instructions（セットアップ手順）

### 必要環境
- VirtualBox（最新版）
- Debian 13 ISOファイル

### セットアップ手順

**1. VirtualBoxのインストール**
```bash
sudo apt install virtualbox -y
```

**2. Debian ISOのダウンロード**
```bash
wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-13.x.x-amd64-netinst.iso
```

**3. VMの作成**
- VirtualBoxで「New」をクリック
- OS：Linux / Debian (64-bit)
- メモリ：1024MB以上
- ディスク：12GB以上

**4. SSHの設定**
```bash
apt install -y openssh-server
nano /etc/ssh/sshd_config
# Port 4242 に変更
# PermitRootLogin no に変更
systemctl restart ssh
```

ホストからSSH接続するには、VirtualBoxのポートフォワーディング設定が必要：
- VMの Settings → Network → Advanced → Port Forwarding
- ルール追加：Host Port `4242` → Guest Port `4242`（TCP）

接続方法：
```bash
ssh mtajima@localhost -p 4242
```

**5. UFWの設定**
```bash
apt install -y ufw
ufw default deny incoming    # 受信をすべて拒否（デフォルト）
ufw default allow outgoing   # 送信をすべて許可（デフォルト）
ufw allow 4242               # SSH用に4242のみ開放
ufw enable
ufw status  # 確認
```

**6. パスワードポリシーの設定**
```bash
apt install -y libpam-pwquality
nano /etc/login.defs        # PASS_MAX_DAYS 30 / PASS_MIN_DAYS 2 / PASS_WARN_AGE 7
nano /etc/pam.d/common-password  # pam_pwquality.so の行に設定追加
```

`/etc/login.defs` の変更は**新規ユーザーにのみ**適用されるため、既存ユーザーには `chage` で個別に適用する必要がある：
```bash
chage -M 30 -m 2 -W 7 root
chage -M 30 -m 2 -W 7 mtajima
chage -l mtajima   # 適用確認
```

**7. sudoの設定**
```bash
apt install -y sudo
mkdir -p /var/log/sudo
nano /etc/sudoers.d/sudoconfig
```

**8. ユーザーとグループの作成**
```bash
useradd -m -s /bin/bash mtajima
passwd mtajima
groupadd user42
usermod -aG user42 mtajima
usermod -aG sudo mtajima
```

**9. ホスト名の設定**
```bash
hostnamectl set-hostname mtajima42
```

**10. monitoring.shのセットアップ**
```bash
nano /usr/local/bin/monitoring.sh
chmod +x /usr/local/bin/monitoring.sh
crontab -e
# */10 * * * * /usr/local/bin/monitoring.sh を追加
```

---

## monitoring.shの説明

サーバー起動時から10分ごとに、全端末にシステム情報を表示するbashスクリプト。

```bash
#!/bin/bash
ARC=$(uname -a)                    # OSアーキテクチャとカーネル情報
PCPU=$(grep -c "physical id" /proc/cpuinfo)   # 物理CPU数
VCPU=$(grep -c "processor" /proc/cpuinfo)      # 仮想CPU数
RAM_TOTAL=$(free -m | awk '/Mem:/{print $2}')  # 総メモリ(MB)
RAM_USED=$(free -m | awk '/Mem:/{print $3}')   # 使用中メモリ(MB)
RAM_PERC=$(free -m | awk '/Mem:/{printf "%.2f", $3/$2*100}')  # メモリ使用率
DISK_TOTAL=$(df -BG --total | grep total | awk '{print $2}')  # 総ストレージ
DISK_USED=$(df -BM --total | grep total | awk '{print $3}')   # 使用中ストレージ
DISK_PERC=$(df --total | grep total | awk '{printf "%d", $3/$2*100}')  # ストレージ使用率
CPU_LOAD=$(top -bn1 | grep "Cpu(s)" | awk '{printf "%.1f", $2+$4}')   # CPU使用率
LAST_BOOT=$(who -b | awk '{print $3" "$4}')    # 最終起動日時
LVM=$(lsblk | grep -q "lvm" && echo "yes" || echo "no")  # LVM使用有無
TCP=$(ss -tn | grep ESTAB | wc -l)             # TCP接続数
USER_LOG=$(users | wc -w)                       # ログイン中ユーザー数
IP=$(hostname -I | awk '{print $1}')            # IPアドレス
MAC=$(ip link | grep "ether" | awk '{print $2}') # MACアドレス
SUDO=$(grep -c COMMAND /var/log/sudo/sudo.log 2>/dev/null || echo 0)  # sudo実行数
```

**cron**
Linuxの定期実行スケジューラ。`crontab -e` で設定し、`*/10 * * * *` は「毎10分ごとに実行」を意味する。

**スクリプトを変更せずに停止する方法：**
```bash
crontab -e
# */10 * * * * の行をコメントアウト（#をつける）または削除する
```

---

## メモ

**仮想マシンの仕組み**
ハイパーバイザー（VirtualBoxなど）がホストOSのリソース（CPU・メモリ・ディスク）を仮想化し、ゲストOSに割り当てる。ゲストOSはハードウェアを直接操作しているように見えるが、実際はソフトウェアによる模擬環境で動作している。

**SSH**
Secure Shellの略で、ネットワーク越しに安全にサーバーを操作するためのプロトコル。通信が暗号化されているため、パスワードやコマンドが盗聴されない。

**LVM**
物理的なディスクを「物理ボリューム→ボリュームグループ→論理ボリューム」という3層構造で抽象化し、柔軟にパーティションを管理できる仕組み。後からサイズを変更したり、複数のディスクをまとめたりできる。

**UFW**
Uncomplicated Firewallの略。iptablesの複雑な設定を簡単なコマンドで操作できるようにしたツール。このプロジェクトではポート4242のみを開放し、不正アクセスを防いでいる。

## ssh接続

VMを起動してSSH接続（`ssh mtajima@localhost -p 4242` → `su -`）

---

### 【1】基本確認

```bash
# OSの確認
head -n 2 /etc/os-release

# グラフィカル環境がないこと
systemctl get-default
# → multi-user.target ならOK

# AppArmorの動作確認
systemctl status apparmor
aa-status
# → active / profiles loaded ならOK

# UFWの動作確認
ufw status
# → Status: active、4242 ALLOW ならOK

# SSHがポート4242のみで動作
ss -tunlp
# → 4242のみLISTENならOK

# ホスト名
hostname
# → mtajima42 ならOK

# パーティション表示（LVM・暗号化の確認）
lsblk
# → sda5_crypt と lvm が表示されればOK

# ユーザーのグループ確認
groups mtajima
# → sudo と user42 が含まれていればOK

# sudoログの確認
ls /var/log/sudo/
cat /var/log/sudo/sudo.log
```

---

### 【2】想定できる変更

**■ 新規ユーザー作成＋パスワード設定**
```bash
useradd -m -s /bin/bash testuser
passwd testuser
```

**■ 弱いパスワードが拒否されることの確認**
```bash
passwd testuser
```

**■ グループ作成＋割り当て**
```bash
groupadd evaluating
usermod -aG evaluating testuser
groups testuser
```

**■ ホスト名の変更＋再起動**
```bash
hostnamectl set-hostname reviewer42
reboot
# 再起動後
hostname
# → reviewer42 ならOK
# 元に戻す
hostnamectl set-hostname mtajima42
```

**■ UFWルールの追加と削除**
```bash
ufw allow 8080
ufw status
ufw delete allow 8080
ufw status
```

**■ SSHで新規ユーザー接続（ホスト側で）**
```bash
ssh testuser@localhost -p 4242
```

**■ rootでSSH接続できないことの確認（ホスト側で）**
```bash
ssh root@localhost -p 4242
```

**■ sudoの動作確認（mtajimaユーザーで）**
```bash
su - mtajima
sudo ls /root
# 正しいパスワード → 実行できる
sudo -k && sudo ls /root
# わざと間違ったパスワードを3回 → カスタムメッセージが表示され遮断される
```

**■ sudoログが更新されることの確認（rootで）**
```bash
cat /var/log/sudo/sudo.log
# 直前のsudoコマンドが記録されていればOK
```

**■ monitoring.shの動作**
```bash
bash /usr/local/bin/monitoring.sh
```

**■ cronを毎分実行に変更**
```bash
crontab -e
# */10 * * * * → * * * * * に変更
# 1分待ってwallが来ることを確認
# 確認後 */10 に戻す
```

**■ cronの停止（スクリプトを変更せずに）**
```bash
crontab -e
# 行頭に # をつけてコメントアウト
reboot
# 再起動後、10分待ってもwallが来ないことを確認
# 確認後、# を外して元に戻す
```

---

## Resources（参考資料）

### 公式ドキュメント
- [Debian公式ドキュメント](https://www.debian.org/doc/)
- [AppArmor公式ドキュメント](https://apparmor.net/)
- [UFW公式ガイド](https://help.ubuntu.com/community/UFW)
- [LVM管理ガイド](https://tldp.org/HOWTO/LVM-HOWTO/)
- [OpenSSH公式ドキュメント](https://www.openssh.com/manual.html)

### 参考記事・チュートリアル
- [Debian インストールガイド](https://www.debian.org/releases/stable/installmanual)
- [Linux パスワードポリシー設定](https://linux.die.net/man/8/pam_pwquality)
- [sudo設定リファレンス](https://linux.die.net/man/5/sudoers)
- [cron使い方ガイド](https://man7.org/linux/man-pages/man5/crontab.5.html)

### AIの使用について
- 使用したAI：Claude
- 用途： pdf翻訳 , 理解を深めるための壁打ち