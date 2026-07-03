# support_tickets テーブル データ構造（サンプル）

```json
{
  "ticket_id": 9001,
  "customer_id": 1,
  "order_id": 1001,
  "created_at": "2025-03-02 12:00:00",
  "status": "closed",
  "labels": ["delivery", "question"],
  "messages": [
    { "sender": "customer", "message": "配送日はいつですか？", "sent_at": "2025-03-02 12:00:00" },
    { "sender": "support", "message": "明日到着予定です。", "sent_at": "2025-03-02 12:10:00" }
  ]
}
```

全54件。実データは `csv/support_tickets.csv` または `SELECT * FROM support_tickets;` で確認。
