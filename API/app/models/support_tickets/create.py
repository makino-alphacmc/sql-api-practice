"""support_tickets作成のリクエストモデル。

ここで必要な処理:
1. POSTのリクエストボディとして受け取りたいフィールドを定義する（主キーticket_idが自動採番なら含めない）
2. 必須項目・型を過不足なく指定する
3. レスポンス用のモデルは read.py のSupportTicketOutを再利用してよい
"""
from pydantic import BaseModel


class SupportTicketCreate(BaseModel):
    ...
