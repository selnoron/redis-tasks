# redis
import redis
from redis import StrictRedis
# json
import pickle
# time
import time
# Flask
import flask
# requests
import requests
from requests.models import Response


app: flask.app.Flask = flask.Flask(__name__)
cards: list[dict] = []
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)

@app.route('/' , methods=['GET', 'POST'])
def main_page() -> dict:
    if flask.request.method == 'POST':
        id: str = flask.request.form.get('card')
        if not r.get(f'{id}'):
            card = pickle.dumps(cards[int(id)])
            r.set(f'{id}', card)
            return r.get(f'{id}')
        else:
            return r.get(f'{id}')
    
    return flask.render_template(
        'index.html'
    )

if __name__ == '__main__':
    URL: str = (
        'https://api.hearthstonejson.com/'
        'v1/121569/ruRU/cards.collectible.json'
    )
    response: Response =\
        requests.get(URL)
    data: list[dict] = response.json()
    for card in data:
        cards.append(card)
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )