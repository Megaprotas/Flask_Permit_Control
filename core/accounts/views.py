from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, logout_user, current_user, login_required

from core import db
from core.models import User, Permit
from core.accounts.forms import LoginForm, RegistrationForm, UpdateUserForm

accounts = Blueprint('accounts', __name__)


@accounts.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('permit.index'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('accounts.login'))
    return render_template('register.html', title='Register the account', form=form)


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.check_password(form.password.data) and user is not None:
            login_user(user, remember=True)
            flash('Welcome ' + current_user.username.capitalize())
            next = request.args.get('next')
            return redirect(url_for('permit.index') or next)
        flash('Invalid username/password')
        return redirect(url_for('accounts.login'))

    return render_template('login.html', title='Log-in form', form=form)


@accounts.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateUserForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Updated successfuly')
        return redirect(url_for('accounts.update'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('update.html', title=current_user.username.capitalize(), form=form)


@accounts.route('/<username>')
def user_permits(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    permits = Permit.query.filter_by(author=user).order_by(Permit.date.desc()).paginate(page=page, per_page=5)
    flash('List of permits submited by ' + username)

    return render_template('user_permits.html', title='User permit', permits=permits, user=user)