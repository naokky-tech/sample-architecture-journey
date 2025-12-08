# simple-serverless

Serverless アーキテクチャを最小構成で理解するためのサンプルです。

- 単一の関数 `handler()` がイベントを受けてレスポンスを返す  
- 実際のクラウドにデプロイする前に「イベント → 関数 → レスポンス」の流れを体験できます  

---

## 📂 フォルダ構成

```
samples/cloud-native/simple-serverless/  
 ├ README.md  
 ├ requirements.txt  
 ├ event.json  
 └ src/  
     ├ __init__.py  
     ├ handler.py  
     └ invoke_local.py  
```

---

## ▶️ ローカル実行（最短）

cd samples/cloud-native/simple-serverless  
pip install -r requirements.txt  
python src/invoke_local.py  

---

## 実行結果例

=== Input Event ===  
{ "name": "cloud-native traveler" }

=== Handler Result ===  
{ "message": "Hello, cloud-native traveler!" }

---

## Serverless ランタイムとの対応例

### AWS Lambda
- ハンドラー → src/handler.handler  
- トリガー → API Gateway / S3 / SQS 等

### Azure Functions
- main 関数を __init__.py に配置  
- function.json でトリガー定義  

---

## 補足
- event.json を編集することで任意の入力を試せます  
- ライブラリ依存なし（標準ライブラリのみ）  
- handler 内にビジネスロジックを追加すれば、そのままクラウドへ移行可能  

---