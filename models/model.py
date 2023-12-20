# models/model.py
from sqlalchemy import MetaData, Table, Column, Integer, String, Float

metadata = MetaData()

lenses = Table(
    "lenses", metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String(50)),
    Column("coating", String(50)),
    Column("stock", Integer),
    Column("selling_price", Float),
    Column("cost", Float)
)

frames = Table(
    "frames", metadata,
    Column("id", Integer, primary_key=True),
    Column("frame", String(50)),
    Column("brand", String(50)),
    Column("size", String(50)),
    Column("stock", Integer),
    Column("model", String(50)),
    Column("color", String(50)),
    Column("selling_price", Float),
    Column("wholesale_price", Float)
)
