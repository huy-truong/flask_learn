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

def make_shell_context():
    return dict(app=app,db=db,User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))



class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash= generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' %self.username

class NameForm(FlaskForm):
    name = StringField("What is your name? ",validators=[Required()])
    submit = SubmitField('Submit')


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html") 

@app.route("/show_info")
def show_info():
    return redirect(url_for('user',name="CHUA CO THONG TIN"))
    abort(401)
    

if __name__== "__main__":
    manager.run()
