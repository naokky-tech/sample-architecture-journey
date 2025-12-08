"""
simple-k8s-api/src/app/main.py
FastAPI による最小の Kubernetes 向け API。
"""

from fastapi import FastAPI

app = FastAPI(title="Cloud Native Hello API")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "world") -> dict:
    return {"message": f"Hello, {name}!"}