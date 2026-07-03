"""customers作成(POST)のcontroller。

対象テーブル: customers（主キー: customer_id）
主なカラム: customer_name, email, prefecture, registered_at, phone_numbers(配列), profile(JSONB: rank, age_group, interests, notification{email,sms})

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/customers/create.py に用意する
2. POSTメソッドのルーター関数を定義する（レスポンスの型・ステータスコード201を指定する）
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/customers/create.py の作成用関数を呼び出し、その戻り値をそのまま返す
5. 必須項目の不足や型違反はPydanticが自動で422にしてくれるので、ここで個別に処理しなくてよい
"""
from fastapi import APIRouter, Depends

from app.db.connection import get_db
from app.services.customers import create as customers_create_service

router = APIRouter()
