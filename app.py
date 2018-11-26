# Importe für das Projekt
# Flask als Framework für das Pythonprojekt
from flask import Flask, render_template, redirect, url_for, request, flash

# SQLAlchemy für die Verbindung zur Datenbank
from flask_sqlalchemy import SQLAlchemy

# Forms für Flask
from flask_wtf import FlaskForm

# Spezielle Felder für die Forms
from wtforms import StringField, PasswordField, BooleanField

# Validators sind Kriterien die die einzelnen Felder ueberpruefen
from wtforms.validators import InputRequired, Email, Length

# Flask Bootstrap implementiert Bootstrap Variablen für das Projekt
from flask_bootstrap import Bootstrap

# Zur Verschluesselung des Passworts gibt es von Python3 vorgefertigte Variablen - sha256
from werkzeug.security import generate_password_hash, check_password_hash

# Vorgefertigte Variablen für Flask, um den Loginprozess programmiertechnisch einfacher zu gestalten
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Testimport für die Seite Artikel
from data import Articles

from data2 import Player_Stats_Solo

from libgravatar import Gravatar


# Initialisierung des Flask Projekts
app = Flask(__name__)

# Bevor man eine Datenbank ansprechen kann, muss ein Secret Key gesetzt werden - Kann nicht ausgesetzt werden
app.config['SECRET_KEY'] = 'HalloWelt'

# Adresse der SQLite Datenbank - Auf die Zeichenfolge muss geachtet werden
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Max\\PycharmProjects\\untitled1\\templates\\database\\database.db'

# Initialisierung der Datenbank
db = SQLAlchemy(app)

# Verknuepfung von Bootstrap zu der App ...
Bootstrap(app)

# Aufruf des LoginManagers
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Für Seite: Artikel
Articles = Articles()

'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATION = False
'''

#Routing für die einzelnen Seiten
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account hast been updated!', 'success')

        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

        image_file = url_for('static', filename='Player1.jpg')
    return render_template('settings.html', form=form,
                           image_file=image_file,
                           name=current_user.username,
                           email=current_user.email)

@app.route('/comparison', methods=['GET', 'POST'])
@login_required
def comparison1():
    player_one = None
    player_two = None
    player_one_solo_fpp_stats = {}
    player_two_solo_fpp_stats = {}

    if request.method == 'POST':
        player_one = request.form.get('playerOneName1')

        if player_one:
            player_two = request.form.get('playerName1')
        else:
            player_one = request.form.get('playerName1')

        player_one_solo_fpp_stats = Player_Stats_Solo(player_one)[1]

        if player_two:
            player_two_solo_fpp_stats = Player_Stats_Solo(player_two)[1]

    image_file1 = url_for('static', filename='Player1.jpg')
    image_file2 = url_for('static', filename='Player2.jpg')

    return render_template('comparison.html', player_one=player_one, player_two=player_two,
                           player_one_solo_fpp_stats=player_one_solo_fpp_stats,
                           player_two_solo_fpp_stats=player_two_solo_fpp_stats,
                           image_file1=image_file1, image_file2=image_file2, name=current_user.username,
                           )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash(f'You have been logged in!', 'success')
                login_user(user, remember=form.remember.data)
                #Vorerst wird der Nutzer nach einem erfolgreichen Login auf die About-Seite geschickt
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

        return '<h1>Ungueltiger Username oder Passwort</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        #sha256 erzeugt ein 80 Charakter langes Passwort, daher auch in der DB 80 Stellen vermerkt
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect('home')

#Aufbau der Datenbank bzw. Tabelle User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Felder für die LoginSeite
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

# Felder für die RegisterSeite
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])

class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

# Start der Applikation im Debugmodus (Seite muss nicht bei jeder Aenderung neu gestartet werden - geschieht dann automatisch)
if __name__ == '__main__':
    app.run(debug=True)
