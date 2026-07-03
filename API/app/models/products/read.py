"""products取得のレスポンスモデル。

対象テーブル: products（主キー: product_id）
主なカラム: sku, product_name, category, price, is_active, tags(配列), specs(JSONB: 商品カテゴリにより異なるキー)

ここで必要な処理:
1. 上記カラムに対応するフィールドをBaseModelのサブクラスとして定義する
2. JSONB型のカラムは、内部構造に対応する別のBaseModelをネストして定義する
3. 配列型のカラムはList[str]などの型で受ける
4. NULL許可のカラムはOptional[...]にする
"""
from pydantic import BaseModel


class ProductOut(BaseModel):
    ...
