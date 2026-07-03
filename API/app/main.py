from fastapi import FastAPI

from app.sample import controller as sample_controller
from app.controllers.customers import create as customers_create
from app.controllers.customers import delete as customers_delete
from app.controllers.customers import read as customers_read
from app.controllers.customers import update as customers_update
from app.controllers.order_items import create as order_items_create
from app.controllers.order_items import delete as order_items_delete
from app.controllers.order_items import read as order_items_read
from app.controllers.order_items import update as order_items_update
from app.controllers.orders import create as orders_create
from app.controllers.orders import delete as orders_delete
from app.controllers.orders import read as orders_read
from app.controllers.orders import update as orders_update
from app.controllers.products import create as products_create
from app.controllers.products import delete as products_delete
from app.controllers.products import read as products_read
from app.controllers.products import update as products_update
from app.controllers.support_tickets import create as support_tickets_create
from app.controllers.support_tickets import delete as support_tickets_delete
from app.controllers.support_tickets import read as support_tickets_read
from app.controllers.support_tickets import update as support_tickets_update

app = FastAPI(title="EC Practice API")

# sample_items: controller/service/modelの基本形を示す参考実装（練習問題の対象ではない）
app.include_router(sample_controller.router, prefix="/sample_items", tags=["sample (reference only)"])

# URLのprefixはここでまとめて管理する（各controllerのrouterにはprefixを付けない）
app.include_router(customers_read.router, prefix="/customers", tags=["customers"])
app.include_router(customers_create.router, prefix="/customers", tags=["customers"])
app.include_router(customers_update.router, prefix="/customers", tags=["customers"])
app.include_router(customers_delete.router, prefix="/customers", tags=["customers"])

app.include_router(products_read.router, prefix="/products", tags=["products"])
app.include_router(products_create.router, prefix="/products", tags=["products"])
app.include_router(products_update.router, prefix="/products", tags=["products"])
app.include_router(products_delete.router, prefix="/products", tags=["products"])

app.include_router(orders_read.router, prefix="/orders", tags=["orders"])
app.include_router(orders_create.router, prefix="/orders", tags=["orders"])
app.include_router(orders_update.router, prefix="/orders", tags=["orders"])
app.include_router(orders_delete.router, prefix="/orders", tags=["orders"])

app.include_router(order_items_read.router, prefix="/order_items", tags=["order_items"])
app.include_router(order_items_create.router, prefix="/order_items", tags=["order_items"])
app.include_router(order_items_update.router, prefix="/order_items", tags=["order_items"])
app.include_router(order_items_delete.router, prefix="/order_items", tags=["order_items"])

app.include_router(support_tickets_read.router, prefix="/support_tickets", tags=["support_tickets"])
app.include_router(support_tickets_create.router, prefix="/support_tickets", tags=["support_tickets"])
app.include_router(support_tickets_update.router, prefix="/support_tickets", tags=["support_tickets"])
app.include_router(support_tickets_delete.router, prefix="/support_tickets", tags=["support_tickets"])


@app.get("/health")
def health():
    return {"status": "ok"}
