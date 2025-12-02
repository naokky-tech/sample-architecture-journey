# adapters パッケージには「外側の世界」と接続するための実装を置きます。
#
# 例：
# - CLI / Web / GUI などの UI
# - In-memory / ファイル / DB などの永続化
#
# ここからは core（ドメイン）を import して OK ですが、
# core 側から adapters を import してはいけません。