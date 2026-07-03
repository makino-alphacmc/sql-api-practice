"""products更新(PUT/PATCH)のcontroller。

対象テーブル: products（主キー: product_id）
主なカラム: sku, product_name, category, price, is_active, tags(配列), specs(JSONB: 商品カテゴリにより異なるキー)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/products/update.py に用意する
   （PUTなら全項目必須、PATCHなら全項目Optionalにするなど方針を決める）
2. パスパラメータで対象のproduct_idを受け取る
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/products/update.py の更新用関数を呼び出す
5. 戻り値がNone（対象が存在しない）だった場合はHTTPExceptionで404を返す
6. 更新後のレコードをレスポンスとして返す
"""
from fastapi import APIRouter, Depends, HTTPException

from app.db.connection import get_db
from app.services.products import update as products_update_service

router = APIRouter()
