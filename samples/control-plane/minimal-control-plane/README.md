# 最小の制御プレーン（Python サンプル）

「フクロウと学ぶアーキテクチャ #6-3  
制御プレーン & エージェント時代（実践編・完結）」で紹介している

**エージェント → 制御プレーン → ツール**

の **最小モデル** を Python で体験するためのサンプルです。

アプリケーション本体の外側に

- **行動（Action）を許可するかどうかを判定するレイヤー（制御プレーン）**

を 1 枚挟むことで、エージェントの行動を安全に統制する構造を体験できます。

---

## 📁 フォルダ構成

```
minimal-control-plane/
  README.md
  src/
    main.py
    control_plane/
      __init__.py
      policies.py       # ポリシー（誰がどの行動を許可されるか）
      control_plane.py  # 制御プレーン本体（authorize を提供）
      tools.py          # エージェントが呼び出すツール群
      agents.py         # エージェント（AI の代わりに振る舞うクラス）
```

---

## 🧪 動作環境

- Python **3.10 以上**  
- 外部ライブラリは **不要（標準ライブラリのみ）**
- LLMも不要

---

## ▶️ 実行方法

### 1. カレントディレクトリを移動

```
cd samples/control-plane/minimal-control-plane
```

### 2. サンプルを実行

```
python src/main.py
```

---

## 📝 実行すると何が起こる？

- `agent-A` は **read_data のみ許可**
- `agent-B` は **read_data / write_data が許可**

そのため、以下のように動きます：

- `agent-A.act("read_data")` → **成功**  
- `agent-A.act("write_data")` → **PermissionError（拒否）**  
- `agent-B.act("write_data")` → **成功**

---

## 🎯 このサンプルで体験できること

この最小サンプルでは、制御プレーンの本質である次を体験できます。

### ✔ Identity  
`Agent.id` によるエージェントの存在証明

### ✔ Action-level Authorization  
`ControlPlane.authorize(agent_id, action)` による行動単位の許可判定

### ✔ Tool Invocation  
許可された場合のみ  
`tool.read_data()` / `tool.write_data()` を実行

### ✔ Deny-by-default（原則拒否）  
許可されない行動は **必ず PermissionError**

---

## 🔍 現実の制御プレーンでは何が追加される？

実際の Microsoft / Google / OpenAI / AWS の制御プレーンでは、ここに多層の機能が追加されます。

- OIDC / OAuth2.1 / DPoP による ID 証明  
- OAuth2 RAR / Resource Indicators による **行動ベースの権限制御**  
- MCP / FastMCP / Secured Gateway による **安全なツール呼び出し**  
- OTel / Kill Switch / DLP による **行動監査と緊急停止**  
- PDP（OPA / Cerbos）による **外部ポリシー判断**

このサンプルは **それらの“芯の部分”だけを切り出したミニマム構造** です。

---

## 🚀 発展アイデア（必要なら一緒に開発できます）

- ポリシーを JSON / YAML ファイルから読み込む  
- RAR 風に「Action + Resource + Condition」に拡張  
- PDP として **OPA / Cerbos** を subprocess 経由で呼ぶ  
- 複数ツールを追加し、エージェントごとに許可範囲を変える  
- 行動ログ（Observability）を追加する  
