"""products作成(POST)のcontroller。

対象テーブル: products（主キー: product_id）
主なカラム: sku, product_name, category, price, is_active, tags(配列), specs(JSONB: 商品カテゴリにより異なるキー)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/products/create.py に用意する
2. POSTメソッドのルーター関数を定義する（レスポンスの型・ステータスコード201を指定する）
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/products/create.py の作成用関数を呼び出し、その戻り値をそのまま返す
5. 必須項目の不足や型違反はPydanticが自動で422にしてくれるので、ここで個別に処理しなくてよい
"""
from fastapi import APIRouter, Depends

from app.db.connection import get_db
from app.services.products import create as products_create_service

router = APIRouter()
