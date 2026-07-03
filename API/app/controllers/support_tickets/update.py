"""support_tickets更新(PUT/PATCH)のcontroller。

対象テーブル: support_tickets（主キー: ticket_id）
主なカラム: customer_id(FK), order_id(FK, nullable), created_at, status, labels(配列), messages(JSONB配列)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/support_tickets/update.py に用意する
   （PUTなら全項目必須、PATCHなら全項目Optionalにするなど方針を決める）
2. パスパラメータで対象のticket_idを受け取る
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/support_tickets/update.py の更新用関数を呼び出す
5. 戻り値がNone（対象が存在しない）だった場合はHTTPExceptionで404を返す
6. 更新後のレコードをレスポンスとして返す
"""
from fastapi import APIRouter, Depends, HTTPException

from app.db.connection import get_db
from app.services.support_tickets import update as support_tickets_update_service

router = APIRouter()
