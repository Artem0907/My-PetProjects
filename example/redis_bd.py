import redis
import asyncio


async def start():
    # Подключение к локальному серверу Redis на стандартном порту
    r = redis.Redis()

    # Подключение к серверу Redis с указанием хоста, порта, пароля и базы данных
    r = redis.Redis(
        host="redis-16497.c83.us-east-1-2.ec2.redns.redis-cloud.com",
        port=16497,
        decode_responses=True,
        username="default",
        password="lArTlQpLpGZTZu2wm4JsXcdHmCbQJ05F",
    )

    # Установка значения ключа
    r.set("name", "John Doe")

    # Получение значения ключа
    name = r.get("name")  # Возвращает b'John Doe' (байтовая строка)

    # Инкремент значения (числового)
    r.incr("counter", 1)

    # Установка значения с истечением срока действия (в секундах)
    r.setex("message", 60, "This message will expire in 60 seconds")

    # Установка значений в хэш
    r.hset("user:1", mapping={"name": "John Doe", "age": 30, "city": "New York"})

    # Получение всех значений хэша
    user_data = r.hgetall("user:1")  # Возвращает словарь байтовых строк

    # Получение значения конкретного поля
    age = r.hget("user:1", "age")  # Возвращает '30'

    # Добавление элементов в список
    r.lpush("my_list", "item1", "item2", "item3")  # Добавляет элементы слева

    # Получение элементов списка
    items = r.lrange("my_list", 0, -1)  # Возвращает все элементы списка

    # Удаление элемента из списка
    r.lrem("my_list", 1, "item2")  # Удаляет одно вхождение 'item2'

    # Добавление элементов в множество
    r.sadd("my_set", "apple", "banana", "cherry")

    # Проверка наличия элемента в множестве
    is_member = r.sismember("my_set", "apple")  # Возвращает True

    # Получение всех элементов множества
    members = r.smembers("my_set")  # Возвращает set([b'apple', b'banana', b'cherry'])

    # Добавление элементов в упорядоченное множество
    r.zadd("my_zset", {"member1": 1, "member2": 2, "member3": 3})

    # Получение элементов с наименьшим рейтингом
    members = r.zrange(
        "my_zset", 0, -1, withscores=True
    )  # Возвращает список кортежей (элемент, рейтинг)

    pipe = r.pipeline()
    pipe.set("key1", "value1")
    pipe.get("key2")
    pipe.hgetall("user:1")
    return pipe.execute()  # Выполняет все команды в одном запросе


print(asyncio.run(start()))
