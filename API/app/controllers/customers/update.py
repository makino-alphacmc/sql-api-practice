"""customers更新(PUT/PATCH)のcontroller。

対象テーブル: customers（主キー: customer_id）
主なカラム: customer_name, email, prefecture, registered_at, phone_numbers(配列), profile(JSONB: rank, age_group, interests, notification{email,sms})

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/customers/update.py に用意する
   （PUTなら全項目必須、PATCHなら全項目Optionalにするなど方針を決める）
2. パスパラメータで対象のcustomer_idを受け取る
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/customers/update.py の更新用関数を呼び出す
5. 戻り値がNone（対象が存在しない）だった場合はHTTPExceptionで404を返す
6. 更新後のレコードをレスポンスとして返す
"""
from fastapi import APIRouter, Depends, HTTPException

from app.db.connection import get_db
from app.services.customers import update as customers_update_service

router = APIRouter()
