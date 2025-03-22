from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

engine = create_engine("sqlite:///my_database.db")


metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

metadata.create_all(engine)


ins = users.insert().values(id=1, name="John Doe")
conn = engine.connect()
result = conn.execute(ins)
conn.close()


s = select(users)
conn = engine.connect()
result = conn.execute(s)
for row in result:
    print(row)
conn.close()


s = select(users).where(users.c.name == "John Doe")
conn = engine.connect()
result = conn.execute(s)
for row in result:
    print(row)
conn.close()
