from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from URLShortner import ShortenURL

app = Flask(__name__)

ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/main'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uczejptlqhvfqr:f7d9a98c519c8a2c059dab0f1a6d77ac1ab3680e6bc2c977275eb6ff7ce28df7@ec2-100-25-100-81.compute-1.amazonaws.com:5432/dfuidlno58nps5'
db = SQLAlchemy(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(80), unique=True, nullable=False)
    long_url = db.Column(db.String(200), unique=True, nullable=False)

    def __init__(self, short_url, long_url):
        self.short_url = short_url
        self.long_url = long_url

@app.route('/', methods=['POST', 'GET'])
def index():
    entries = URL.query.all()
    if request.method == 'POST' and request.form['long_url']:
        long_url = request.form['long_url']
        short_url = ShortenURL().encode(long_url)
        url = URL(short_url, long_url)
        db.session.add(url) 
        db.session.commit()
        entries = URL.query.all()
    return render_template('home.html', entries=entries)

if __name__ == '__main__':
    app.run()