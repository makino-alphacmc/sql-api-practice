# customers テーブル データ構造（サンプル）

```json
{
  "customer_id": 1,
  "customer_name": "佐藤 花子",
  "email": "hanako.sato@example.com",
  "prefecture": "東京都",
  "registered_at": "2025-01-05",
  "phone_numbers": ["090-1111-1111", "03-1111-1111"],
  "profile": {
    "rank": "gold",
    "age_group": "30s",
    "interests": ["travel", "coffee", "gadget"],
    "notification": { "email": true, "sms": false }
  }
}
```

全60件。実データは `csv/customers.csv` または `SELECT * FROM customers;` で確認。
