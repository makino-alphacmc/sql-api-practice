# SQL学習用ECデータベース仕様書

## 1. 概要

このデータベースは、SQL学習用に作成した **ECサイト風のサンプルデータベース** です。
通常のリレーショナルテーブルに加えて、PostgreSQLの実務でよく使われる以下の要素を含みます。

- 通常カラム
- 主キー `PRIMARY KEY`
- 外部キー `FOREIGN KEY`
- 配列型 `TEXT[]`
- JSONB型 `JSONB`
- 1対多のリレーション
- nullableな外部キー

主な学習テーマは以下です。

- `SELECT`
- `WHERE`
- `ORDER BY`
- `JOIN`
- `LEFT JOIN`
- `GROUP BY`
- `COUNT`
- `SUM`
- `CASE`
- 配列検索
- JSONB検索
- JSONBからの値抽出
- 集計SQL
- 実務的なデータ比較

---

## 2. 使用DB

想定DBMSは **PostgreSQL** です。

理由は、PostgreSQLでは以下を自然に扱えるためです。

| 機能                 | PostgreSQLでの型・構文 |
| -------------------- | ---------------------- |
| 配列                 | `TEXT[]`               |
| JSON                 | `JSONB`                |
| JSON文字列取得       | `->>`                  |
| JSONオブジェクト取得 | `->`                   |
| 配列内検索           | `ANY()` / `@>`         |
| JSON配列内検索       | `?`                    |

---

## 3. ER図イメージ

```text
customers
  │ 1
  │
  │ customer_id
  ▼ 多
orders
  │ 1
  │
  │ order_id
  ▼ 多
order_items
  ▲ 多
  │
  │ product_id
  │ 1
products

customers
  │ 1
  │
  │ customer_id
  ▼ 多
support_tickets

orders
  │ 1
  │
  │ order_id
  ▼ 0..多
support_tickets
```

---

## 4. テーブル一覧

| テーブル名        | 論理名     | 概要                                                               |
| ----------------- | ---------- | ------------------------------------------------------------------ |
| `customers`       | 顧客       | 顧客の基本情報、電話番号配列、プロフィールJSONを管理する           |
| `products`        | 商品       | 商品情報、タグ配列、商品スペックJSONを管理する                     |
| `orders`          | 注文       | 注文ヘッダー情報、クーポン配列、配送先JSON、注文メモJSONを管理する |
| `order_items`     | 注文明細   | 注文に含まれる商品ごとの数量・単価・オプションJSONを管理する       |
| `support_tickets` | 問い合わせ | 顧客問い合わせ、ラベル配列、メッセージ履歴JSONを管理する           |

---

# 5. テーブル定義

---

## 5.1 `customers` テーブル

### 概要

顧客情報を管理するテーブルです。

1人の顧客は複数の注文を持つことができます。
また、1人の顧客は複数の問い合わせを持つことができます。

### カラム定義

| カラム名        | 型             | NULL許可 | キー   | 説明                 |
| --------------- | -------------- | -------: | ------ | -------------------- |
| `customer_id`   | `INTEGER`      |     不可 | PK     | 顧客ID               |
| `customer_name` | `VARCHAR(100)` |     不可 |        | 顧客名               |
| `email`         | `VARCHAR(255)` |     不可 | UNIQUE | メールアドレス       |
| `prefecture`    | `VARCHAR(50)`  |     不可 |        | 都道府県             |
| `registered_at` | `DATE`         |     不可 |        | 会員登録日           |
| `phone_numbers` | `TEXT[]`       |       可 |        | 電話番号の配列       |
| `profile`       | `JSONB`        |     不可 |        | 顧客プロフィール情報 |

### 配列カラム

#### `phone_numbers`

複数の電話番号を配列で保持します。

例：

```text
{"090-1111-1111","03-1111-1111"}
```

### JSONBカラム

#### `profile`

顧客の詳細プロフィールをJSONBで保持します。

例：

```json
{
	"rank": "gold",
	"age_group": "30s",
	"interests": ["travel", "coffee", "gadget"],
	"notification": {
		"email": true,
		"sms": false
	}
}
```

### `profile` の主なキー

| JSONキー             | 型      | 説明                                          |
| -------------------- | ------- | --------------------------------------------- |
| `rank`               | string  | 顧客ランク。`gold` / `silver` / `bronze` など |
| `age_group`          | string  | 年代                                          |
| `interests`          | array   | 興味・関心の配列                              |
| `notification.email` | boolean | メール通知の可否                              |
| `notification.sms`   | boolean | SMS通知の可否                                 |

### 主な利用例

#### 顧客ランクを取り出す

```sql
SELECT
    customer_id,
    customer_name,
    profile ->> 'rank' AS rank
FROM
    customers;
```

#### travelに興味がある顧客を取得する

```sql
SELECT
    customer_id,
    customer_name,
    profile -> 'interests' AS interests
FROM
    customers
WHERE
    profile -> 'interests' ? 'travel';
```

---

## 5.2 `products` テーブル

### 概要

商品情報を管理するテーブルです。

1つの商品は複数の注文明細に登場できます。

### カラム定義

| カラム名       | 型             | NULL許可 | キー   | 説明           |
| -------------- | -------------- | -------: | ------ | -------------- |
| `product_id`   | `INTEGER`      |     不可 | PK     | 商品ID         |
| `sku`          | `VARCHAR(50)`  |     不可 | UNIQUE | 商品SKU        |
| `product_name` | `VARCHAR(100)` |     不可 |        | 商品名         |
| `category`     | `VARCHAR(50)`  |     不可 |        | 商品カテゴリ   |
| `price`        | `INTEGER`      |     不可 |        | 現在の商品価格 |
| `is_active`    | `BOOLEAN`      |     不可 |        | 販売中フラグ   |
| `tags`         | `TEXT[]`       |       可 |        | 商品タグの配列 |
| `specs`        | `JSONB`        |     不可 |        | 商品スペック   |

### 配列カラム

#### `tags`

商品に紐づくタグを配列で保持します。

例：

```text
{"wireless","gadget","beginner"}
```

### JSONBカラム

#### `specs`

商品ごとに異なるスペックをJSONBで保持します。

例：

```json
{
	"color": "black",
	"connection": "bluetooth",
	"warranty_months": 12,
	"weight_g": 85
}
```

### `specs` に入り得る主なキー

| JSONキー          | 型      | 対象商品例          | 説明               |
| ----------------- | ------- | ------------------- | ------------------ |
| `color`           | string  | マウス、モニター    | 色                 |
| `connection`      | string  | マウス              | 接続方式           |
| `warranty_months` | number  | 多くの商品          | 保証期間（月）     |
| `weight_g`        | number  | マウス、食品        | 重量               |
| `switch`          | string  | キーボード          | キースイッチ       |
| `layout`          | string  | キーボード          | 配列               |
| `backlight`       | boolean | キーボード          | バックライト有無   |
| `size_inch`       | number  | モニター            | 画面サイズ         |
| `resolution`      | string  | モニター、Webカメラ | 解像度             |
| `refresh_rate`    | number  | モニター            | リフレッシュレート |
| `material`        | string  | チェア              | 素材               |
| `has_headrest`    | boolean | チェア              | ヘッドレスト有無   |
| `origin`          | string  | コーヒー豆          | 原産国             |
| `roast`           | string  | コーヒー豆          | 焙煎度             |
| `reason_inactive` | string  | 非アクティブ商品    | 販売停止理由       |

### 主な利用例

#### gadgetタグを含む商品を取得する

```sql
SELECT
    product_id,
    product_name,
    tags
FROM
    products
WHERE
    'gadget' = ANY(tags);
```

#### 保証期間が12ヶ月以上の商品を取得する

```sql
SELECT
    product_id,
    product_name,
    (specs ->> 'warranty_months')::INTEGER AS warranty_months
FROM
    products
WHERE
    (specs ->> 'warranty_months')::INTEGER >= 12;
```

---

## 5.3 `orders` テーブル

### 概要

注文ヘッダー情報を管理するテーブルです。

1つの注文は1人の顧客に紐づきます。
1つの注文は複数の注文明細を持つことができます。
また、問い合わせが注文に紐づく場合もあります。

### カラム定義

| カラム名           | 型            | NULL許可 | キー | 説明                             |
| ------------------ | ------------- | -------: | ---- | -------------------------------- |
| `order_id`         | `INTEGER`     |     不可 | PK   | 注文ID                           |
| `customer_id`      | `INTEGER`     |     不可 | FK   | 顧客ID                           |
| `order_date`       | `TIMESTAMP`   |     不可 |      | 注文日時                         |
| `status`           | `VARCHAR(30)` |     不可 |      | 注文ステータス                   |
| `payment_method`   | `VARCHAR(30)` |     不可 |      | 支払い方法                       |
| `coupon_codes`     | `TEXT[]`      |       可 |      | 利用クーポンコードの配列         |
| `delivery_address` | `JSONB`       |     不可 |      | 配送先住所                       |
| `order_note`       | `JSONB`       |       可 |      | 注文メモ、流入元、ギフト情報など |

### 外部キー

| カラム        | 参照先                  |
| ------------- | ----------------------- |
| `customer_id` | `customers.customer_id` |

### ステータス一覧

| status     | 意味       |
| ---------- | ---------- |
| `shipped`  | 発送済み   |
| `pending`  | 保留中     |
| `canceled` | キャンセル |

### 支払い方法一覧

| payment_method | 意味             |
| -------------- | ---------------- |
| `card`         | クレジットカード |
| `bank`         | 銀行振込         |
| `convenience`  | コンビニ払い     |

### 配列カラム

#### `coupon_codes`

注文時に利用されたクーポンコードを配列で保持します。

例：

```text
{"WELCOME10","COFFEE50"}
```

クーポン未使用の場合は空配列です。

```text
{}
```

### JSONBカラム

#### `delivery_address`

配送先住所をJSONBで保持します。

例：

```json
{
	"zip": "355-0001",
	"prefecture": "埼玉県",
	"city": "東松山市",
	"is_remote_area": false
}
```

#### `order_note`

注文に関する補足情報をJSONBで保持します。

例：

```json
{
	"gift": true,
	"source": "web",
	"memo": "新居用"
}
```

### `order_note` の主なキー

| JSONキー        | 型      | 説明                           |
| --------------- | ------- | ------------------------------ |
| `gift`          | boolean | ギフト注文かどうか             |
| `source`        | string  | 注文流入元。`web` / `app` など |
| `memo`          | string  | 注文メモ                       |
| `cancel_reason` | string  | キャンセル理由                 |

### 主な利用例

#### WELCOME10クーポンを使った注文を取得する

```sql
SELECT
    order_id,
    customer_id,
    coupon_codes
FROM
    orders
WHERE
    'WELCOME10' = ANY(coupon_codes);
```

#### ギフト注文を取得する

```sql
SELECT
    order_id,
    customer_id,
    order_note ->> 'gift' AS gift
FROM
    orders
WHERE
    (order_note ->> 'gift')::BOOLEAN = true;
```

---

## 5.4 `order_items` テーブル

### 概要

注文明細を管理するテーブルです。

1つの注文に対して、複数の商品明細が紐づきます。

このテーブルでは、購入時点の単価を `unit_price` として保持します。
これは、商品マスタ側の `products.price` が将来変更されても、当時の売上金額を正しく計算するためです。

### カラム定義

| カラム名        | 型        | NULL許可 | キー | 説明           |
| --------------- | --------- | -------: | ---- | -------------- |
| `order_item_id` | `INTEGER` |     不可 | PK   | 注文明細ID     |
| `order_id`      | `INTEGER` |     不可 | FK   | 注文ID         |
| `product_id`    | `INTEGER` |     不可 | FK   | 商品ID         |
| `quantity`      | `INTEGER` |     不可 |      | 数量           |
| `unit_price`    | `INTEGER` |     不可 |      | 購入時点の単価 |
| `item_options`  | `JSONB`   |       可 |      | 商品オプション |

### 外部キー

| カラム       | 参照先                |
| ------------ | --------------------- |
| `order_id`   | `orders.order_id`     |
| `product_id` | `products.product_id` |

### JSONBカラム

#### `item_options`

商品ごとの購入オプションをJSONBで保持します。

例：

```json
{
	"color": "black",
	"gift_wrap": false
}
```

### `item_options` の主なキー

| JSONキー    | 型      | 説明                 |
| ----------- | ------- | -------------------- |
| `color`     | string  | 色指定               |
| `gift_wrap` | boolean | ギフト包装の有無     |
| `length_m`  | number  | ケーブル長           |
| `switch`    | string  | キーボードのスイッチ |
| `grind`     | string  | コーヒー豆の挽き方   |

### 主な利用例

#### 明細ごとの小計を計算する

```sql
SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price AS subtotal
FROM
    order_items;
```

#### ギフト包装ありの明細を取得する

```sql
SELECT
    order_item_id,
    order_id,
    product_id,
    item_options ->> 'gift_wrap' AS gift_wrap
FROM
    order_items
WHERE
    (item_options ->> 'gift_wrap')::BOOLEAN = true;
```

---

## 5.5 `support_tickets` テーブル

### 概要

顧客からの問い合わせ情報を管理するテーブルです。

1つの問い合わせは必ず1人の顧客に紐づきます。
注文に関する問い合わせの場合は `order_id` に注文IDが入ります。
注文と関係ない問い合わせの場合は `order_id` がNULLになる想定です。

### カラム定義

| カラム名      | 型            | NULL許可 | キー | 説明                   |
| ------------- | ------------- | -------: | ---- | ---------------------- |
| `ticket_id`   | `INTEGER`     |     不可 | PK   | 問い合わせID           |
| `customer_id` | `INTEGER`     |     不可 | FK   | 顧客ID                 |
| `order_id`    | `INTEGER`     |       可 | FK   | 注文ID                 |
| `created_at`  | `TIMESTAMP`   |     不可 |      | 問い合わせ作成日時     |
| `status`      | `VARCHAR(30)` |     不可 |      | 問い合わせステータス   |
| `labels`      | `TEXT[]`      |       可 |      | 問い合わせラベルの配列 |
| `messages`    | `JSONB`       |     不可 |      | メッセージ履歴         |

### 外部キー

| カラム        | 参照先                  |
| ------------- | ----------------------- |
| `customer_id` | `customers.customer_id` |
| `order_id`    | `orders.order_id`       |

### ステータス一覧

| status   | 意味     |
| -------- | -------- |
| `open`   | 対応中   |
| `closed` | 対応完了 |

### 配列カラム

#### `labels`

問い合わせ内容を分類するためのラベルを配列で保持します。

例：

```text
{"gift","address_change"}
```

### JSONBカラム

#### `messages`

問い合わせのメッセージ履歴をJSONB配列として保持します。

例：

```json
[
	{
		"sender": "customer",
		"message": "配送日はいつですか？",
		"sent_at": "2025-03-02 12:00:00"
	},
	{
		"sender": "support",
		"message": "明日到着予定です。",
		"sent_at": "2025-03-02 12:10:00"
	}
]
```

### `messages` 内の主なキー

| JSONキー  | 型     | 説明                                |
| --------- | ------ | ----------------------------------- |
| `sender`  | string | 送信者。`customer` / `support` など |
| `message` | string | メッセージ本文                      |
| `sent_at` | string | 送信日時                            |

### 主な利用例

#### paymentラベルを含む問い合わせを取得する

```sql
SELECT
    ticket_id,
    customer_id,
    labels
FROM
    support_tickets
WHERE
    'payment' = ANY(labels);
```

#### メッセージ数を取得する

```sql
SELECT
    ticket_id,
    jsonb_array_length(messages) AS message_count
FROM
    support_tickets;
```

---

# 6. リレーション仕様

## 6.1 `customers` と `orders`

| 関係     | 内容                                         |
| -------- | -------------------------------------------- |
| 1対多    | 1人の顧客は複数の注文を持つ                  |
| 結合キー | `customers.customer_id = orders.customer_id` |

### JOIN例

```sql
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    o.status
FROM
    customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id;
```

---

## 6.2 `orders` と `order_items`

| 関係     | 内容                                     |
| -------- | ---------------------------------------- |
| 1対多    | 1つの注文は複数の注文明細を持つ          |
| 結合キー | `orders.order_id = order_items.order_id` |

### JOIN例

```sql
SELECT
    o.order_id,
    o.order_date,
    oi.order_item_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price
FROM
    orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id;
```

---

## 6.3 `products` と `order_items`

| 関係     | 内容                                           |
| -------- | ---------------------------------------------- |
| 1対多    | 1つの商品は複数の注文明細に登場する            |
| 結合キー | `products.product_id = order_items.product_id` |

### JOIN例

```sql
SELECT
    p.product_id,
    p.product_name,
    oi.order_id,
    oi.quantity,
    oi.unit_price
FROM
    products p
INNER JOIN order_items oi
    ON p.product_id = oi.product_id;
```

---

## 6.4 `customers` と `support_tickets`

| 関係     | 内容                                                  |
| -------- | ----------------------------------------------------- |
| 1対多    | 1人の顧客は複数の問い合わせを持つ                     |
| 結合キー | `customers.customer_id = support_tickets.customer_id` |

---

## 6.5 `orders` と `support_tickets`

| 関係     | 内容                                            |
| -------- | ----------------------------------------------- |
| 1対0..多 | 1つの注文に複数の問い合わせが紐づく可能性がある |
| 結合キー | `orders.order_id = support_tickets.order_id`    |
| 注意     | `support_tickets.order_id` はNULL許可           |

注文に紐づかない問い合わせもある想定なので、実務では `LEFT JOIN` の練習にも使えます。

---

# 7. CSVファイル構成

このDBは以下のCSVファイルに分けて管理します。

| CSVファイル           | 対応テーブル      |
| --------------------- | ----------------- |
| `customers.csv`       | `customers`       |
| `products.csv`        | `products`        |
| `orders.csv`          | `orders`          |
| `order_items.csv`     | `order_items`     |
| `support_tickets.csv` | `support_tickets` |

---

# 8. CSVインポート順

外部キー制約があるため、以下の順番でインポートします。

```text
1. customers
2. products
3. orders
4. order_items
5. support_tickets
```

理由は以下です。

- `orders` は `customers` を参照する
- `order_items` は `orders` と `products` を参照する
- `support_tickets` は `customers` と `orders` を参照する

---

# 9. 配列・JSONBカラムの扱い方

## 9.1 PostgreSQL配列の例

### 配列リテラル

```text
{"WELCOME10","COFFEE50"}
```

### 配列に値が含まれるか確認する

```sql
SELECT
    order_id,
    coupon_codes
FROM
    orders
WHERE
    'WELCOME10' = ANY(coupon_codes);
```

### `@>` を使う書き方

```sql
SELECT
    order_id,
    coupon_codes
FROM
    orders
WHERE
    coupon_codes @> ARRAY['WELCOME10'];
```

---

## 9.2 JSONBの値を取得する

### JSONとして取得する

```sql
profile -> 'interests'
```

### 文字列として取得する

```sql
profile ->> 'rank'
```

### 数値として比較する

```sql
(specs ->> 'warranty_months')::INTEGER >= 12
```

### 真偽値として比較する

```sql
(order_note ->> 'gift')::BOOLEAN = true
```

---

# 10. 実務的な設計メモ

## 10.1 通常カラムにした方がよいもの

以下のような値は、検索・集計・JOINでよく使うため、JSONBではなく通常カラムにする方が扱いやすいです。

- 顧客ID
- 商品ID
- 注文ID
- 注文日
- 注文ステータス
- 支払い方法
- 商品価格
- 数量
- 購入時単価

## 10.2 配列やJSONBに向いているもの

以下のような値は、項目数や構造が変わりやすいため、配列やJSONBに向いています。

- タグ
- クーポンコード
- 通知設定
- 商品スペック
- 注文メモ
- ギフト設定
- 問い合わせラベル
- 問い合わせメッセージ履歴
- 外部APIレスポンス

## 10.3 注意点

配列やJSONBは便利ですが、乱用すると以下の問題が起きやすくなります。

- JOINしづらい
- 集計しづらい
- 型の保証が弱くなる
- インデックス設計が難しくなる
- データの揺れが起きやすい

そのため、実務では以下のように判断します。

| 判断基準                     | 推奨される持ち方 |
| ---------------------------- | ---------------- |
| 集計・検索・JOINで頻繁に使う | 通常カラム       |
| 1対多で厳密に管理したい      | 別テーブル       |
| 可変項目・補足情報           | JSONB            |
| 単純な複数値                 | 配列             |

---

# 11. 練習問題で使いやすいSQLテーマ

このDBでは、以下のような問題を作成できます。

## 11.1 基礎SELECT

- 全顧客一覧を取得する
- 埼玉県の顧客だけ取得する
- 価格が10,000円以上の商品を取得する
- 有効な商品だけ取得する

## 11.2 配列検索

- `gadget` タグを持つ商品を取得する
- `WELCOME10` クーポンを使った注文を取得する
- `payment` ラベルを持つ問い合わせを取得する

## 11.3 JSONB検索

- `gold` ランクの顧客を取得する
- `travel` に興味がある顧客を取得する
- ギフト注文を取得する
- 保証期間が12ヶ月以上の商品を取得する

## 11.4 JOIN

- 顧客名付きの注文一覧を取得する
- 商品名付きの注文明細を取得する
- 顧客別の注文数を取得する
- 商品別の販売数を取得する

## 11.5 集計

- 注文ごとの合計金額を計算する
- 顧客ごとの購入金額を計算する
- 商品カテゴリ別の売上を計算する
- 月別売上を計算する

## 11.6 実務寄り

- キャンセル注文を除いた売上を計算する
- 未購入顧客を抽出する
- 問い合わせがある注文だけ取得する
- 問い合わせがない注文だけ取得する
- ギフト包装ありの明細を抽出する
- 注文流入元ごとの売上を集計する

---

# 12. 代表的な確認SQL

## 12.1 全テーブルの件数確認

```sql
SELECT 'customers' AS table_name, COUNT(*) AS count FROM customers
UNION ALL
SELECT 'products' AS table_name, COUNT(*) AS count FROM products
UNION ALL
SELECT 'orders' AS table_name, COUNT(*) AS count FROM orders
UNION ALL
SELECT 'order_items' AS table_name, COUNT(*) AS count FROM order_items
UNION ALL
SELECT 'support_tickets' AS table_name, COUNT(*) AS count FROM support_tickets;
```

期待される件数は以下です。

| table_name      | count |
| --------------- | ----: |
| customers       |     6 |
| products        |     7 |
| orders          |     8 |
| order_items     |    12 |
| support_tickets |     4 |

---

## 12.2 注文ごとの合計金額

```sql
SELECT
    o.order_id,
    o.status,
    SUM(oi.quantity * oi.unit_price) AS order_total
FROM
    orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    o.status
ORDER BY
    o.order_id;
```

---

## 12.3 顧客別の購入金額

```sql
SELECT
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_amount
FROM
    customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE
    o.status <> 'canceled'
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    total_amount DESC;
```

---

# 13. 学習時の基本ルール

SQLを書くときは、以下の順番で考えると整理しやすいです。

```text
1. どのテーブルが必要か
2. JOINが必要か
3. どの行に絞るか
4. どの列を表示するか
5. 集計が必要か
6. 並び順はどうするか
7. 期待結果と一致するか
```

SQLの実行順イメージは以下です。

```text
FROM
↓
JOIN
↓
WHERE
↓
GROUP BY
↓
HAVING
↓
SELECT
↓
ORDER BY
```

---

# 14. 今後追加しやすいテーブル案

より実務寄りにする場合、以下のテーブルを追加できます。

| 追加テーブル            | 用途           |
| ----------------------- | -------------- |
| `payments`              | 決済履歴       |
| `shipments`             | 発送履歴       |
| `inventory_movements`   | 在庫増減履歴   |
| `reviews`               | 商品レビュー   |
| `coupons`               | クーポンマスタ |
| `product_price_history` | 商品価格履歴   |
| `login_events`          | ログイン履歴   |
| `cart_items`            | カート情報     |

---

# 15. 補足

このDBは学習用のため、実務DBよりも一部シンプルにしています。

ただし、以下のような実務で頻出する設計要素は含めています。

- マスタ系テーブル
- トランザクション系テーブル
- 明細テーブル
- JSONBによる可変情報管理
- 配列によるタグ・ラベル管理
- nullableな外部キー
- 購入時単価の保持
- キャンセル注文の扱い
- 問い合わせ履歴の保持

この仕様をベースに、SQL Zoo形式で問題を増やしていくことができます。
