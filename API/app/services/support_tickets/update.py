"""support_tickets更新のservice層。

ここで必要な処理:
1. 更新対象が存在するかどうかを考慮する（存在しない場合はNoneを返し、404判定はcontroller側に任せる）
2. 受け取った値でUPDATE文を組み立てる（%sプレースホルダを使う）
3. 部分更新（PATCH）にする場合、Noneのフィールドは更新対象から除外する方法を考える
   （現在値を取得してマージする、COALESCEを使う、など）
4. 更新後の行をRETURNING句などで取得して返す
"""


def update_support_ticket(cur, ticket_id: int, body):
    ...
