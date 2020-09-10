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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lkfqvzykbkvsjf:a04c0cefb97ed5357733dec35ed9f5980a92bde047df059ee7de99cc51e1126d@ec2-52-21-247-176.compute-1.amazonaws.com:5432/ded8f65tqo39in'
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