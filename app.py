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
from wtforms.validators import  InputRequired, Email, Length

# Flask Bootstrap implementiert Bootstrap Variablen für das Projekt
from flask_bootstrap import Bootstrap

# Zur Verschluesselung des Passworts gibt es von Python3 vorgefertigte Variablen - sha256
from werkzeug.security import generate_password_hash, check_password_hash

# Vorgefertigte Variablen für Flask, um den Loginprozess programmiertechnisch einfacher zu gestalten
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from chicken_dinner.pubgapi import PUBG

# Testimport für die Seite Artikel
from data import Articles

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

        # Flash ist noch nicht richtig implementiert!
        #flash('your account hast been updated!', 'success')

        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('settings.html', form=form)

@app.route('/comparison', methods=['GET', 'POST'])
@login_required
def comparison():

    player_one = None
    player_two = None
    player_one_stats = {}
    player_two_stats = {}

    if request.method == 'POST':
        player_one = request.form.get('playerOneName')

        if player_one:
            player_two = request.form.get('playerName')
        else:
            player_one = request.form.get('playerName')

        player_one_stats = Player_stats(player_one)

        if player_two:
            player_two_stats = Player_stats(player_two)

    return render_template('comparison.html', player_one=player_one, player_two=player_two, player_one_stats=player_one_stats, player_two_stats=player_two_stats)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                #Vorerst wird der Nutzer nach einem erfolgreichen Login auf die About-Seite geschickt
                return redirect(url_for('dashboard'))

        return '<h1>Ungueltiger Username oder Passwort</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        #sha256 erzeugt ein 80 Charakter langes Passwort, daher auch in der DB 80 Stellen vermerkt
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>Neuer Benutzer wurde angelegt!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('You are now logged out', 'success')
    return redirect('home')


#Aufbau der Datenbank bzw. Tabelle User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

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


def Player_stats(playername):
    # API-KEY
    api_key = "API-KEY"
    # (server) beschreibt, von wo den Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    squad_fpp_stats = shroud_season.game_mode_stats("squad", "fpp")

    temporary_dict = {}
    temporary_dict['wins'] = squad_fpp_stats['wins']
    temporary_dict['kills'] = squad_fpp_stats['kills']
    temporary_dict['assists'] = squad_fpp_stats['assists']
    temporary_dict['best_rank_point'] = squad_fpp_stats['best_rank_point']
    temporary_dict['boosts'] = squad_fpp_stats['boosts']
    temporary_dict['dbnos'] = squad_fpp_stats['dbnos']
    temporary_dict['daily_kills'] = squad_fpp_stats['daily_kills']
    temporary_dict['daily_wins'] = squad_fpp_stats['daily_wins']
    temporary_dict['damage_dealt'] = squad_fpp_stats['damage_dealt']
    temporary_dict['days'] = squad_fpp_stats['days']
    temporary_dict['headshot_kills'] = squad_fpp_stats['headshot_kills']
    temporary_dict['kill_points'] = squad_fpp_stats['kill_points']
    temporary_dict['longest_kill'] = squad_fpp_stats['longest_kill']
    temporary_dict['longest_time_survived'] = squad_fpp_stats['longest_time_survived']
    temporary_dict['losses'] = squad_fpp_stats['losses']
    temporary_dict['max_kill_streaks'] = squad_fpp_stats['max_kill_streaks']
    temporary_dict['most_survival_time'] = squad_fpp_stats['most_survival_time']
    temporary_dict['rank_points'] = squad_fpp_stats['rank_points']
    temporary_dict['revives'] = squad_fpp_stats['revives']
    temporary_dict['ride_distance'] = squad_fpp_stats['ride_distance']
    temporary_dict['road_kills'] = squad_fpp_stats['road_kills']
    temporary_dict['round_most_kills'] = squad_fpp_stats['round_most_kills']
    temporary_dict['rounds_played'] = squad_fpp_stats['rounds_played']
    temporary_dict['suicides'] = squad_fpp_stats['suicides']
    temporary_dict['swim_distance'] = squad_fpp_stats['swim_distance']
    temporary_dict['team_kills'] = squad_fpp_stats['team_kills']
    temporary_dict['time_survived'] = squad_fpp_stats['time_survived']
    temporary_dict['top_10s'] = squad_fpp_stats['top_10s']
    temporary_dict['vehicle_destroys'] = squad_fpp_stats['vehicle_destroys']
    temporary_dict['walk_distance'] = squad_fpp_stats['walk_distance']
    temporary_dict['weapons_acquired'] = squad_fpp_stats['weapons_acquired']
    temporary_dict['weekly_kills'] = squad_fpp_stats['weekly_kills']
    temporary_dict['weekly_wins'] = squad_fpp_stats['weekly_wins']
    temporary_dict['win_points'] = squad_fpp_stats['win_points']
    return temporary_dict

# Start der Applikation im Debugmodus (Seite muss nicht bei jeder Aenderung neu gestartet werden - geschieht dann automatisch)
if __name__ == '__main__':
    app.run(debug=True)
