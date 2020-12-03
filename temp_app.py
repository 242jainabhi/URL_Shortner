from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from URLShortner import ShortenURL

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/main'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://exilzivydanmfb:ae842b710a694b2d8ef0b5a2a3b4c0ef681ee55c0685384c8643bf887a493547@ec2-54-161-58-21.compute-1.amazonaws.com:5432/d2ju31dvtv4h5p'
db = SQLAlchemy(app)


class URL(db.Model):
    hash_id = db.Column(db.String(10), primary_key=True)
    short_url = db.Column(db.String(80), unique=True, nullable=False)
    long_url = db.Column(db.String(200), unique=True, nullable=False)

    def __init__(self, hash_id, short_url, long_url):
        self.hash_id = hash_id
        self.short_url = short_url
        self.long_url = long_url

@app.route('/', methods=['POST', 'GET'])
def index():
    entries = URL.query.all()
    if request.method == 'POST' and request.form['long_url']:
        long_url = request.form['long_url']
        hash_id = ShortenURL().encode(long_url)
        short_url = 'localhost:5000/' + hash_id
        url = URL(hash_id, short_url, long_url)
        db.session.add(url) 
        db.session.commit()
        entries = URL.query.all()
    return render_template('home.html', entries=entries)

@app.route('/<hash_id>')
def visit_short_url(hash_id):
    longURL = URL.query.filter_by(hash_id=hash_id).first()
    return redirect(longURL.long_url, 302)


if __name__ == '__main__':
    app.run(debug=True)