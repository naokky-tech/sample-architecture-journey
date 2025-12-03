# 🦉 フクロウと学ぶアーキテクチャ #3  
## 分散・サービス分割（Microservices / SOA） ─ Python標準ライブラリでつくる最小HTTPサンプル

本リポジトリは、Zenn 記事  
**「フクロウと学ぶアーキテクチャ #3 ─ 分散・サービス分割（Microservices / SOA）」**  
で紹介している「最小構成のマイクロサービス」を **Python 標準ライブラリのみ** で再現したサンプルです。

フレームワーク（FastAPI など）は使用せず、  

- `http.server`  
- `urllib.request`  
- `json`

の3つを中心に、「サービスを分ける」という感覚を **最小限のコードで体験できる** ことを目的としています。

---

# 📁 フォルダ構成

```
samples/microservices/simple-http/
  README.md
  src/
    http_utils.py
    gateway.py
    user_service.py
    task_service.py
    notification_service.py
```

4つのサービスが **別プロセス・別ポート** で動作します。

| サービス名 | 役割 | ポート |
|-----------|------|--------|
| gateway | API Gateway（入口。認証は省略） | 8000 |
| user-service | ユーザ管理 | 8001 |
| task-service | タスク管理（作成時に通知連携） | 8002 |
| notification-service | 通知メッセージ蓄積 | 8003 |

---

# 🚀 セットアップ

外部ライブラリ不要（標準ライブラリのみ）。  
Python 3.10+ を推奨。

```
cd samples/microservices/simple-http
```

---

# ▶️ サービスの起動方法

各サービスは **別ターミナル** で起動します。  
すべて `src/` ディレクトリで実行してください。

## 1. notification-service（port=8003）

```
cd samples/microservices/simple-http/src
python notification_service.py
```

## 2. task-service（port=8002）

```
cd samples/microservices/simple-http/src
python task_service.py
```

## 3. user-service（port=8001）

```
cd samples/microservices/simple-http/src
python user_service.py
```

## 4. gateway（port=8000）

```
cd samples/microservices/simple-http/src
python gateway.py
```

---

# 📡 エンドポイント一覧

## user-service（http://localhost:8001）

### POST /users  
ユーザ作成  
例:  
```json
{"name": "Alice"}
```

### GET /users  
ユーザ一覧

### GET /users/{id}  
単一ユーザ取得

---

## task-service（http://localhost:8002）

### POST /tasks  
タスク作成  
作成時に通知サービスへ HTTP 連携  
```json
{"title": "買い物リストを整理する", "user_id": 1}
```

### GET /tasks  
タスク一覧

---

## notification-service（http://localhost:8003）

### POST /notifications  
通知を追加

### GET /notifications  
通知一覧

---

## gateway（http://localhost:8000）

### POST /tasks  
1. user-service にユーザ存在確認  
2. OKなら task-service にタスク作成依頼  
3. 結果をそのまま返却

### GET /tasks  
task-service の一覧をプロキシして返す

---

# 🧪 動作確認例

### 1. ユーザ作成（user-serviceへ直接）

```
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

---

### 2. Gateway 経由でタスク作成

```
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "買い物リストを整理する", "user_id": 1}'
```

---

### 3. 通知一覧

```
curl http://localhost:8003/notifications
```

---

# 🎯 このサンプルのねらい

- **Bounded Context = サービス** として分割する感覚をつかむ  
- 各サービスは **自分の状態（インメモリDB）** を内側に持つ  
- サービス間連携は **HTTP 越しに疎結合に行う**  
- Gateway を「ひとつの入口」として置く  
- ネットワークの失敗や“部分障害”などの特性が見えてくる

本番環境のような堅牢性（認証・リトライ・Circuit Breakerなど）は扱わず、  
**microserviceの最小イメージをつかむこと** を目標にしています。