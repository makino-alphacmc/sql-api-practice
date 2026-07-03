"""customers更新のリクエストモデル。

ここで必要な処理:
1. PUT（全項目更新）にする場合は、更新したい項目を必須フィールドとして定義する
2. PATCH（部分更新）にする場合は、全フィールドをOptionalにし、デフォルト値をNoneにする
"""
from pydantic import BaseModel


class CustomerUpdate(BaseModel):
    ...
