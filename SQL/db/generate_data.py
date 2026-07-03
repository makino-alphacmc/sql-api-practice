#!/usr/bin/env python3
"""
sql-practice用ECデータベースのサンプルデータを増量するスクリプト。
既存のcsv/*.csvの先頭データ(customer_id 1-6など)はそのまま残し、
その後ろに新規レコードを追記して各CSVを丸ごと書き直す。

実行: python3 db/generate_data.py  (sql-practiceディレクトリから実行すること)
"""
import csv
import json
import random
from pathlib import Path

random.seed(42)

BASE = Path(__file__).resolve().parent.parent
CSV_DIR = BASE / "csv"

# ---------- マスタデータ ----------

SURNAMES = [
    "佐藤", "鈴木", "高橋", "田中", "伊藤", "渡辺", "山本", "中村", "小林", "加藤",
    "吉田", "山田", "佐々木", "山口", "松本", "井上", "木村", "林", "斎藤", "清水",
    "山崎", "森", "池田", "橋本", "阿部", "石川", "前田", "藤田", "後藤", "近藤",
    "村上", "遠藤", "青木", "坂本", "福田", "太田", "西村", "藤井", "岡田", "長谷川",
    "原田", "松田", "石井", "中川", "中野", "原", "小川", "竹内", "金子", "和田",
    "中山", "石田", "上田", "森田", "小野", "柴田", "武田", "菅原", "横山", "大野",
]
GIVEN_NAMES = [
    "花子", "太郎", "美香", "健", "葵", "一郎", "直樹", "由美", "和也", "恵子",
    "亮", "美咲", "拓也", "愛子", "大輔", "真由美", "翔太", "沙織", "健太", "麻衣",
    "勇気", "彩", "海斗", "optional", "健二", "美穂", "隆", "由紀", "涼太", "千尋",
]
GIVEN_NAMES = [g for g in GIVEN_NAMES if g != "optional"]

ROMAJI_SURNAME = {
    "佐藤": "sato", "鈴木": "suzuki", "高橋": "takahashi", "田中": "tanaka", "伊藤": "ito",
    "渡辺": "watanabe", "山本": "yamamoto", "中村": "nakamura", "小林": "kobayashi", "加藤": "kato",
    "吉田": "yoshida", "山田": "yamada", "佐々木": "sasaki", "山口": "yamaguchi", "松本": "matsumoto",
    "井上": "inoue", "木村": "kimura", "林": "hayashi", "斎藤": "saito", "清水": "shimizu",
    "山崎": "yamazaki", "森": "mori", "池田": "ikeda", "橋本": "hashimoto", "阿部": "abe",
    "石川": "ishikawa", "前田": "maeda", "藤田": "fujita", "後藤": "goto", "近藤": "kondo",
    "村上": "murakami", "遠藤": "endo", "青木": "aoki", "坂本": "sakamoto", "福田": "fukuda",
    "太田": "ota", "西村": "nishimura", "藤井": "fujii", "岡田": "okada", "長谷川": "hasegawa",
    "原田": "harada", "松田": "matsuda", "石井": "ishii", "中川": "nakagawa", "中野": "nakano",
    "原": "hara", "小川": "ogawa", "竹内": "takeuchi", "金子": "kaneko", "和田": "wada",
    "中山": "nakayama", "石田": "ishida", "上田": "ueda", "森田": "morita", "小野": "ono",
    "柴田": "shibata", "武田": "takeda", "菅原": "sugawara", "横山": "yokoyama", "大野": "ono2",
}
ROMAJI_GIVEN = {
    "花子": "hanako", "太郎": "taro", "美香": "mika", "健": "ken", "葵": "aoi",
    "一郎": "ichiro", "直樹": "naoki", "由美": "yumi", "和也": "kazuya", "恵子": "keiko",
    "亮": "ryo", "美咲": "misaki", "拓也": "takuya", "愛子": "aiko", "大輔": "daisuke",
    "真由美": "mayumi", "翔太": "shota", "沙織": "saori", "健太": "kenta", "麻衣": "mai",
    "勇気": "yuki", "彩": "aya", "海斗": "kaito", "健二": "kenji", "美穂": "miho",
    "隆": "takashi", "由紀": "yuki2", "涼太": "ryota", "千尋": "chihiro",
}

PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県",
    "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県",
]

CITY_BY_PREF = {
    "東京都": ["千代田区", "新宿区", "渋谷区", "港区", "世田谷区"],
    "埼玉県": ["さいたま市", "東松山市", "川口市", "所沢市"],
    "大阪府": ["大阪市", "堺市", "豊中市"],
    "神奈川県": ["横浜市", "川崎市", "藤沢市"],
}
DEFAULT_CITY = "中央区"

RANKS = ["gold", "silver", "bronze"]
AGE_GROUPS = ["10s", "20s", "30s", "40s", "50s", "60s"]
INTEREST_POOL = [
    "travel", "coffee", "gadget", "desk_setup", "keyboard", "food", "drive",
    "office", "chair", "monitor", "fashion", "sports", "book", "music",
    "camera", "cooking", "pet", "game",
]

PRODUCT_CATALOG = [
    ("PC周辺機器", "MOUSE", "マウス", 1500, 4500, ["wireless", "gadget"]),
    ("PC周辺機器", "KEYBOARD", "キーボード", 3000, 15000, ["keyboard", "gadget"]),
    ("PC周辺機器", "MONITOR", "モニター", 15000, 45000, ["monitor", "display", "work"]),
    ("PC周辺機器", "WEBCAM", "Webカメラ", 2000, 8000, ["webcam", "gadget"]),
    ("PC周辺機器", "SPEAKER", "PCスピーカー", 2500, 9000, ["audio", "gadget"]),
    ("アクセサリ", "CABLE", "USBケーブル", 800, 2500, ["usb-c", "mobile", "gadget"]),
    ("アクセサリ", "CASE", "スマホケース", 1000, 3500, ["mobile", "fashion"]),
    ("アクセサリ", "CHARGER", "充電器", 1800, 5500, ["mobile", "gadget"]),
    ("家具", "CHAIR", "オフィスチェア", 12000, 35000, ["chair", "office", "work"]),
    ("家具", "DESK", "デスク", 15000, 40000, ["desk_setup", "work"]),
    ("家具", "SHELF", "本棚", 8000, 20000, ["storage", "work"]),
    ("食品", "COFFEE", "コーヒー豆", 800, 2500, ["coffee", "food"]),
    ("食品", "TEA", "紅茶セット", 1000, 3000, ["food"]),
    ("食品", "SNACK", "お菓子詰め合わせ", 1200, 3500, ["food"]),
    ("家電", "KETTLE", "電気ケトル", 3000, 8000, ["kitchen", "gadget"]),
    ("家電", "FAN", "扇風機", 4000, 12000, ["gadget"]),
    ("日用品", "TOWEL", "タオルセット", 1500, 4000, ["home"]),
    ("文房具", "NOTEBOOK", "ノートセット", 500, 1800, ["office"]),
    ("スポーツ用品", "YOGA_MAT", "ヨガマット", 2000, 6000, ["sports"]),
    ("キッチン用品", "KNIFE", "包丁セット", 3500, 12000, ["kitchen"]),
]

COUPON_POOL = [
    "WELCOME10", "SPRINGSALE", "KEYBOARD500", "FOOD100", "MONITOR1000",
    "COFFEE50", "SUMMER2026", "VIP5", "REPEAT300", "NEWYEAR20",
]

TICKET_LABEL_POOL = [
    "delivery", "question", "payment", "coupon", "gift", "address_change",
    "defect", "return", "cancel", "general",
]

MESSAGE_PAIRS = [
    ("配送日はいつですか？", "明日到着予定です。"),
    ("クーポンは適用されていますか？", "適用されておりますのでご安心ください。"),
    ("商品に不備がありました。", "大変申し訳ございません。交換対応いたします。"),
    ("返品は可能ですか？", "未開封であれば7日以内に返品可能です。"),
    ("支払い方法を変更したいです。", "発送前であれば変更可能です。"),
    ("ギフト包装をお願いできますか？", "承知いたしました。ギフト包装で対応します。"),
    ("住所を変更したいです。", "発送準備前でしたら変更可能です。"),
    ("注文をキャンセルしたいです。", "キャンセル手続きを承りました。"),
]


def esc_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def pg_array(values):
    inner = ",".join(f'"{v}"' for v in values)
    return "{" + inner + "}"


def random_date(start_y, start_m, start_d, end_y, end_m, end_d):
    import datetime
    start = datetime.date(start_y, start_m, start_d)
    end = datetime.date(end_y, end_m, end_d)
    delta = (end - start).days
    return start + datetime.timedelta(days=random.randint(0, delta))


def random_datetime(start, end):
    import datetime
    delta = int((end - start).total_seconds())
    return start + datetime.timedelta(seconds=random.randint(0, delta))


# ---------- customers ----------

def gen_customers(n, start_id):
    rows = []
    used_emails = set()
    for i in range(n):
        cid = start_id + i
        sur = random.choice(SURNAMES)
        giv = random.choice(GIVEN_NAMES)
        name = f"{sur} {giv}"
        email_base = f"{ROMAJI_GIVEN[giv]}.{ROMAJI_SURNAME[sur]}"
        email = f"{email_base}@example.com"
        n2 = 2
        while email in used_emails:
            email = f"{email_base}{n2}@example.com"
            n2 += 1
        used_emails.add(email)
        pref = random.choice(PREFECTURES)
        registered = random_date(2025, 1, 1, 2026, 6, 30)
        phones = [f"0{random.choice([70,80,90])}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
                  for _ in range(random.choice([1, 1, 2]))]
        profile = {
            "rank": random.choice(RANKS),
            "age_group": random.choice(AGE_GROUPS),
            "interests": random.sample(INTEREST_POOL, k=random.choice([1, 2, 3])),
            "notification": {"email": random.choice([True, False]), "sms": random.choice([True, False])},
        }
        rows.append([
            cid, name, email, pref, registered.isoformat(),
            pg_array(phones), esc_json(profile),
        ])
    return rows


# ---------- products ----------

def gen_products(n, start_id):
    rows = []
    used_skus = set()
    for i in range(n):
        pid = start_id + i
        category, code_prefix, base_name, lo, hi, tag_pool = random.choice(PRODUCT_CATALOG)
        sku = f"{code_prefix}-{pid:03d}"
        while sku in used_skus:
            pid += 1000
            sku = f"{code_prefix}-{pid:03d}"
        used_skus.add(sku)
        product_name = f"{base_name}タイプ{random.choice(['A','B','C','Pro','Lite'])}"
        price = random.randrange(lo, hi, 100)
        is_active = random.random() > 0.08
        tags = list(dict.fromkeys(tag_pool + random.sample(INTEREST_POOL, k=1)))
        specs = {
            "color": random.choice(["black", "white", "gray", "navy"]),
            "warranty_months": random.choice([0, 6, 12, 24, 36]),
            "weight_g": random.randint(50, 5000),
        }
        if not is_active:
            specs["reason_inactive"] = random.choice(["discontinued", "out_of_stock", "recalled"])
        rows.append([
            pid, sku, product_name, category, price,
            "true" if is_active else "false",
            pg_array(tags), esc_json(specs),
        ])
    return rows


# ---------- orders ----------

def gen_orders(n, start_id, customer_ids):
    import datetime
    rows = []
    order_date_start = datetime.datetime(2025, 4, 10, 0, 0, 0)
    order_date_end = datetime.datetime(2026, 6, 30, 23, 59, 59)
    for i in range(n):
        oid = start_id + i
        cid = random.choice(customer_ids)
        order_dt = random_datetime(order_date_start, order_date_end)
        status = random.choices(
            ["shipped", "pending", "canceled"], weights=[65, 20, 15], k=1
        )[0]
        payment = random.choice(["card", "bank", "convenience"])
        coupons = random.sample(COUPON_POOL, k=random.choice([0, 0, 1, 1, 2]))
        pref = random.choice(PREFECTURES)
        city = random.choice(CITY_BY_PREF.get(pref, [DEFAULT_CITY]))
        delivery = {
            "zip": f"{random.randint(100,999)}-{random.randint(1000,9999)}",
            "prefecture": pref,
            "city": city,
            "is_remote_area": random.random() < 0.05,
        }
        note = {
            "gift": random.random() < 0.3,
            "source": random.choice(["web", "app"]),
        }
        if status == "canceled":
            note["cancel_reason"] = random.choice(
                ["customer_request", "out_of_stock", "payment_failed"]
            )
        rows.append([
            oid, cid, order_dt.strftime("%Y-%m-%d %H:%M:%S"), status, payment,
            pg_array(coupons), esc_json(delivery), esc_json(note),
        ])
    return rows


# ---------- order_items ----------

def gen_order_items(start_id, order_rows, product_catalog_rows):
    rows = []
    next_id = start_id
    products = [(int(r[0]), int(r[4])) for r in product_catalog_rows]  # (product_id, price)
    for order_row in order_rows:
        order_id = order_row[0]
        num_items = random.choice([1, 1, 2, 2, 3])
        chosen = random.sample(products, k=min(num_items, len(products)))
        for product_id, price in chosen:
            quantity = random.randint(1, 5)
            options = {"gift_wrap": random.random() < 0.25}
            extra_key = random.choice(["color", "length_m", "switch", "grind", None])
            if extra_key == "color":
                options["color"] = random.choice(["black", "white", "gray"])
            elif extra_key == "length_m":
                options["length_m"] = random.choice([1.0, 1.5, 2.0])
            elif extra_key == "switch":
                options["switch"] = random.choice(["red", "brown", "blue"])
            elif extra_key == "grind":
                options["grind"] = random.choice(["beans", "fine", "medium"])
            rows.append([
                next_id, order_id, product_id, quantity, price, esc_json(options),
            ])
            next_id += 1
    return rows


# ---------- support_tickets ----------

def gen_support_tickets(n, start_id, customer_order_map):
    import datetime
    rows = []
    customer_ids = list(customer_order_map.keys())
    for i in range(n):
        tid = start_id + i
        cid = random.choice(customer_ids)
        orders_for_customer = customer_order_map[cid]
        if orders_for_customer and random.random() < 0.7:
            order_id = random.choice(orders_for_customer)
            order_id_str = str(order_id)
        else:
            order_id_str = ""  # NULL
        created = random_datetime(
            datetime.datetime(2025, 4, 10, 0, 0, 0),
            datetime.datetime(2026, 7, 3, 23, 59, 59),
        )
        status = random.choices(["open", "closed"], weights=[35, 65], k=1)[0]
        labels = random.sample(TICKET_LABEL_POOL, k=random.choice([1, 2]))
        num_messages = random.choice([1, 1, 2, 2, 3])
        cust_msg, support_msg = random.choice(MESSAGE_PAIRS)
        messages = []
        t = created
        messages.append({"sender": "customer", "message": cust_msg, "sent_at": t.strftime("%Y-%m-%d %H:%M:%S")})
        if num_messages >= 2:
            t = t + datetime.timedelta(minutes=random.randint(5, 120))
            messages.append({"sender": "support", "message": support_msg, "sent_at": t.strftime("%Y-%m-%d %H:%M:%S")})
        if num_messages >= 3:
            t = t + datetime.timedelta(minutes=random.randint(5, 120))
            messages.append({"sender": "customer", "message": "ありがとうございます、承知しました。", "sent_at": t.strftime("%Y-%m-%d %H:%M:%S")})
        rows.append([
            tid, cid, order_id_str, created.strftime("%Y-%m-%d %H:%M:%S"), status,
            pg_array(labels), esc_json(messages),
        ])
    return rows


def read_existing(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    cust_header, cust_rows = read_existing(CSV_DIR / "customers.csv")
    prod_header, prod_rows = read_existing(CSV_DIR / "products.csv")
    ord_header, ord_rows = read_existing(CSV_DIR / "orders.csv")
    item_header, item_rows = read_existing(CSV_DIR / "order_items.csv")
    tick_header, tick_rows = read_existing(CSV_DIR / "support_tickets.csv")

    next_customer_id = max(int(r[0]) for r in cust_rows) + 1
    next_product_id = max(int(r[0]) for r in prod_rows) + 1
    next_order_id = max(int(r[0]) for r in ord_rows) + 1
    next_item_id = max(int(r[0]) for r in item_rows) + 1
    next_ticket_id = max(int(r[0]) for r in tick_rows) + 1

    new_customers = gen_customers(54, next_customer_id)
    new_products = gen_products(53, next_product_id)

    all_customer_ids = [int(r[0]) for r in cust_rows] + [r[0] for r in new_customers]
    all_product_rows = prod_rows + new_products

    new_orders = gen_orders(52, next_order_id, all_customer_ids)
    new_items = gen_order_items(next_item_id, new_orders, all_product_rows)

    all_orders_for_map = ord_rows + new_orders
    customer_order_map = {}
    for r in all_orders_for_map:
        cid = int(r[1])
        customer_order_map.setdefault(cid, []).append(int(r[0]))
    for cid in all_customer_ids:
        customer_order_map.setdefault(cid, [])

    new_tickets = gen_support_tickets(50, next_ticket_id, customer_order_map)

    write_csv(CSV_DIR / "customers.csv", cust_header, cust_rows + new_customers)
    write_csv(CSV_DIR / "products.csv", prod_header, prod_rows + new_products)
    write_csv(CSV_DIR / "orders.csv", ord_header, ord_rows + new_orders)
    write_csv(CSV_DIR / "order_items.csv", item_header, item_rows + new_items)
    write_csv(CSV_DIR / "support_tickets.csv", tick_header, tick_rows + new_tickets)

    print(f"customers: {len(cust_rows) + len(new_customers)}")
    print(f"products: {len(prod_rows) + len(new_products)}")
    print(f"orders: {len(ord_rows) + len(new_orders)}")
    print(f"order_items: {len(item_rows) + len(new_items)}")
    print(f"support_tickets: {len(tick_rows) + len(new_tickets)}")


if __name__ == "__main__":
    main()
