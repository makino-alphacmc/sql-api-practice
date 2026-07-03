"""support_tickets作成(POST)のcontroller。

対象テーブル: support_tickets（主キー: ticket_id）
主なカラム: customer_id(FK), order_id(FK, nullable), created_at, status, labels(配列), messages(JSONB配列)

ここで必要な処理:
1. リクエストボディを受け取るためのPydanticモデルを app/models/support_tickets/create.py に用意する
2. POSTメソッドのルーター関数を定義する（レスポンスの型・ステータスコード201を指定する）
3. Depends(get_db)でDBカーソルを受け取る
4. app/services/support_tickets/create.py の作成用関数を呼び出し、その戻り値をそのまま返す
5. 必須項目の不足や型違反はPydanticが自動で422にしてくれるので、ここで個別に処理しなくてよい
"""
from fastapi import APIRouter, Depends

from app.db.connection import get_db
from app.services.support_tickets import create as support_tickets_create_service

router = APIRouter()
