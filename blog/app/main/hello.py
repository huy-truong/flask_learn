from flask import Flask, redirect, url_for, render_template, session, flash 
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os

from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash, check_password_hash



basedir = os.path.abspath(os.path.dirname(__file__))


app= Flask(__name__)
app.config['SECRET_KEY']='matkhau'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment= Moment(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

app.config.update(
            #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'huy.truong.ict@jvn.edu.vn',
    MAIL_PASSWORD = 'n0^B!e^1t'
    )


mail=Mail(app)




@app.route("/sendmail")
def sendmail():
    msg = Message('Send mail testing',sender='truonghuy1801@gmail.com',
            recipients=['truonghuy1801@gmail.com'],body = 'Congratulation, sending is ok')

    mail.send(msg)
    return "Mail sent"


@app.route("/", methods=['GET','POST'])
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
        return redirect(url_for('index'))
    return render_template('index.html',form=form, name=session.get('name'), current_time=datetime.utcnow(), known = session.get('known'))

@app.route("/user/<name>")
def user(name):
    return render_template('user.html',name=name)


   

if __name__== "__main__":
    manager.run()
