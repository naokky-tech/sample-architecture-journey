# Layered Architecture Sample (Python)

この記事「フクロウと学ぶアーキテクチャ #1 ─ レイヤードアーキテクチャ入門」で紹介している、
シンプルなレイヤードアーキテクチャの Python サンプルコードです。

構成は以下の 4 レイヤーです。

- Presentation Layer（UI / Controller）
- Application Layer（ユースケース・アプリの振る舞い）
- Domain Layer（ビジネスロジック・エンティティ）
- Infrastructure Layer（Repository / DB）

## 動かし方

```bash
git clone <このリポジトリ>
cd <このリポジトリ>

# （特別なライブラリは使っていないので仮想環境だけ任意で）
cd samples/layered/simple-cli
python src/main.py