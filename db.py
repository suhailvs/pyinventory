# https://github.com/coleifer/peewee
from modules.peewee import *
db = SqliteDatabase('db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = db

class Inventory_Invoice(BaseModel):
    customer = CharField()
    date = DateTimeField()
    amount = IntegerField()                 

class Inventory_Product(BaseModel): 
    name = CharField()
    description = CharField()
    price = IntegerField(default=0)

class Inventory_InvoiceItem(BaseModel):
    invoice = ForeignKeyField(Inventory_Invoice,backref='invoice_invoiceitems')
    product = ForeignKeyField(Inventory_Product,backref='product_invoiceitems')
    quantity = IntegerField()

"""
Usage:
======

delete
------
item = Product.get(Product.id == self.mlb.item_selected[1])
item.delete_instance()

query
-----
p = Product.select()
p = Product.select().where(Product.name.contains(fnd)
p = Product.select().where(Product.name.contains(val)).order_by(Product.name)

items = InvoiceItem.select().where(InvoiceItem.invoice == 1)
for i in items: print (i.quantity,i.product.price)
            
create
------
cur_inv = Invoice.create(customer=inv[0],date=inv[1],amount=inv[2])
InvoiceItem.insert(invoice=cur_inv,product=i[0],quantity=i[1]).execute()

"""