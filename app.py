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
    player_one_squad_fpp_stats = {}
    player_one_squad_tpp_stats = {}
    player_one_solo_fpp_stats = {}
    player_one_solo_tpp_stats = {}
    player_one_duo_fpp_stats = {}
    player_one_duo_tpp_stats = {}

    player_two_squad_fpp_stats = {}
    player_two_squad_tpp_stats = {}
    player_two_solo_fpp_stats = {}
    player_two_solo_tpp_stats = {}
    player_two_duo_fpp_stats = {}
    player_two_duo_tpp_stats = {}


    if request.method == 'POST':
        player_one = request.form.get('playerOneName')

        if player_one:
            player_two = request.form.get('playerName')
        else:
            player_one = request.form.get('playerName')

        player_one_squad_fpp_stats = Squad_Fpp_Stats(player_one)
        player_one_squad_tpp_stats = Squad_Tpp_Stats(player_one)
        player_one_solo_fpp_stats = Solo_Fpp_Stats(player_one)
        player_one_solo_tpp_stats = Solo_Tpp_Stats(player_one)
        player_one_duo_fpp_stats = Duo_Fpp_Stats(player_one)
        player_one_duo_tpp_stats = Duo_Tpp_Stats(player_one)


        if player_two:
            player_two_squad_fpp_stats = Squad_Fpp_Stats(player_two)
            player_two_squad_tpp_stats = Squad_Tpp_Stats(player_two)
            player_two_solo_fpp_stats = Solo_Fpp_Stats(player_two)
            player_two_solo_tpp_stats = Solo_Tpp_Stats(player_two)
            player_two_duo_fpp_stats = Duo_Fpp_Stats(player_two)
            player_two_duo_tpp_stats = Duo_Tpp_Stats(player_two)

    return render_template('comparison.html', player_one=player_one, player_two=player_two, player_one_squad_fpp_stats=player_one_squad_fpp_stats, player_two_squad_fpp_stats=player_two_squad_fpp_stats, player_one_squad_tpp_stats=player_one_squad_tpp_stats, player_one_solo_fpp_stats= player_one_solo_fpp_stats, player_one_solo_tpp_stats=player_one_solo_tpp_stats, player_one_duo_fpp_stats=player_one_duo_fpp_stats, player_one_duo_tpp_stats=player_one_duo_tpp_stats,
                           player_two_squad_tpp_stats=player_two_squad_tpp_stats, player_two_solo_fpp_stats=player_two_solo_fpp_stats, player_two_solo_tpp_stats=player_two_solo_tpp_stats, player_two_duo_fpp_stats=player_two_duo_fpp_stats, player_two_duo_tpp_stats=player_two_duo_tpp_stats)


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

def Apikey():
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
    return(api_key)

def Squad_Tpp_Stats(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo die Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    squad_tpp_stats = shroud_season.game_mode_stats("squad")

    squad_tpp_stats_dict = {}
    squad_tpp_stats_dict['wins'] = squad_tpp_stats['squad']['wins']
    squad_tpp_stats_dict['kills'] = squad_tpp_stats['squad']['kills']
    squad_tpp_stats_dict['assists'] = squad_tpp_stats['squad']['assists']
    squad_tpp_stats_dict['best_rank_point'] = squad_tpp_stats['squad']['best_rank_point']
    squad_tpp_stats_dict['boosts'] = squad_tpp_stats['squad']['boosts']
    squad_tpp_stats_dict['dbnos'] = squad_tpp_stats['squad']['dbnos']
    squad_tpp_stats_dict['daily_kills'] = squad_tpp_stats['squad']['daily_kills']
    squad_tpp_stats_dict['daily_wins'] = squad_tpp_stats['squad']['daily_wins']
    squad_tpp_stats_dict['damage_dealt'] = squad_tpp_stats['squad']['damage_dealt']
    squad_tpp_stats_dict['days'] = squad_tpp_stats['squad']['days']
    squad_tpp_stats_dict['headshot_kills'] = squad_tpp_stats['squad']['headshot_kills']
    squad_tpp_stats_dict['kill_points'] = squad_tpp_stats['squad']['kill_points']
    squad_tpp_stats_dict['longest_kill'] = squad_tpp_stats['squad']['longest_kill']
    squad_tpp_stats_dict['longest_time_survived'] = squad_tpp_stats['squad']['longest_time_survived']
    squad_tpp_stats_dict['losses'] = squad_tpp_stats['squad']['losses']
    squad_tpp_stats_dict['max_kill_streaks'] = squad_tpp_stats['squad']['max_kill_streaks']
    squad_tpp_stats_dict['most_survival_time'] = squad_tpp_stats['squad']['most_survival_time']
    squad_tpp_stats_dict['rank_points'] = squad_tpp_stats['squad']['rank_points']
    squad_tpp_stats_dict['revives'] = squad_tpp_stats['squad']['revives']
    squad_tpp_stats_dict['ride_distance'] = squad_tpp_stats['squad']['ride_distance']
    squad_tpp_stats_dict['road_kills'] = squad_tpp_stats['squad']['road_kills']
    squad_tpp_stats_dict['round_most_kills'] = squad_tpp_stats['squad']['round_most_kills']
    squad_tpp_stats_dict['rounds_played'] = squad_tpp_stats['squad']['rounds_played']
    squad_tpp_stats_dict['suicides'] = squad_tpp_stats['squad']['suicides']
    squad_tpp_stats_dict['swim_distance'] = squad_tpp_stats['squad']['swim_distance']
    squad_tpp_stats_dict['team_kills'] = squad_tpp_stats['squad']['team_kills']
    squad_tpp_stats_dict['time_survived'] = squad_tpp_stats['squad']['time_survived']
    squad_tpp_stats_dict['top_10s'] = squad_tpp_stats['squad']['top_10s']
    squad_tpp_stats_dict['vehicle_destroys'] = squad_tpp_stats['squad']['vehicle_destroys']
    squad_tpp_stats_dict['walk_distance'] = squad_tpp_stats['squad']['walk_distance']
    squad_tpp_stats_dict['weapons_acquired'] = squad_tpp_stats['squad']['weapons_acquired']
    squad_tpp_stats_dict['weekly_kills'] = squad_tpp_stats['squad']['weekly_kills']
    squad_tpp_stats_dict['weekly_wins'] = squad_tpp_stats['squad']['weekly_wins']
    squad_tpp_stats_dict['win_points'] = squad_tpp_stats['squad']['win_points']
    return squad_tpp_stats_dict

def Squad_Fpp_Stats(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo den Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    squad_fpp_stats = shroud_season.game_mode_stats("squad", "fpp")

    squad_fpp_stats_dict = {}
    squad_fpp_stats_dict['wins'] = squad_fpp_stats['wins']
    squad_fpp_stats_dict['kills'] = squad_fpp_stats['kills']
    squad_fpp_stats_dict['assists'] = squad_fpp_stats['assists']
    squad_fpp_stats_dict['best_rank_point'] = squad_fpp_stats['best_rank_point']
    squad_fpp_stats_dict['boosts'] = squad_fpp_stats['boosts']
    squad_fpp_stats_dict['dbnos'] = squad_fpp_stats['dbnos']
    squad_fpp_stats_dict['daily_kills'] = squad_fpp_stats['daily_kills']
    squad_fpp_stats_dict['daily_wins'] = squad_fpp_stats['daily_wins']
    squad_fpp_stats_dict['damage_dealt'] = squad_fpp_stats['damage_dealt']
    squad_fpp_stats_dict['days'] = squad_fpp_stats['days']
    squad_fpp_stats_dict['headshot_kills'] = squad_fpp_stats['headshot_kills']
    squad_fpp_stats_dict['kill_points'] = squad_fpp_stats['kill_points']
    squad_fpp_stats_dict['longest_kill'] = squad_fpp_stats['longest_kill']
    squad_fpp_stats_dict['longest_time_survived'] = squad_fpp_stats['longest_time_survived']
    squad_fpp_stats_dict['losses'] = squad_fpp_stats['losses']
    squad_fpp_stats_dict['max_kill_streaks'] = squad_fpp_stats['max_kill_streaks']
    squad_fpp_stats_dict['most_survival_time'] = squad_fpp_stats['most_survival_time']
    squad_fpp_stats_dict['rank_points'] = squad_fpp_stats['rank_points']
    squad_fpp_stats_dict['revives'] = squad_fpp_stats['revives']
    squad_fpp_stats_dict['ride_distance'] = squad_fpp_stats['ride_distance']
    squad_fpp_stats_dict['road_kills'] = squad_fpp_stats['road_kills']
    squad_fpp_stats_dict['round_most_kills'] = squad_fpp_stats['round_most_kills']
    squad_fpp_stats_dict['rounds_played'] = squad_fpp_stats['rounds_played']
    squad_fpp_stats_dict['suicides'] = squad_fpp_stats['suicides']
    squad_fpp_stats_dict['swim_distance'] = squad_fpp_stats['swim_distance']
    squad_fpp_stats_dict['team_kills'] = squad_fpp_stats['team_kills']
    squad_fpp_stats_dict['time_survived'] = squad_fpp_stats['time_survived']
    squad_fpp_stats_dict['top_10s'] = squad_fpp_stats['top_10s']
    squad_fpp_stats_dict['vehicle_destroys'] = squad_fpp_stats['vehicle_destroys']
    squad_fpp_stats_dict['walk_distance'] = squad_fpp_stats['walk_distance']
    squad_fpp_stats_dict['weapons_acquired'] = squad_fpp_stats['weapons_acquired']
    squad_fpp_stats_dict['weekly_kills'] = squad_fpp_stats['weekly_kills']
    squad_fpp_stats_dict['weekly_wins'] = squad_fpp_stats['weekly_wins']
    squad_fpp_stats_dict['win_points'] = squad_fpp_stats['win_points']
    return squad_fpp_stats_dict

def Solo_Tpp_Stats(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo den Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    solo_tpp_stats = shroud_season.game_mode_stats("solo")

    solo_tpp_stats_dict = {}
    solo_tpp_stats_dict['wins'] = solo_tpp_stats['solo']['wins']
    solo_tpp_stats_dict['kills'] = solo_tpp_stats['solo']['kills']
    solo_tpp_stats_dict['assists'] = solo_tpp_stats['solo']['assists']
    solo_tpp_stats_dict['best_rank_point'] = solo_tpp_stats['solo']['best_rank_point']
    solo_tpp_stats_dict['boosts'] = solo_tpp_stats['solo']['boosts']
    solo_tpp_stats_dict['dbnos'] = solo_tpp_stats['solo']['dbnos']
    solo_tpp_stats_dict['daily_kills'] = solo_tpp_stats['solo']['daily_kills']
    solo_tpp_stats_dict['daily_wins'] = solo_tpp_stats['solo']['daily_wins']
    solo_tpp_stats_dict['damage_dealt'] = solo_tpp_stats['solo']['damage_dealt']
    solo_tpp_stats_dict['days'] = solo_tpp_stats['solo']['days']
    solo_tpp_stats_dict['headshot_kills'] = solo_tpp_stats['solo']['headshot_kills']
    solo_tpp_stats_dict['kill_points'] = solo_tpp_stats['solo']['kill_points']
    solo_tpp_stats_dict['longest_kill'] = solo_tpp_stats['solo']['longest_kill']
    solo_tpp_stats_dict['longest_time_survived'] = solo_tpp_stats['solo']['longest_time_survived']
    solo_tpp_stats_dict['losses'] = solo_tpp_stats['solo']['losses']
    solo_tpp_stats_dict['max_kill_streaks'] = solo_tpp_stats['solo']['max_kill_streaks']
    solo_tpp_stats_dict['most_survival_time'] = solo_tpp_stats['solo']['most_survival_time']
    solo_tpp_stats_dict['rank_points'] = solo_tpp_stats['solo']['rank_points']
    solo_tpp_stats_dict['revives'] = solo_tpp_stats['solo']['revives']
    solo_tpp_stats_dict['ride_distance'] = solo_tpp_stats['solo']['ride_distance']
    solo_tpp_stats_dict['road_kills'] = solo_tpp_stats['solo']['road_kills']
    solo_tpp_stats_dict['round_most_kills'] = solo_tpp_stats['solo']['round_most_kills']
    solo_tpp_stats_dict['rounds_played'] = solo_tpp_stats['solo']['rounds_played']
    solo_tpp_stats_dict['suicides'] = solo_tpp_stats['solo']['suicides']
    solo_tpp_stats_dict['swim_distance'] = solo_tpp_stats['solo']['swim_distance']
    solo_tpp_stats_dict['team_kills'] = solo_tpp_stats['solo']['team_kills']
    solo_tpp_stats_dict['time_survived'] = solo_tpp_stats['solo']['time_survived']
    solo_tpp_stats_dict['top_10s'] = solo_tpp_stats['solo']['top_10s']
    solo_tpp_stats_dict['vehicle_destroys'] = solo_tpp_stats['solo']['vehicle_destroys']
    solo_tpp_stats_dict['walk_distance'] = solo_tpp_stats['solo']['walk_distance']
    solo_tpp_stats_dict['weapons_acquired'] = solo_tpp_stats['solo']['weapons_acquired']
    solo_tpp_stats_dict['weekly_kills'] = solo_tpp_stats['solo']['weekly_kills']
    solo_tpp_stats_dict['weekly_wins'] = solo_tpp_stats['solo']['weekly_wins']
    solo_tpp_stats_dict['win_points'] = solo_tpp_stats['solo']['win_points']
    return solo_tpp_stats_dict

def Solo_Fpp_Stats(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo den Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    solo_fpp_stats = shroud_season.game_mode_stats("solo", "fpp")

    solo_fpp_stats_dict = {}
    solo_fpp_stats_dict['wins'] = solo_fpp_stats['wins']
    solo_fpp_stats_dict['kills'] = solo_fpp_stats['kills']
    solo_fpp_stats_dict['assists'] = solo_fpp_stats['assists']
    solo_fpp_stats_dict['best_rank_point'] = solo_fpp_stats['best_rank_point']
    solo_fpp_stats_dict['boosts'] = solo_fpp_stats['boosts']
    solo_fpp_stats_dict['dbnos'] = solo_fpp_stats['dbnos']
    solo_fpp_stats_dict['daily_kills'] = solo_fpp_stats['daily_kills']
    solo_fpp_stats_dict['daily_wins'] = solo_fpp_stats['daily_wins']
    solo_fpp_stats_dict['damage_dealt'] = solo_fpp_stats['damage_dealt']
    solo_fpp_stats_dict['days'] = solo_fpp_stats['days']
    solo_fpp_stats_dict['headshot_kills'] = solo_fpp_stats['headshot_kills']
    solo_fpp_stats_dict['kill_points'] = solo_fpp_stats['kill_points']
    solo_fpp_stats_dict['longest_kill'] = solo_fpp_stats['longest_kill']
    solo_fpp_stats_dict['longest_time_survived'] = solo_fpp_stats['longest_time_survived']
    solo_fpp_stats_dict['losses'] = solo_fpp_stats['losses']
    solo_fpp_stats_dict['max_kill_streaks'] = solo_fpp_stats['max_kill_streaks']
    solo_fpp_stats_dict['most_survival_time'] = solo_fpp_stats['most_survival_time']
    solo_fpp_stats_dict['rank_points'] = solo_fpp_stats['rank_points']
    solo_fpp_stats_dict['revives'] = solo_fpp_stats['revives']
    solo_fpp_stats_dict['ride_distance'] = solo_fpp_stats['ride_distance']
    solo_fpp_stats_dict['road_kills'] = solo_fpp_stats['road_kills']
    solo_fpp_stats_dict['round_most_kills'] = solo_fpp_stats['round_most_kills']
    solo_fpp_stats_dict['rounds_played'] = solo_fpp_stats['rounds_played']
    solo_fpp_stats_dict['suicides'] = solo_fpp_stats['suicides']
    solo_fpp_stats_dict['swim_distance'] = solo_fpp_stats['swim_distance']
    solo_fpp_stats_dict['team_kills'] = solo_fpp_stats['team_kills']
    solo_fpp_stats_dict['time_survived'] = solo_fpp_stats['time_survived']
    solo_fpp_stats_dict['top_10s'] = solo_fpp_stats['top_10s']
    solo_fpp_stats_dict['vehicle_destroys'] = solo_fpp_stats['vehicle_destroys']
    solo_fpp_stats_dict['walk_distance'] = solo_fpp_stats['walk_distance']
    solo_fpp_stats_dict['weapons_acquired'] = solo_fpp_stats['weapons_acquired']
    solo_fpp_stats_dict['weekly_kills'] = solo_fpp_stats['weekly_kills']
    solo_fpp_stats_dict['weekly_wins'] = solo_fpp_stats['weekly_wins']
    solo_fpp_stats_dict['win_points'] = solo_fpp_stats['win_points']
    return solo_fpp_stats_dict

def Duo_Tpp_Stats(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo den Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    duo_tpp_stats = shroud_season.game_mode_stats("duo")

    duo_tpp_stats_dict = {}
    duo_tpp_stats_dict['wins'] = duo_tpp_stats["duo"]['wins']
    duo_tpp_stats_dict['kills'] = duo_tpp_stats["duo"]['kills']
    duo_tpp_stats_dict['assists'] = duo_tpp_stats["duo"]['assists']
    duo_tpp_stats_dict['best_rank_point'] = duo_tpp_stats["duo"]['best_rank_point']
    duo_tpp_stats_dict['boosts'] = duo_tpp_stats["duo"]['boosts']
    duo_tpp_stats_dict['dbnos'] = duo_tpp_stats["duo"]['dbnos']
    duo_tpp_stats_dict['daily_kills'] = duo_tpp_stats["duo"]['daily_kills']
    duo_tpp_stats_dict['daily_wins'] = duo_tpp_stats["duo"]['daily_wins']
    duo_tpp_stats_dict['damage_dealt'] = duo_tpp_stats["duo"]['damage_dealt']
    duo_tpp_stats_dict['days'] = duo_tpp_stats["duo"]['days']
    duo_tpp_stats_dict['headshot_kills'] = duo_tpp_stats["duo"]['headshot_kills']
    duo_tpp_stats_dict['kill_points'] = duo_tpp_stats["duo"]['kill_points']
    duo_tpp_stats_dict['longest_kill'] = duo_tpp_stats["duo"]['longest_kill']
    duo_tpp_stats_dict['longest_time_survived'] = duo_tpp_stats["duo"]['longest_time_survived']
    duo_tpp_stats_dict['losses'] = duo_tpp_stats["duo"]['losses']
    duo_tpp_stats_dict['max_kill_streaks'] = duo_tpp_stats["duo"]['max_kill_streaks']
    duo_tpp_stats_dict['most_survival_time'] = duo_tpp_stats["duo"]['most_survival_time']
    duo_tpp_stats_dict['rank_points'] = duo_tpp_stats["duo"]['rank_points']
    duo_tpp_stats_dict['revives'] = duo_tpp_stats["duo"]['revives']
    duo_tpp_stats_dict['ride_distance'] = duo_tpp_stats["duo"]['ride_distance']
    duo_tpp_stats_dict['road_kills'] = duo_tpp_stats["duo"]['road_kills']
    duo_tpp_stats_dict['round_most_kills'] = duo_tpp_stats["duo"]['round_most_kills']
    duo_tpp_stats_dict['rounds_played'] = duo_tpp_stats["duo"]['rounds_played']
    duo_tpp_stats_dict['suicides'] = duo_tpp_stats["duo"]['suicides']
    duo_tpp_stats_dict['swim_distance'] = duo_tpp_stats["duo"]['swim_distance']
    duo_tpp_stats_dict['team_kills'] = duo_tpp_stats["duo"]['team_kills']
    duo_tpp_stats_dict['time_survived'] = duo_tpp_stats["duo"]['time_survived']
    duo_tpp_stats_dict['top_10s'] = duo_tpp_stats["duo"]['top_10s']
    duo_tpp_stats_dict['vehicle_destroys'] = duo_tpp_stats["duo"]['vehicle_destroys']
    duo_tpp_stats_dict['walk_distance'] = duo_tpp_stats["duo"]['walk_distance']
    duo_tpp_stats_dict['weapons_acquired'] = duo_tpp_stats["duo"]['weapons_acquired']
    duo_tpp_stats_dict['weekly_kills'] = duo_tpp_stats["duo"]['weekly_kills']
    duo_tpp_stats_dict['weekly_wins'] = duo_tpp_stats["duo"]['weekly_wins']
    duo_tpp_stats_dict['win_points'] = duo_tpp_stats["duo"]['win_points']
    return duo_tpp_stats_dict

def Duo_Fpp_Stats(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo den Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    duo_fpp_stats = shroud_season.game_mode_stats("duo", "fpp")

    duo_fpp_stats_dict = {}
    duo_fpp_stats_dict['wins'] = duo_fpp_stats['wins']
    duo_fpp_stats_dict['kills'] = duo_fpp_stats['kills']
    duo_fpp_stats_dict['assists'] = duo_fpp_stats['assists']
    duo_fpp_stats_dict['best_rank_point'] = duo_fpp_stats['best_rank_point']
    duo_fpp_stats_dict['boosts'] = duo_fpp_stats['boosts']
    duo_fpp_stats_dict['dbnos'] = duo_fpp_stats['dbnos']
    duo_fpp_stats_dict['daily_kills'] = duo_fpp_stats['daily_kills']
    duo_fpp_stats_dict['daily_wins'] = duo_fpp_stats['daily_wins']
    duo_fpp_stats_dict['damage_dealt'] = duo_fpp_stats['damage_dealt']
    duo_fpp_stats_dict['days'] = duo_fpp_stats['days']
    duo_fpp_stats_dict['headshot_kills'] = duo_fpp_stats['headshot_kills']
    duo_fpp_stats_dict['kill_points'] = duo_fpp_stats['kill_points']
    duo_fpp_stats_dict['longest_kill'] = duo_fpp_stats['longest_kill']
    duo_fpp_stats_dict['longest_time_survived'] = duo_fpp_stats['longest_time_survived']
    duo_fpp_stats_dict['losses'] = duo_fpp_stats['losses']
    duo_fpp_stats_dict['max_kill_streaks'] = duo_fpp_stats['max_kill_streaks']
    duo_fpp_stats_dict['most_survival_time'] = duo_fpp_stats['most_survival_time']
    duo_fpp_stats_dict['rank_points'] = duo_fpp_stats['rank_points']
    duo_fpp_stats_dict['revives'] = duo_fpp_stats['revives']
    duo_fpp_stats_dict['ride_distance'] = duo_fpp_stats['ride_distance']
    duo_fpp_stats_dict['road_kills'] = duo_fpp_stats['road_kills']
    duo_fpp_stats_dict['round_most_kills'] = duo_fpp_stats['round_most_kills']
    duo_fpp_stats_dict['rounds_played'] = duo_fpp_stats['rounds_played']
    duo_fpp_stats_dict['suicides'] = duo_fpp_stats['suicides']
    duo_fpp_stats_dict['swim_distance'] = duo_fpp_stats['swim_distance']
    duo_fpp_stats_dict['team_kills'] = duo_fpp_stats['team_kills']
    duo_fpp_stats_dict['time_survived'] = duo_fpp_stats['time_survived']
    duo_fpp_stats_dict['top_10s'] = duo_fpp_stats['top_10s']
    duo_fpp_stats_dict['vehicle_destroys'] = duo_fpp_stats['vehicle_destroys']
    duo_fpp_stats_dict['walk_distance'] = duo_fpp_stats['walk_distance']
    duo_fpp_stats_dict['weapons_acquired'] = duo_fpp_stats['weapons_acquired']
    duo_fpp_stats_dict['weekly_kills'] = duo_fpp_stats['weekly_kills']
    duo_fpp_stats_dict['weekly_wins'] = duo_fpp_stats['weekly_wins']
    duo_fpp_stats_dict['win_points'] = duo_fpp_stats['win_points']
    return duo_fpp_stats_dict

# Start der Applikation im Debugmodus (Seite muss nicht bei jeder Aenderung neu gestartet werden - geschieht dann automatisch)
if __name__ == '__main__':
    app.run(debug=True)
