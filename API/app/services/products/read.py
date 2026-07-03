"""products取得のservice層。

ここで必要な処理:

[一覧取得]
1. 絞り込み条件（引数）を受け取り、指定があればWHERE句に反映してSELECT文を組み立てる
2. 条件がなければ全件を取得するSELECT文にする
3. cur.execute()の後、cur.fetchall()で全行を取得して返す

[単体取得]
1. 主キー（product_id）を条件にSELECT文を組み立てる（%sプレースホルダを使う）
2. cur.execute()の後、cur.fetchone()で1行取得して返す
   （見つからなければNoneが返る。404の判定はcontroller側の仕事）
"""


def list_products(cur, *args, **kwargs):
    ...


def get_product_by_id(cur, product_id: int):
    ...
