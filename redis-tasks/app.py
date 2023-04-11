# redis
import redis
# time
import time
# Flask
import flask
# local files


app: flask.app.Flask = flask.Flask(__name__)
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)


@app.route('/')
def main_page() -> dict:
    index: float = r.get('index')
    if not index:
        index = 5
        time.sleep(3)
        r.set('index', index)
    index = float(index)
    if index > 2:
        return flask.jsonify({"message": "Accepted"})
    else:
        return flask.jsonify({"message": "Not accepted"})


@app.route('/reg', methods=['GET', 'POST'])
def reg_page() -> dict:
    if flask.request.method == 'POST':
        login: str = r.get('login')
        pas: str = r.get('password')
        if not login:
            r.set('login', flask.request.form.get('log'))
            r.set('pas', flask.request.form.get('pas'))
            return flask.redirect(
                    flask.url_for('auth_page')
                )
        else:
            return flask.redirect(
                    flask.url_for('auth_page')
                )
    return flask.render_template(
        'index.html'
    )
            
@app.route('/auth', methods=['GET', 'POST'])
def auth_page() -> dict:
    if flask.request.method == 'POST':
        login: str = r.get('login')
        pas: str = r.get('password')
        if (
            login == r.get('login')
        ) and (
            pas == r.get('password')
        ):
            return flask.redirect(
                flask.url_for('main_page')
            )
        else:
            raise ValueError(
                "wrong password or login"
            )
    return flask.render_template(
        'index2.html'
    )

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )