# order_items テーブル データ構造（サンプル）

```json
{
  "order_item_id": 5001,
  "order_id": 1001,
  "product_id": 101,
  "quantity": 1,
  "unit_price": 2800,
  "item_options": {
    "color": "black",
    "gift_wrap": false
  }
}
```

全108件。実データは `csv/order_items.csv` または `SELECT * FROM order_items;` で確認。
