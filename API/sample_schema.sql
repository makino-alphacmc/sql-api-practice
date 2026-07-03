-- app/sample/ の参考実装デモ専用テーブル。
-- SQL練習・API練習(customers/products/orders/order_items/support_tickets)とは無関係。
-- POST/PUT/DELETEで自由に汚してよいテーブルとして分離している。

DROP TABLE IF EXISTS sample_items;

CREATE TABLE sample_items (
    item_id     SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    price       INTEGER NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT true
);

INSERT INTO sample_items (name, price, is_active) VALUES
    ('サンプル商品A', 1000, true),
    ('サンプル商品B', 2000, false);
