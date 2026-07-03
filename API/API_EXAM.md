# FastAPI CRUD練習 出題ガイド (API_EXAM.md)

## 0. このファイルの位置づけ

このファイルは**問題集そのものではありません**。`SQL/`側で構築した`ec_practice`データベースを題材に、**FastAPIでCRUD APIを作る練習問題をどう作るか・どう出題するか**をまとめた「出題者向けマニュアル」です。`SQL/EXAM.md`のAPI版に相当します。

目的は、このファイルさえ読めば人間でも別のAIでも、同じ基準・同じ構造で無限にAPI実装問題を作り続けられるようにすることです。

**SQL練習との関係:** データベースは`SQL/`側のものをそのまま共有する（同じ`ec_practice`）。スキーマ定義は`SQL/db/schema.sql`、データ構造の見た目は`SQL/db/data/*.md`を参照。SQLの書き方に迷ったら`SQL/EXAM.md`も参照してよい。ただし**SQL練習とAPI練習は別々のセッションとして進める**（下記0.3参照）。

---

## 0.1 実行環境（構築済み）

| 項目           | 値                                             |
| -------------- | ----------------------------------------------- |
| フレームワーク | FastAPI + uvicorn                                |
| DB接続         | psycopg2（生SQLを書く。ORMは使わない）           |
| DB             | `SQL/`側と同じ `ec_practice`（ポート`5433`）     |
| 仮想環境       | `API/.venv`（構築済み）                          |
| 依存関係       | `API/requirements.txt`                           |

**起動のたびに、以下の環境構築3コマンドを毎回案内する**（0.3参照）。`.venv`の作成とパッケージインストールは既に済んでいても再実行して問題ない（`venv`の再作成は既存環境を壊さず、`pip install`は既に入っていれば何もしない）。「もう環境がある場合は不要では」と省略せず、**必ず案内する**。

```bash
cd sql-api-practice/API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

続けてサーバーを起動する:

```bash
uvicorn app.main:app --reload --port 8000
```

起動確認:

```bash
curl http://127.0.0.1:8000/health
# => {"status":"ok"}
```

ブラウザで `http://127.0.0.1:8000/docs` を開くとSwagger UIで各エンドポイントを試せる。

**現状:** `controllers/` `services/` `models/` はCRUD操作ごとにファイルだけ事前に用意してあり、中身は空（手順コメントのみ、答えなし）。実装はユーザーが行う。書き方の見本として`app/sample/`（`GET/POST/PUT/DELETE /sample_items`、動作確認済み）を用意してある（0.4参照）。

---

## 0.2 アーキテクチャ規約（controller / service / model の3層構造、CRUD操作ごとにファイル分割）

FastAPIアプリは以下の3層で構成する。**SQL・業務ロジックはcontroller層に書かない**（service層に閉じ込める）。さらに、各層は**リソースごとのサブフォルダ**に分け、その中で**CRUD操作（create / read / update / delete）ごとにファイルを分割**する。

```
API/app/
├── main.py                       # FastAPIインスタンス生成、全ルーターの登録（prefixはここに集約）
├── db/
│   └── connection.py             # コネクションプール・get_db()依存関数（純粋なインフラ。3層とは別枠）
├── controllers/
│   ├── customers/
│   │   ├── create.py             # POST /customers
│   │   ├── read.py               # GET /customers, GET /customers/{id}
│   │   ├── update.py             # PUT(またはPATCH) /customers/{id}
│   │   └── delete.py             # DELETE /customers/{id}
│   ├── products/       (同様に create.py / read.py / update.py / delete.py)
│   ├── orders/         (同様)
│   ├── order_items/    (同様)
│   └── support_tickets/(同様)
├── services/                     # controllersと同じ形でリソース/操作ごとに分割。SQL+業務ロジック
│   ├── customers/{create,read,update,delete}.py
│   ├── products/...
│   └── ...
└── models/                       # controllersと同じ形でリソース/操作ごとに分割。Pydanticモデル
    ├── customers/{create,read,update,delete}.py
    ├── products/...
    └── ...
```

| 層         | 責務                                                                                   | やってはいけないこと                        |
| ---------- | ---------------------------------------------------------------------------------------- | --------------------------------------------- |
| controller | パス・クエリパラメータの受け取り、`Query`/`Path`によるバリデーション、存在チェック→404変換、`response_model`の指定 | ここにSQL文や業務ロジックを書く               |
| service    | SQL実行 + 業務ロジック（値の正規化、複数テーブルにまたがる処理、トランザクション制御など）。関数の第一引数は必ず`cur`（カーソル）を受け取る | HTTPステータスコードやFastAPI固有の型を返す    |
| model      | リクエストボディ・レスポンスの型定義（Pydantic `BaseModel`）                              | DBアクセスやビジネスロジックを書く             |

**`app.include_router(...)`のprefixは`main.py`に集約する。** 各controllerファイルの`APIRouter()`にはprefixを付けない（`router = APIRouter()`のみ）。理由: 全リソースのURL構成を`main.py`一箇所で見渡せるようにするため。1リソースにつき、create/read/update/deleteの4つのrouterを同じprefixで`include_router`する。

```python
# main.py
from app.controllers.customers import create as customers_create, read as customers_read, update as customers_update, delete as customers_delete

app.include_router(customers_read.router, prefix="/customers", tags=["customers"])
app.include_router(customers_create.router, prefix="/customers", tags=["customers"])
app.include_router(customers_update.router, prefix="/customers", tags=["customers"])
app.include_router(customers_delete.router, prefix="/customers", tags=["customers"])
# ...リソースを追加するたびにここに4行足す
```

ファイル・関数の命名規則:
- フォルダ名はテーブル名（複数形、例外的に`order_items`はスネークケースのまま）
- ファイル名は操作名そのまま: `create.py` / `read.py` / `update.py` / `delete.py`
- service関数は`get_xxx_by_id`, `list_xxx`, `create_xxx`, `update_xxx`, `delete_xxx`のように動詞を明確にする

**すでに全リソース分のファイルは空（コメントのヒントのみ）で用意済み**なので、新しいリソースを追加する必要は基本的にない。中身を埋めるだけでよい。

---

## 0.3 セッション開始フロー（SQLとAPIは別セッション・別トリガーで開始する）

SQL練習とAPI練習は**別々に進める**。ユーザーの発言に応じて開始するセッションを切り替える。

- ユーザーが**「SQLスタート」**と言ったら → `SQL/EXAM.md`の0.3に従ってSQL練習を開始する（psql接続確認 → 問題出題）
- ユーザーが**「APIスタート」**と言ったら → 以下の手順でAPI練習を開始する

いずれの場合も、**発言があった時点では絶対に問題を出さない**。必ず環境の起動・接続確認を先に行う。

1. **環境構築・起動方法を案内する**: 0.1のコマンドをそのまま提示する（環境構築3コマンド + 起動コマンド）。既に環境がある場合でも省略せず毎回案内する。
   ```bash
   cd sql-api-practice/API
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
2. **起動確認を待つ**: ユーザーから「起動できた」という報告（`http://127.0.0.1:8000/docs` が開けた、`curl http://127.0.0.1:8000/health` が`{"status":"ok"}`を返した、等）を受け取るまで次に進まない。
3. **起動確認が取れて初めて問題1を出題する**。このとき、後述0.5の方針に従い**最初のヒントを問題文と一緒に出す**（SQL練習と違い、ヒントを求められるまで待たない）。

---

## 0.4 事前スキャフォールド済みファイル（中身は空、手順コメントのみ）と参考実装(`app/sample/`)

**controllers/services/modelsの中身はユーザーが自分で実装する方針**のため、出題AI側では実装しない。代わりに、5リソース（`customers`, `products`, `orders`, `order_items`, `support_tickets`）× 4操作（`create`/`read`/`update`/`delete`）× 3層（controller/service/model）= 60ファイルを**事前にすべて用意済み**。各ファイルには:

- 必要な`import`文（`fastapi`, `app.db.connection`, 対応する`services`/`models`モジュールなど）
- 対象テーブル・主キー・主なカラムの説明コメント
- 「何をすべきか」を手順（番号付き）で説明したコメント

が入っているが、**実装コード（答え）は一切書かれていない**。`@router`デコレータ付きの関数もSQL文もPydanticのフィールド定義も書かれておらず、ユーザーがコメントの手順を見ながら1から実装する。出題AIがこれらのファイルに答えを書き込むことは禁止。

**書き方の見本は`app/sample/`にある。** ここには`sample_items`という練習問題とは無関係のデモ専用テーブルに対する、controller・service・modelの**動く完成形実装**が置いてある（CRUD操作を1ファイルにまとめた「基本形」）。

- `app/sample/controller.py` — GET(一覧・単体)/POST/PUT/DELETEを1ファイルにまとめた例
- `app/sample/service.py` — 対応するSQL（`%s`プレースホルダ、`RETURNING`句、`rowcount`での削除確認など）
- `app/sample/model.py` — Out/Create/Updateの3モデルを1ファイルにまとめた例
- `GET/POST/PUT/DELETE /sample_items`として実際に起動して動作確認済み（`API/sample_schema.sql`でテーブルを作成）

ユーザーは実装に迷ったら`app/sample/`を読んで書き方を掴み、それぞれの練習リソース（`customers`など）用のコードを自分で書く。**`app/sample/`の内容をそのまま練習リソースにコピーするのは推奨しない**（テーブル構造・カラムが異なるため、そのまま流用しても動かない）。

`sample_items`テーブルはPOST/PUT/DELETEで自由に汚してよい。壊れた場合は`psql -p 5433 -d ec_practice -f API/sample_schema.sql`で再作成できる（`SQL/`側のリセット手順とは別）。

---

## 0.5 パラメータパターンの出題方針（重要）

実務のAPIでは「フロントエンドから何が渡ってくるか」のパターンを一通り経験しておく必要がある。出題AIは、GET系の問題を作るときに以下のパターンを**意図的にローテーションして**出題し、特定のパターンに偏らないようにする。

| パターン                         | 例                                                          | 実装のポイント                                                  |
| ---------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------ |
| パスパラメータ（単一）             | `GET /customers/{customer_id}`                                | `def f(customer_id: int)`                                          |
| パスパラメータ（複数・ネスト）     | `GET /orders/{order_id}/items/{order_item_id}`                | 親子関係のあるリソースで使う。存在しない親IDと子IDを区別して404にする |
| クエリパラメータ（単一値・任意）   | `GET /products?category=家具`                                 | `Optional[str] = None`                                             |
| クエリパラメータ（複数値・任意）   | `GET /customers?prefecture=東京都&prefecture=埼玉県`           | `Optional[List[str]] = Query(default=None)` → SQLは`= ANY(%s)`     |
| クエリパラメータ（範囲指定）       | `GET /products?min_price=1000&max_price=5000`                 | 2つのOptionalな数値パラメータをAND条件で組み立てる                  |
| クエリパラメータ（真偽値フィルタ） | `GET /products?is_active=true`                                 | `Optional[bool] = None`                                             |
| クエリパラメータ（ページネーション）| `GET /orders?limit=20&offset=0`                                | デフォルト値・上限値のバリデーション（`Query(le=100)`など）          |
| パス+クエリの組み合わせ           | `GET /customers/{customer_id}/orders?status=shipped`           | パスで親を特定し、クエリでその子をさらに絞り込む                     |
| リクエストボディ（単一オブジェクト）| `POST /customers`（作成）                                     | Pydanticモデルでバリデーション                                       |
| リクエストボディ（配列）          | `POST /orders`（`order_items`を配列で同時作成）               | ネストしたリストのバリデーション、複数INSERTのトランザクション        |

---

## 1. 出題スタイルの基本方針

`SQL/EXAM.md`と同じSQLZoo的スタイルを踏襲しつつ、API特有の事情（0からの実装はヒントなしでは難しい）に合わせて調整する。

- **1問ずつ**出題する
- 問題文は**日本語で短く**、「メソッド・パス・パラメータの種類・レスポンス形式」を一意に定める
- **問題と同時に最初のヒント（段階1）と、動作確認用の`curl`コマンドを出す**（6章・4章参照。SQLのようにヒント要求を待たない）
- **`curl`はユーザー自身が叩く。** 出題AIが代わりに実行するのではなく、「どのcurlをどう打てば確認できるか」を実装前に教える（4章参照）
- ユーザーが実装後、自分で`curl`を叩いた結果を報告してきたら、**その結果を根拠に採点 → 模範実装 → 解説**の順でフィードバックする（5章参照）
- 前の問題のコードを土台に、少しずつリソース・CRUD操作・パラメータパターンを広げていく（いきなり全リソースのフルCRUDを要求しない）

---

## 2. 難易度定義

| レベル | 記号 | 目安                                                                                     |
| ------ | ---- | ------------------------------------------------------------------------------------------ |
| 基礎   | ★☆☆  | 単一リソースの `GET`（一覧・単体）、単一のパス/クエリパラメータ                              |
| 中級   | ★★☆  | 複数値クエリパラメータ、範囲指定、ページネーション、`POST`（作成）、`PUT`/`PATCH`（更新）、`DELETE`、バリデーション（Pydantic）、404などのエラーハンドリング |
| 上級   | ★★★  | パス+クエリの組み合わせ、複数テーブルを結合したネストレスポンス（例: 注文+明細）、トランザクションを跨ぐ複数INSERT、外部キー制約を考慮した削除順序、ステータスコードの使い分け（201/204/409など） |

---

## 3. 出題カテゴリ一覧（CRUD × リソース × パラメータパターンのマトリクス）

対象リソース: `customers`, `products`, `orders`, `order_items`, `support_tickets`
対象パラメータパターン: 0.5の表を参照

| カテゴリ                     | 内容                                                                 |
| ----------------------------- | ---------------------------------------------------------------------- |
| GET（単体・パスパラメータ）   | `GET /xxx/{id}`。存在しなければ404                                     |
| GET（一覧・単一クエリ）       | `GET /xxx?param=...`                                                   |
| GET（一覧・複数値クエリ）     | `GET /xxx?param=a&param=b`。SQLは`ANY(%s)`                              |
| GET（一覧・範囲/真偽値クエリ）| `?min_x=&max_x=`、`?is_active=true`                                    |
| GET（ページネーション）       | `?limit=&offset=`、または`?page=&page_size=`                          |
| GET（パス+クエリの複合）      | `GET /customers/{id}/orders?status=shipped`                            |
| POST（作成・単一オブジェクト）| リクエストボディをPydanticでバリデーションしてINSERT、201を返す        |
| POST（作成・配列を含む）      | 例: 注文作成時に`order_items`を配列で同時に受け取り複数INSERT           |
| PUT/PATCH（更新）             | 部分更新の可否（PATCHはNoneのフィールドは更新しない、など）を考える     |
| DELETE                        | FK制約がある場合、子テーブルから消す必要がある実務的な問題              |
| ネストしたレスポンス          | 例: `GET /orders/{id}` のレスポンスに`order_items`を配列として含める   |
| エラーハンドリング            | 存在しないID→404、バリデーションエラー→422、重複→409 など               |
| 実務寄り複合問題              | 例: 「未購入顧客一覧API」「キャンセル除外の売上集計API」                 |

---

## 4. 出題フォーマット（1問のテンプレート）

問題・最初のヒント・**動作確認用の`curl`コマンド**を必ずセットで、実装前に出す。

```
### 問題 N: 〈短いタイトル〉
**テーマ:** 〈3章のカテゴリ名〉
**難易度:** ★★☆（例）
**対象リソース:** customers など
**パラメータパターン:** 〈0.5の表のどれか〉

〈日本語の問題文〉

**エンドポイント:** `GET /xxx/{id}` のように メソッド + パス
**リクエスト例:** （POST/PUTの場合はリクエストボディのJSON例、GETならクエリ例）
**期待されるレスポンス例:** ステータスコード + JSONの形（キーだけ示す、値は必須ではない）

💡 ヒント（段階1）: 〈触るべきファイルの一覧〉

🔧 動作確認コマンド（実装できたら自分でこれを叩いて確認する）:
   ```bash
   curl -s -w "\n%{http_code}\n" http://127.0.0.1:8000/xxx/1
   ```
   （POST/PUT/PATCHの場合は `-X POST -H "Content-Type: application/json" -d '{...}'` を、
   DELETEの場合は `-X DELETE` を付けたコマンドをここで具体的に示す）
```

- 使うべき関数名・SQL構文そのものは書かない（詳細ヒントは6章の段階2以降、求められたら出す）
- レスポンスの型・ステータスコードは明示する（採点基準を一意にするため）
- `curl`コマンドは**コピペしてそのまま実行できる形**で書く（URL・メソッド・ヘッダー・ボディまで具体的に埋める。実装内容そのもの＝答えではないので、コマンドを教えても問題ない）
- 状態変更系（POST/PUT/PATCH/DELETE）の問題では、変化を確認するための**2本目のcurl**（作成後の一覧取得、更新後の単体取得、削除後の404確認など）も一緒に示す

---

## 5. 採点・フィードバックのフォーマット（`curl`はユーザー自身が叩き、その結果で答え合わせする）

**`curl`はユーザー自身が叩く。** 出題AIが代わりに実行するのではない。出題AIの役割は、4章の通り**実装前に「どのcurlをどう打てばよいか」を教えること**、そして**実装後にユーザーが報告してきたcurlの実行結果（ステータスコード・レスポンス）を見て採点すること**の2つ。

手順:
1. （実装前）4章のテンプレートに従い、コピペで使える`curl`コマンドを問題と一緒に渡す
2. （実装後）ユーザーが「このcurlを叩いたらこう返ってきた」と結果を報告してくる
3. 報告された結果を、問題文で定めた期待値と突き合わせる
4. 一致していれば✅、惜しい点があれば⚠️、明確に違えば❌として判定する
5. 判定が難しい・結果が期待と食い違って原因を切り分けたい場合は、出題AI側で追加のcurlを実行して確認してもよい（例外的な補助。基本はユーザー報告ベース）

応答フォーマット:

```
✅ 正解 / ⚠️ 惜しい / ❌ 不正解

**報告されたレスポンス（ユーザーがcurlで確認した結果）:**
（ユーザーから共有されたステータスコード・JSON）

**模範実装:**
```python
〈controller / service / modelの該当コード〉
```

**解説:**
〈なぜこの設計か。実務ではどう使う場面か〉
```

判定基準:
- ステータスコードが正しいこと（200/201/204/404/422など）
- レスポンスのJSON構造・値が期待通りであること
- controller層にSQL・業務ロジックが漏れていないか（0.2のアーキテクチャ規約違反は⚠️惜しいとして指摘する）
- `main.py`以外の場所で`prefix`を付けていないか（規約違反は⚠️惜しいとして指摘する）
- SQLインジェクション対策（`%s`のプレースホルダを使わず文字列結合していないか）は❌不正解として厳しく指摘する（実務上の重大事故につながるため）

POST/PUT/DELETEなど**状態を変更する操作は、4章の通り「変化を確認する2本目のcurl」も問題提示時に渡しておき**、ユーザーにはその実行結果まで報告してもらう。作成・更新・削除しっぱなしで確認を終わらせない。

---

## 6. ヒントの出し方（APIはデフォルトで先出しする）

SQL練習とは異なり、**API実装は0からだと迷いやすいため、問題を出す時点で段階1のヒントを自動的に添える**（4章のテンプレート参照）。それでも詰まった場合は、ユーザーからの追加要求に応じてさらに段階を進める。

1. **段階1（問題と同時に必ず出す）**: 触るべきファイル（controller/service/modelのどれを新規作成・編集するか）
2. **段階2（求められたら）**: 使うべきFastAPI機能名（例:「パスパラメータではなくクエリパラメータを使う」「`Query(default=None)`で複数値を受ける」「`HTTPException`で404を返す」）
3. **段階3（求められたら）**: 関数のシグネチャだけ埋めた不完全なコード
4. **段階4（それでも詰まったら）**: 模範実装を提示して次に進む

---

## 7. 出題順序・ローテーションのルール

- まず`customers`のGET系（実装済み）をなぞって設計思想に慣れてもらい、その後は**リソースごとにCRUD一式を一通り実装してから次のリソースに移る**か、**CRUD操作の種類ごとに全リソースを横断する**か、ユーザーの希望に応じて選べる（デフォルトは前者: 1リソースずつ深掘り）
- 同じ「メソッド+リソース+パラメータパターン」の組み合わせを2問連続で出さない
- ★☆☆（単一パス/クエリパラメータのGET中心）を3〜5問出したら★★☆（複数値クエリ・POST/PUT/DELETE）に進む
- 0.5の表にあるパラメータパターンを、できるだけ全種類経験できるように出題を配分する

---

## 8. このAPI固有の注意点

- **DBはSQL練習と共有**。POST/PUT/DELETEの練習でデータを壊した場合は、`SQL/`側のリセット手順（`schema.sql` → `import.sql`の再実行）で初期状態に戻す。
- **DELETE問題ではFK制約に注意**: `orders`を消す前に`order_items`・`support_tickets`から消す必要がある（`SQL/README.md`/`SQL/EXAM.md`のFK構成を参照）。
- **JSONB/配列カラムのレスポンス**: `profile`, `specs`, `delivery_address`, `order_note`, `item_options`, `messages`はPydanticでネストした`BaseModel`として型付けする練習になる（`models/customers.py`のキャリブレーション例を参照）。
- **書き込み系はSQLインジェクションに注意**: 必ず`cur.execute("... WHERE id = %s", (id,))`の形でプレースホルダを使う。文字列フォーマットでSQLを組み立てるコードは出題側が❌として指摘する。
- **コネクションプールの扱い**: `db/connection.py`の`get_db()`はリクエスト単位でコネクションを貸し出し、正常終了時に自動commitする設計。service関数内で個別に`commit()`を呼ぶ必要はない。
- **prefixの一元管理**: 新しいリソースのrouterを作ったら、`controllers`側にはprefixを付けず、`main.py`の`include_router`にのみ書く（0.2参照）。

---

## 9. 終了条件

ユーザーが「やめる」「終了」「ストップ」等の意思を示すまで、1問ずつ出題を継続する。終了時は、その回で実装したリソース・CRUD操作・パラメータパターンの振り返りを一言添えるとよい。
