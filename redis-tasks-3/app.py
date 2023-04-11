from flask import Flask
import redis

app = Flask(__name__)

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)

@app.route('/')
def index():
    r.set('queue', 'Hello World!')
    return 'Message added to queue.'

def background_task():
    while True:
        message = r.get('queue')
        if message:
            print(message)

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
    background_task()
