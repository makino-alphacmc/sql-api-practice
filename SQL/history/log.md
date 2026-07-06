# SQL練習 出題履歴

このファイルは「SQLスタート」で出題した問題を1問ずつ記録するログです。
新しいセッションで「SQLスタート」と言われたら、出題AIはまずこのファイルの末尾（直近の問題）を確認し、
- 直近のテーマ・難易度
- 直近で出したテーマ（連続を避けるため）

を踏まえた上で、少しずつ難易度を上げながら次の問題を出すこと。

記録ルール:
- 問題を出題した時点で1エントリ追加する（結果は「未回答」にしておく）
- ユーザーが回答したら、そのエントリの「結果」を更新する（✅正解 / ⚠️惜しい / ❌不正解）

---

## 2026-07-04 - 問題1
**テーマ:** 基礎SELECT / WHERE / ORDER BY
**難易度:** ★☆☆

`products` テーブルから、`is_active` が true（販売中）かつ `price` が10,000円以上の商品を取得してください。

**出力してほしいカラム:** product_id, product_name, price
**ソート条件:** priceの降順

**結果:** ✅ 正解（1回目はWHERE/ORDER BYを付け忘れて❌、模範解答提示後の2回目で✅）

---

## 2026-07-04 - 問題2
**テーマ:** 基礎SELECT / WHERE / ORDER BY
**難易度:** ★☆☆

`customers` テーブルから、`prefecture` が「東京都」または「埼玉県」の顧客を取得してください。

**出力してほしいカラム:** customer_id, customer_name, prefecture
**ソート条件:** customer_nameの昇順

**結果:** ✅ 正解（1回目はダブルクォート/OR構文のミスで修正、2回目で✅。`IN`も別解として紹介）

---

## 2026-07-04 - 問題3
**テーマ:** JOIN
**難易度:** ★★☆

`orders` テーブルと `customers` テーブルを結合して、注文ごとに顧客名を付けた一覧を取得してください。

**出力してほしいカラム:** order_id, customer_name, order_date, status
**ソート条件:** order_idの昇順

**結果:** ✅ 正解（1回目は`FROM`のカンマ結合と`INNER JOIN`混在・`ON`抜け・`ustomers`タイプミス・`ORDER BY =`でエラー、ヒント→模範解答提示後の再実行で✅）

---

## 2026-07-04 - 問題4
**テーマ:** GROUP BY / 集計
**難易度:** ★★☆

`customers` テーブルと `orders` テーブルを結合し、顧客ごとの注文件数を取得してください。

**出力してほしいカラム:** customer_id, customer_name, order_count（注文件数）
**ソート条件:** order_countの降順

**結果:** ✅ 正解（1回目は`customer_id`が曖昧＋GROUP BYに集計結果を含めるミスで❌、2回目でGROUP BY修正、3〜4回目で`ORDER BY DESC`忘れが続き、5回目で✅）

---

## 2026-07-04 - 問題6
**テーマ:** CASE式
**難易度:** ★★☆

`orders` テーブルから、注文ID・ステータスに加えて、ステータスを日本語表示に変換した列を取得してください（`shipped`→発送済み、`pending`→保留中、`canceled`→キャンセル）。

**出力してほしいカラム:** order_id, status, status_label
**ソート条件:** order_idの昇順

**結果:** ✅ 正解（1回目はFROM抜け・CASEの位置ミス・`ELSE AS`混同・タイプミスで❌、ヒント後の2回目で✅）

---

## 2026-07-05 - 問題7
**テーマ:** 日付操作
**難易度:** ★★☆

`orders` テーブルから、2025年12月に注文された注文を取得してください。

**出力してほしいカラム:** order_id, order_date, status
**ソート条件:** order_idの昇順

**結果:** ✅ 正解（ヒント2段階目の範囲比較を使い、1回目で✅）

---

## 2026-07-05 - 問題8
**テーマ:** サブクエリ / NOT EXISTS / NOT IN
**難易度:** ★★☆

`customers` テーブルから、一度も注文をしたことがない顧客を取得してください。

**出力してほしいカラム:** customer_id, customer_name
**ソート条件:** customer_idの昇順

**結果:** ✅ 正解（1回目は`NOT EXIST`のタイプミス＋`customers.customer.id`のドット過多で❌、ヒント後の2回目で✅）

---

## 2026-07-05 - 問題9
**テーマ:** 配列検索
**難易度:** ★★☆

`orders` テーブルから、クーポンを1つも使っていない（`coupon_codes`が空配列の）注文を取得してください。

**出力してほしいカラム:** order_id, customer_id, coupon_codes
**ソート条件:** order_idの昇順

**結果:** ✅ 正解（1回目は`IS NOT NULL`でNULL判定と空配列判定を混同、模範解答提示後の2回目で✅）

---

## 2026-07-04 - 問題5
**テーマ:** JOIN
**難易度:** ★★☆

`order_items` テーブルと `products` テーブルを結合して、注文明細ごとに商品名を付けた一覧を取得してください。

**出力してほしいカラム:** order_item_id, order_id, product_name, quantity, unit_price
**ソート条件:** order_item_idの昇順

**結果:** ✅ 正解（1回目はJOIN構文のミス「INNER JOIN order_items.product_id」で❌、ヒント後の2回目で✅）

---

## 2026-07-06 - 問題10
**テーマ:** UPDATE
**難易度:** ★★☆

`orders` テーブルで、`order_id` が `1003` の注文の `status` を `'canceled'` に更新してください。

**出力してほしいカラム（更新後の確認用SELECT）:** order_id, status

**結果:** ✅ 正解扱い（SQL自体は正しくWHERE条件も適切だったが、`BEGIN`を使わずオートコミットで実行してしまった。元データがもともと`canceled`だったため実害はなし。トランザクションの使い方を別途解説）

---

## 2026-07-06 - 問題11
**テーマ:** JSONB検索
**難易度:** ★★☆

`customers` テーブルから、`profile`の`age_group`が`'20s'`、かつ`notification`内の`email`がtrueになっている顧客を取得してください。

**出力してほしいカラム:** customer_id, customer_name, age_group, email_notification
**ソート条件:** customer_idの昇順

**結果:** ⚠️ 模範解答提示で終了（全角クォート・WHERE句でのエイリアス使用・SQL実行順の理解でヒント段階4まで進行。最終的にロジック自体は正しかった。次回は「WHEREはSELECTより先に評価される」点と半角クォートの入力に注意）

---

## 2026-07-06 - 問題12
**テーマ:** 実務寄り複合問題（JOIN + 集計 + JSONB）
**難易度:** ★★★

`orders` と `order_items` を結合し、キャンセル済み（`status = 'canceled'`）の注文を除いて、注文メモ（`order_note`）の`source`（流入元）ごとに合計売上金額を集計してください。

**出力してほしいカラム:** source, total_sales
**ソート条件:** total_salesの降順

**結果:** ⚠️ 模範解答提示で終了（ヒント段階1・2を経て、自力での回答提出前に模範解答を要求。上級レベルの複合問題で、JOIN+WHERE除外+JSONB+GROUP BYの組み合わせに慣れる必要あり）
