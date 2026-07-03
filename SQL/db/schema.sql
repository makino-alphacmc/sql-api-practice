-- SQL練習用ECデータベース スキーマ定義
-- README.md 5章の定義に対応
-- 実行順は README.md 8章のFK依存順（customers -> products -> orders -> order_items -> support_tickets）

DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id    INTEGER PRIMARY KEY,
    customer_name  VARCHAR(100) NOT NULL,
    email          VARCHAR(255) NOT NULL UNIQUE,
    prefecture     VARCHAR(50) NOT NULL,
    registered_at  DATE NOT NULL,
    phone_numbers  TEXT[],
    profile        JSONB NOT NULL
);

CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    sku           VARCHAR(50) NOT NULL UNIQUE,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50) NOT NULL,
    price         INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL,
    tags          TEXT[],
    specs         JSONB NOT NULL
);

CREATE TABLE orders (
    order_id          INTEGER PRIMARY KEY,
    customer_id       INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date        TIMESTAMP NOT NULL,
    status            VARCHAR(30) NOT NULL,
    payment_method    VARCHAR(30) NOT NULL,
    coupon_codes      TEXT[],
    delivery_address  JSONB NOT NULL,
    order_note        JSONB
);

CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    quantity       INTEGER NOT NULL,
    unit_price     INTEGER NOT NULL,
    item_options   JSONB
);

CREATE TABLE support_tickets (
    ticket_id    INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_id     INTEGER REFERENCES orders(order_id),
    created_at   TIMESTAMP NOT NULL,
    status       VARCHAR(30) NOT NULL,
    labels       TEXT[],
    messages     JSONB NOT NULL
);
