import redis

class RedisWrapper(object):

    def __init__(self, host, port=6379, pw=None):
        self.__r = redis.Redis(host=host, port=port, db=0, password=pw)

    def setvalue(self, key, value):
        self.__r.lpush(key, value)

    def getvalue(self, key):
        value = self.__r.rpop(key)
        return value

    def __del__(self):
        self.__r.close()

if __name__ == "__main__":
    r = RedisWrapper('localhost', '6379', 'ycho2020')
    #r.setvalue('foo', 'bar')
    value = r.getvalue('foo')
    print(value)

