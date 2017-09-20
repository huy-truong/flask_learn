from flask import Flask, redirect, url_for, render_template, session, flash 
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app= Flask(__name__)
app.config['SECRET_KEY']='matkhau'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment= Moment(app)

class NameForm(FlaskForm):
    name = StringField("What is your name? ",validators=[Required()])
    submit = SubmitField('Submit')


@app.route("/", methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("You should change the name")
            
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',form=form, name=session.get('name'), current_time=datetime.utcnow())

@app.route("/user/<name>")
def user(name):
    return render_template('user.html',name=name)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html") 

@app.route("/show_info")
def show_info():
    return redirect(url_for('user',name="CHUA CO THONG TIN"))
    abort(401)
    

if __name__== "__main__":
    manager.run()
