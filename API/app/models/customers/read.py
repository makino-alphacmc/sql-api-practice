"""customers取得のレスポンスモデル。

対象テーブル: customers（主キー: customer_id）
主なカラム: customer_name, email, prefecture, registered_at, phone_numbers(配列), profile(JSONB: rank, age_group, interests, notification{email,sms})

ここで必要な処理:
1. 上記カラムに対応するフィールドをBaseModelのサブクラスとして定義する
2. JSONB型のカラムは、内部構造に対応する別のBaseModelをネストして定義する
3. 配列型のカラムはList[str]などの型で受ける
4. NULL許可のカラムはOptional[...]にする
"""
from pydantic import BaseModel


class CustomerOut(BaseModel):
    ...
