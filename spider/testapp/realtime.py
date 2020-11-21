from redis_wrapper import RedisWrapper
import time

def run():
    r = RedisWrapper('localhost', pw='ycho2020')
    while 1:
        if r.getsize('spider_request_queue') > 0:
            queue = r.getvalue('spider_request_queue')
            print(queue)
        time.sleep(0.5)
        print ("waiting...")

if __name__ == "__main__":
    run()

