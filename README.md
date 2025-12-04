# 🦉 フクロウと学ぶアーキテクチャ ─ サンプルコード集

このリポジトリは、Zenn 連載 **「フクロウと学ぶアーキテクチャ」** シリーズで紹介する  
各アーキテクチャを *実際に動くコードで体験できる* ようにまとめたサンプル集です。

AI エージェント時代の複雑な設計に進む前に、  
**「書いて動かして理解する」** を重視して構成しています。

---

## 🎯 目的

- 各アーキテクチャの *責務の分け方* をコードで理解できるようにする  
- シンプルで壊れにくい最小構成を提示する  
- 記事と GitHub の対応を明確にして、学習導線を迷わせない  
- 後から別のアーキテクチャを追加しても破綻しない構造にする  

---

## 🗃️ ディレクトリ構成

アーキテクチャごとに `samples/` 以下へ格納し、  
各フォルダは **「サンプルプロジェクト単位で完結」** する構造になっています。

```text
samples/
  layered/                # Layered / N-Tier（第1回）
    simple-cli/           # CLIで動く最小構成
      README.md
      src/
        main.py
        presentation/
        application/
        domain/
        infrastructure/

  domain-centric/         # Clean / Hexagonal / DDD（第2回）
    simple-cli/

  microservices/          # Microservices / SOA（第3回）
    simple-http/

  event-driven/           # EDA / CQRS / Event Sourcing（第4回）
    ...

  cloud-native/           # Serverless / Kubernetes（第5回予定）
    ...

  control-plane-agents/   # エージェント制御プレーン（第6回予定）
    ...
```

---

## 📚 対応する Zenn 連載記事

| 回 | アーキテクチャ | 記事 | サンプルコード |
|---|-----------------|------|----------------|
| #1 | レイヤード（Layered / N-Tier） | *公開中* | `samples/layered/simple-cli` |
| #2 | ドメイン中心（Clean / Hexagonal / DDD） | *公開中* | `samples/domain-centric/...` |
| #3 | 分散（Microservices） | *公開中* | `samples/microservices/...` |
| #4 | イベント駆動（EDA / CQRS） | *公開予定* | `samples/event-driven/...` |
| #5 | クラウドネイティブ | *公開予定* | `samples/cloud-native/...` |
| #6 | エージェント制御プレーン | *公開予定* | `samples/control-plane-agents/...` |

各サンプルの説明は `samples/<arch>/<sample>/README.md` に記載しています。

---

## ▶️ 動かし方

すべてのサンプルは Python の標準ライブラリだけで動作するように設計されています。  
（必要に応じて各サンプルごとに `requirements.txt` を追加できます）

### 例：レイヤードの CLI サンプル

```bash
cd samples/layered/simple-cli
python src/main.py
```

実行すると、各レイヤーがどのように連携するのかを体験できます。

---

## 🦉 設計方針（学習者向けのガイドライン）

このリポジトリは単なるコード集ではなく、**アーキテクチャの学習用教材** として設計しています。  

### 1. 責務の境界を明確にする  
各レイヤーやモジュールが *何に責任を持つか* が分かる構造を徹底しています。

### 2. 依存方向のルールを守る  
アーキテクチャごとに「依存の流れ」が異なるため、  
そのポイントが明確に見えるようなファイル配置にしています。

### 3. コードは最小構成に寄せる  
過剰な抽象化や DI フレームワークは採用せず、  
初心者でも理解しやすい状態を保ちます。

### 4. 差し替え可能性を意識  
Infrastructure / Adapter / Repository などは  
バックエンドが変化しても置き換えやすい形をキープします。

---

## 📝 ライセンス

MIT License

---

## 🦉 制作者

- **naokky**  
  Zenn: https://zenn.dev/naokky  

学習の旅を、一緒に進めていきましょう 🚀