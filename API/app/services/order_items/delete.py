"""order_items削除のservice層。

ここで必要な処理:
1. 主キー（order_item_id）を条件にDELETE文を組み立てる（%sプレースホルダを使う）
2. cur.execute()の後、cur.rowcount で削除された行数を確認できる（0件なら対象が存在しなかった）
3. 削除できたかどうかを表す値（真偽値など）を返す
4. このテーブルが他テーブルから参照されている場合、FK制約違反でエラーになることがある点に注意する
"""


def delete_order_item(cur, order_item_id: int):
    ...
