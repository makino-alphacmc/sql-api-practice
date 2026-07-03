"""products取得(GET)のcontroller。一覧取得と単体取得の両方をここに書く。

対象テーブル: products（主キー: product_id）
主なカラム: sku, product_name, category, price, is_active, tags(配列), specs(JSONB: 商品カテゴリにより異なるキー)

ここで必要な処理:

[一覧取得 GET /products]
1. 絞り込み用のクエリパラメータを受け取る関数を定義する
   （単一値・複数値・範囲指定・真偽値・ページネーションなど、API_EXAM.md 0.5のパターンを検討する）
2. Depends(get_db)でDBカーソルを受け取る
3. app/services/products/read.py の一覧取得用関数を呼び出し、結果をそのまま返す

[単体取得 GET /products/{product_id}]
1. パスパラメータとしてproduct_idを受け取る関数を定義する
2. app/services/products/read.py の単体取得用関数を呼び出す
3. 結果がNoneだった場合はHTTPExceptionで404を返す
4. 見つかった場合はそのまま返す
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.db.connection import get_db
from app.services.products import read as products_read_service

router = APIRouter()
