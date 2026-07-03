# orders テーブル データ構造（サンプル）

```json
{
  "order_id": 1001,
  "customer_id": 1,
  "order_date": "2025-03-01 10:15:00",
  "status": "shipped",
  "payment_method": "card",
  "coupon_codes": ["WELCOME10"],
  "delivery_address": {
    "zip": "100-0001",
    "prefecture": "東京都",
    "city": "千代田区",
    "is_remote_area": false
  },
  "order_note": {
    "gift": false,
    "source": "web"
  }
}
```

全60件。実データは `csv/orders.csv` または `SELECT * FROM orders;` で確認。
