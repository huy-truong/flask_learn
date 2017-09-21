from datetime import datetime
from flask import Flask, render_template,session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_required

@main.route("/", methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('.index'))
    return render_template('index.html',form=form, name=session.get('name'), current_time=datetime.utcnow(), known = session.get('known'))


@main.route("/secret")
@login_required
def secret():
    return ' Only authenticated users are allowed'
