from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Advert
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    adverts = Advert.query.all()
    return render_template("home.html", adverts=adverts, user=current_user)


@views.route('/newadvert', methods=['GET', 'POST'])
def newAdvert():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')

        if len(title) < 1:
            flash('Title is too short!', category='error')
        if len(category) < 1:
            flash('Category is too short!', category='error')
        if len(description) < 10:
            flash('Description is too short!', category='error')
        else:
            new_note = Advert(title=title, category=category, description=description, add_user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Advert added!', category='success')

    return render_template("newadvert.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    advert = json.loads(request.data)
    advertId = advert['advertId']
    note = Advert.query.get(advertId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
