-- CSVデータ投入スクリプト
-- README.md 8章のFK依存順で実行すること（customers -> products -> orders -> order_items -> support_tickets）
-- psqlのカレントディレクトリからの相対パスで \copy を使う（サーバー側ではなくクライアント側読み込みのため権限不要）

\copy customers FROM 'csv/customers.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy products FROM 'csv/products.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy orders FROM 'csv/orders.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy order_items FROM 'csv/order_items.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy support_tickets FROM 'csv/support_tickets.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
