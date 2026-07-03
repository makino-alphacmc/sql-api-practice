"""sampleリソース（sample_itemsテーブル）のモデル定義。

controller / service / model の「基本形」を1ファイルずつで示すための参考実装。
実際の練習では models/<リソース名>/{create,read,update,delete}.py のように
CRUD操作ごとにファイルを分けるが、ここではまとめて1ファイルに書いている。

このファイルは動くコード（見本）です。練習用の5リソース（customers等）の
答えではないので、そのまま流用はできません。書き方の型として参考にしてください。
"""
from typing import Optional

from pydantic import BaseModel


class SampleItemOut(BaseModel):
    """レスポンス用モデル。テーブルの列にそのまま対応させる。"""

    item_id: int
    name: str
    price: int
    is_active: bool


class SampleItemCreate(BaseModel):
    """POST用リクエストモデル。主キー(item_id)は自動採番なので含めない。"""

    name: str
    price: int
    is_active: bool = True


class SampleItemUpdate(BaseModel):
    """PATCH用リクエストモデル。部分更新できるように全項目Optionalにする。"""

    name: Optional[str] = None
    price: Optional[int] = None
    is_active: Optional[bool] = None
