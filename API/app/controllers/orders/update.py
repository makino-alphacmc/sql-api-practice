"""orders更新(PUT/PATCH)のcontroller。

対象テーブル: orders（主キー: order_id）
主なカラム: customer_id(FK), order_date, status, payment_method, coupon_codes(配列), delivery_address(JSONB), order_note(JSONB, nullable)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/orders/update.py に用意する
   （PUTなら全項目必須、PATCHなら全項目Optionalにするなど方針を決める）
2. パスパラメータで対象のorder_idを受け取る
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/orders/update.py の更新用関数を呼び出す
5. 戻り値がNone（対象が存在しない）だった場合はHTTPExceptionで404を返す
6. 更新後のレコードをレスポンスとして返す
"""
from fastapi import APIRouter, Depends, HTTPException

from app.db.connection import get_db
from app.services.orders import update as orders_update_service

router = APIRouter()
