# products テーブル データ構造（サンプル）

```json
{
  "product_id": 101,
  "sku": "MOUSE-001",
  "product_name": "ワイヤレスマウス",
  "category": "PC周辺機器",
  "price": 2800,
  "is_active": true,
  "tags": ["wireless", "gadget", "beginner"],
  "specs": {
    "color": "black",
    "connection": "bluetooth",
    "warranty_months": 12,
    "weight_g": 85
  }
}
```

全60件。実データは `csv/products.csv` または `SELECT * FROM products;` で確認。
