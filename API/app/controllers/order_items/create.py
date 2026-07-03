"""order_items作成(POST)のcontroller。

対象テーブル: order_items（主キー: order_item_id）
主なカラム: order_id(FK), product_id(FK), quantity, unit_price, item_options(JSONB, nullable)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/order_items/create.py に用意する
2. POSTメソッドのルーター関数を定義する（レスポンスの型・ステータスコード201を指定する）
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/order_items/create.py の作成用関数を呼び出し、その戻り値をそのまま返す
5. 必須項目の不足や型違反はPydanticが自動で422にしてくれるので、ここで個別に処理しなくてよい
"""
from fastapi import APIRouter, Depends

from app.db.connection import get_db
from app.services.order_items import create as order_items_create_service

router = APIRouter()
