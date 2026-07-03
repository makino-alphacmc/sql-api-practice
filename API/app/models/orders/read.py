"""orders取得のレスポンスモデル。

対象テーブル: orders（主キー: order_id）
主なカラム: customer_id(FK), order_date, status, payment_method, coupon_codes(配列), delivery_address(JSONB), order_note(JSONB, nullable)

ここで必要な処理:
1. 上記カラムに対応するフィールドをBaseModelのサブクラスとして定義する
2. JSONB型のカラムは、内部構造に対応する別のBaseModelをネストして定義する
3. 配列型のカラムはList[str]などの型で受ける
4. NULL許可のカラムはOptional[...]にする
"""
from pydantic import BaseModel


class OrderOut(BaseModel):
    ...
