"""orders作成(POST)のcontroller。

対象テーブル: orders（主キー: order_id）
主なカラム: customer_id(FK), order_date, status, payment_method, coupon_codes(配列), delivery_address(JSONB), order_note(JSONB, nullable)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/orders/create.py に用意する
2. POSTメソッドのルーター関数を定義する（レスポンスの型・ステータスコード201を指定する）
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/orders/create.py の作成用関数を呼び出し、その戻り値をそのまま返す
5. 必須項目の不足や型違反はPydanticが自動で422にしてくれるので、ここで個別に処理しなくてよい
"""
from fastapi import APIRouter, Depends

from app.db.connection import get_db
from app.services.orders import create as orders_create_service

router = APIRouter()
