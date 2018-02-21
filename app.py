# pip install redis
# pip install flask

import time
import redis

from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379) # 'redis' is the hostname of the redis container on the application's network.
                                             # docker inspect testapp_redis_1 
                                             #  Networks 
                                             #      Aliases

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) # bind to 0.0.0.0 (machine/container's IP) -- so that it can be accessed from outside
                                        # if localhost, it can only be accessed from within the machine/container
                                        # default port is 5000
