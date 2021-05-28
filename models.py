from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('wardrobe.sqlite')
# DATABASE = PostgresqlDatabase('wardrobe', user='postgres')


class User_Account(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE


class Category(Model):
    name=CharField()

    class Meta:
        database = DATABASE


class Item(Model):
    name=CharField()
    price=DecimalField(decimal_places=2)
    user_id=ForeignKeyField(User_Account, backref='user_items')
    category_id=ForeignKeyField(Category, backref='category_items')
    imageUrl=CharField()
    itemInStoreUrl=CharField()
    brand=CharField()
    is_purchased=BooleanField(default=False)
    created_at: DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Outfit(Model):
    name=CharField()
    date=DateField()
    user_id=ForeignKeyField(User_Account, backref='user_outfits')

    class Meta:
        database = DATABASE


class Outfit_Collection(Model):
    item_id=ForeignKeyField(Item, backref='item_outfits')
    outfit_id=ForeignKeyField(Outfit, backref='outfit_items')
    coordinateX=IntegerField()
    coordinateY=IntegerField()
    image_width=IntegerField()
    image_height=IntegerField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User_Account, Item, Category, Outfit, Outfit_Collection], safe=True)
    print("Connected to the DB and created tables if not exist")
    DATABASE.close()
