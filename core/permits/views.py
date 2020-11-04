from flask import render_template, redirect, request, url_for, Blueprint, flash, abort
from jinja2 import TemplateNotFound

from flask_login import current_user, login_required

from core import db
from core.models import Permit
from core.permits.forms import PermitForm

permits = Blueprint('permit', __name__)


@permits.route('/')
def index():
    try:
        return render_template('index.html', title='Permit Log')
    except TemplateNotFound:
        abort(404)


@permits.route('/create_permit', methods=['GET', 'POST'])
@login_required
def create_permit():
    form = PermitForm()

    if form.validate_on_submit():
        permit = Permit(user_id=current_user.id,
                        title=form.title.data,
                        text=form.text.data,
                        location=form.location.data,
                        mileage=form.mileage.data,
                        resolved=form.resolved.data,
                        follow_up=form.follow_up.data)
        db.session.add(permit)
        db.session.commit()
        flash('Posted Successfuly')
        return redirect(url_for('permit.permit_list'))
    return render_template('create_permit.html', title='Create Permit', form=form)


@permits.route('/<int:permit_id>')
@login_required
def permit(permit_id):
    permit = Permit.query.get_or_404(permit_id)
    return render_template('permit.html', title=permit.title, date=permit.date, permit=permit)


@permits.route('/<int:permit_id>/update', methods=['GET', 'POST'])
@login_required
def update_permit(permit_id):
    permit = Permit.query.get_or_404(permit_id)
    if permit.author != current_user:
        abort(403)

    form = PermitForm()
    if form.validate_on_submit():
        permit.title = form.title.data
        permit.text = form.text.data
        permit.location = form.location.data
        permit.mileage = form.mileage.data
        permit.resolved = form.resolved.data
        permit.follow_up = form.follow_up.data
        db.session.commit()
        flash('Updated Successfuly')
        return redirect(url_for('permit.permit', permit_id=permit.id))

    elif request.method == 'GET':
        form.title.data = permit.title
        form.text.data = permit.text
        form.location.data = permit.location
        form.mileage.data = permit.mileage
        form.resolved.data = permit.resolved
        form.follow_up.data = permit.follow_up

    return render_template('create_permit.html', title='Update Permit', form=form)


@permits.route('/<int:permit_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_permit(permit_id):
    permit = Permit.query.get_or_404(permit_id)
    if permit.author != current_user:
        abort(403)

    db.session.delete(permit)
    db.session.commit()
    flash('Permit Deleted')
    return redirect(url_for('permit.permit_list'))


@permits.route('/permit_list')
@login_required
def permit_list():
    page = request.args.get('page', 1, type=int)
    permits = Permit.query.order_by(Permit.date.desc()).paginate(page=page, per_page=5)
    return render_template('permit_list.html', title='Permits List', permits=permits)