"""order_items削除(DELETE)のcontroller。

対象テーブル: order_items（主キー: order_item_id）

ここで必要な処理:
1. パスパラメータで対象のorder_item_idを受け取る関数を定義する
2. Depends(get_db)でDBカーソルを受け取る
3. app/services/order_items/delete.py の削除用関数を呼び出す
4. 削除できなかった場合（対象が存在しない）はHTTPExceptionで404を返す
5. 削除できた場合はステータスコード204（レスポンスボディなし）を返す
6. このテーブルが他テーブルから参照されている場合、FK制約によって削除がエラーになることがある点に注意する
"""
from fastapi import APIRouter, Depends, HTTPException, Response

from app.db.connection import get_db
from app.services.order_items import delete as order_items_delete_service

router = APIRouter()
