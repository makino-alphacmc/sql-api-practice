"""support_tickets取得のレスポンスモデル。

対象テーブル: support_tickets（主キー: ticket_id）
主なカラム: customer_id(FK), order_id(FK, nullable), created_at, status, labels(配列), messages(JSONB配列)

ここで必要な処理:
1. 上記カラムに対応するフィールドをBaseModelのサブクラスとして定義する
2. JSONB型のカラムは、内部構造に対応する別のBaseModelをネストして定義する
3. 配列型のカラムはList[str]などの型で受ける
4. NULL許可のカラムはOptional[...]にする
"""
from pydantic import BaseModel


class SupportTicketOut(BaseModel):
    ...
