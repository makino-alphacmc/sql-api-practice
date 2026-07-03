"""order_items取得のレスポンスモデル。

対象テーブル: order_items（主キー: order_item_id）
主なカラム: order_id(FK), product_id(FK), quantity, unit_price, item_options(JSONB, nullable)

ここで必要な処理:
1. 上記カラムに対応するフィールドをBaseModelのサブクラスとして定義する
2. JSONB型のカラムは、内部構造に対応する別のBaseModelをネストして定義する
3. 配列型のカラムはList[str]などの型で受ける
4. NULL許可のカラムはOptional[...]にする
"""
from pydantic import BaseModel


class OrderItemOut(BaseModel):
    ...
