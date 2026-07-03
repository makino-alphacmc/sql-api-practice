"""order_items作成のservice層。

ここで必要な処理:
1. 受け取ったリクエストボディの値を使ってINSERT文を組み立てる
2. 値の埋め込みには必ず %s プレースホルダを使う（文字列結合でSQLを組み立てない。SQLインジェクション対策）
3. RETURNING句を使うと、INSERT直後に生成された行（自動採番されたIDなど）をそのまま取得できる
4. 取得した行を返す
"""


def create_order_item(cur, body):
    ...
