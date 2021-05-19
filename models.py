from peewee import *
import datetime

DATABASE = SqliteDatabase('wardrobe.sqlite')


class User(Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE


class Item(Model):
    name=CharField()
    price=DecimalField(decimal_places=2)
    user_id=ForeignKeyField(User, backref='user_items')
    url=CharField()
    is_purchased=BooleanField(default=False)
    created_at: DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Category(Model):
    name=CharField()
    item_id=ForeignKeyField(Item, backref='item_categories')

    class Meta:
        database = DATABASE


class Outfit(Model):
    name=CharField()
    date=DateField()
    item_id=ForeignKeyField(Item, backref='item_outfits')

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Item, Category, Outfit], safe=True)
    print("Connected to the DB and created tables if not exist")
    DATABASE.close()
