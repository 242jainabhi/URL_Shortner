from myproject import app, db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from myproject.models import User, URL
from myproject.forms import LoginForm, RegistrationForm
from URLShortner import ShortenURL


@app.route('/')
def home():
    if current_user.is_authenticated:
        entries = URL.query.filter_by(user_id=current_user.id)
        return render_template('welcome_user.html', userid=current_user.id, username=current_user.username, entries=entries)
    else:
        return render_template('home.html')


@app.route('/welcome/<int:userid>/<username>', methods=['POST', 'GET'])
@login_required
def welcome_user(userid, username):
    entries = URL.query.filter_by(user_id=userid)
    if request.method == 'POST' and request.form['long_url']:
        long_url = request.form['long_url']
        hash_id = ShortenURL().encode(long_url)
        short_url = request.url_root + hash_id
        url = URL(hash_id, short_url, long_url, userid)
        db.session.add(url)
        db.session.commit()
        entries = URL.query.all()
    return render_template('welcome_user.html', userid=userid, username=username, entries=entries)


@app.route('/<hash_id>')
@login_required
def visit_short_url(hash_id):
    longURL = URL.query.filter_by(hash_id=hash_id).first()
    return redirect(longURL.long_url, 302)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0] == '/':
                entries = URL.query.filter_by(user_id=current_user.id)
                next = url_for('welcome_user', userid=user.id, username=user.username, entries=entries)

            return redirect(next)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
