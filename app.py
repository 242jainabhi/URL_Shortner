from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from URLShortner import ShortenURL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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
    '''
    home.html is loaded when blank URL is loaded. It displays the input field for repo name and a button.
    If the button is clicked after entering the repository name, repo_name and stats_dict arguments will be 
    populated and home.html will be loaded again which will display the table of issue counts.
    '''
    return render_template('home.html', entries=entries)

@app.route('/shorten')
def shorten():
    pass

@app.route('/long_url')
def long_url():
    pass

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    '''
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    print(User.query.all())
    print(User.query.filter_by(username='admin').first())'''