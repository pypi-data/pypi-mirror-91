# gevent-queue


gevent-queue is a lightweight, stateful multi-producer and multi-consumer queue. It was
designed to work inside gevent-based web apps (especially Flask) so that you only need a
single process. If you later wish to scale, you can easily spawn separate worker
processes.

gevent-queue supports Redis to persist enqueued messages.

## Installing

Install and update using pip:

```sh
pip install -U gevent-queue
```


## Usage Examples


Using workers:

```python
import gevent_queue
import redis

r = redis.Redis()
worker = gevent_queue.Worker(r)

@worker.job
def myjob(arg):
    print("foo", arg)

@worker.schedule("*/2 * * * *")
def every_2_minutes():
    print("bar")

myjob.delay("myarg")

while True:
worker.step()
```
