"""sampleリソース（sample_itemsテーブル）のcontroller層。

controller / service / model の「基本形」を1ファイルずつで示すための参考実装。
CRUD(一覧・単体取得、作成、更新、削除)を1ファイルにまとめて書いている。
実際の練習用リソース(customers等)は create/read/update/delete でファイルを分けて
中身は空にしてあるので、書き方の参考としてこのファイルを見ながら実装する。
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response

from app.db.connection import get_db
from app.sample import service as sample_service
from app.sample.model import SampleItemCreate, SampleItemOut, SampleItemUpdate

router = APIRouter()


@router.get("", response_model=list[SampleItemOut])
def list_sample_items(is_active: Optional[bool] = None, cur=Depends(get_db)):
    return sample_service.list_sample_items(cur, is_active)


@router.get("/{item_id}", response_model=SampleItemOut)
def get_sample_item(item_id: int, cur=Depends(get_db)):
    item = sample_service.get_sample_item_by_id(cur, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="sample_item not found")
    return item


@router.post("", response_model=SampleItemOut, status_code=201)
def create_sample_item(body: SampleItemCreate, cur=Depends(get_db)):
    return sample_service.create_sample_item(cur, body)


@router.put("/{item_id}", response_model=SampleItemOut)
def update_sample_item(item_id: int, body: SampleItemUpdate, cur=Depends(get_db)):
    updated = sample_service.update_sample_item(cur, item_id, body)
    if updated is None:
        raise HTTPException(status_code=404, detail="sample_item not found")
    return updated


@router.delete("/{item_id}", status_code=204)
def delete_sample_item(item_id: int, cur=Depends(get_db)):
    deleted = sample_service.delete_sample_item(cur, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="sample_item not found")
    return Response(status_code=204)
