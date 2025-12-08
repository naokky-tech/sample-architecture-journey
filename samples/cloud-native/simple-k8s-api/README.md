# simple-k8s-api

Kubernetes 上で動作する最小の API サンプルです。  
Python + FastAPI を Docker でコンテナ化し、Deployment / Service で公開します。

---

## 📂 フォルダ構成

```
samples/cloud-native/simple-k8s-api/  
 ├ README.md  
 ├ requirements.txt  
 ├ Dockerfile  
 ├ k8s/  
 │   ├ deployment.yaml  
 │   └ service.yaml  
 └ src/  
     └ app/  
         ├ __init__.py  
         └ main.py  
```

---

## ▶️ 1. ローカルで API 動作確認

cd samples/cloud-native/simple-k8s-api  
pip install -r requirements.txt  
uvicorn app.main:app --reload --port 8000 --app-dir src  

アクセス:  
- http://127.0.0.1:8000/health  
- http://127.0.0.1:8000/hello?name=k8s  

---

## ▶️ 2. Docker イメージビルド

docker build -t k8s-hello-api:latest .

---

## ▶️ 3. kind（ローカル Kubernetes）へのデプロイ例

### クラスタ作成
kind create cluster --name cn-sample

### イメージ取り込み
kind load docker-image k8s-hello-api:latest --name cn-sample

### マニフェスト適用
kubectl apply -f k8s/deployment.yaml  
kubectl apply -f k8s/service.yaml  

---

## ▶️ 4. port-forward でアクセス

kubectl port-forward service/k8s-hello-api 8080:80

アクセス:  
http://127.0.0.1:8080/hello?name=cluster  

---

## Kubernetes の学びどころ

- Deployment により Pod 数（replicas=2）が維持される（Self-healing）  
- Pod を消しても自動復旧  
- Service が負荷分散  
- readiness / liveness probe によるヘルス監視  

---

クラウドネイティブの基本である  
「宣言的運用」「自動復旧」「小さなコンテナの組み合わせ」を体験できます。