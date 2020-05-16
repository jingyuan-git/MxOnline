__author__ = 'jingyuan'
__date__ = '2020/5/13 11:48'

import redis, time

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf8", decode_responses=True)

r.set("mobile","123")
r.expire("mobile", 1)
time.sleep(1)
print(r.get("mobile"))