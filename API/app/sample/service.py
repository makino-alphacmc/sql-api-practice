"""sampleリソース（sample_itemsテーブル）のservice層。

controller / service / model の「基本形」を1ファイルずつで示すための参考実装。
業務ロジック + DB操作をservice層にまとめる、というAPI_EXAM.md 0.2の規約通りの書き方。
値の埋め込みは必ず%sプレースホルダを使う（文字列結合でSQLを組み立てない）。
"""
from typing import Optional


def list_sample_items(cur, is_active: Optional[bool] = None):
    if is_active is not None:
        cur.execute(
            "SELECT item_id, name, price, is_active FROM sample_items "
            "WHERE is_active = %s ORDER BY item_id",
            (is_active,),
        )
    else:
        cur.execute(
            "SELECT item_id, name, price, is_active FROM sample_items ORDER BY item_id"
        )
    return cur.fetchall()


def get_sample_item_by_id(cur, item_id: int):
    cur.execute(
        "SELECT item_id, name, price, is_active FROM sample_items WHERE item_id = %s",
        (item_id,),
    )
    return cur.fetchone()


def create_sample_item(cur, body):
    cur.execute(
        """
        INSERT INTO sample_items (name, price, is_active)
        VALUES (%s, %s, %s)
        RETURNING item_id, name, price, is_active
        """,
        (body.name, body.price, body.is_active),
    )
    return cur.fetchone()


def update_sample_item(cur, item_id: int, body):
    current = get_sample_item_by_id(cur, item_id)
    if current is None:
        return None

    # PATCH的な部分更新: Noneのフィールドは現在値のまま維持する
    name = body.name if body.name is not None else current["name"]
    price = body.price if body.price is not None else current["price"]
    is_active = body.is_active if body.is_active is not None else current["is_active"]

    cur.execute(
        """
        UPDATE sample_items
        SET name = %s, price = %s, is_active = %s
        WHERE item_id = %s
        RETURNING item_id, name, price, is_active
        """,
        (name, price, is_active, item_id),
    )
    return cur.fetchone()


def delete_sample_item(cur, item_id: int) -> bool:
    cur.execute("DELETE FROM sample_items WHERE item_id = %s", (item_id,))
    return cur.rowcount > 0
