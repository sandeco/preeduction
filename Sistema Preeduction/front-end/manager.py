
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CsrfProtect
csrf = CsrfProtect()

app = Flask(__name__)
app.config.from_object('config')
csrf.init_app(app)

# Read database settings from the configuration file
dbhost = app.config['DBHOST']
dbname = app.config['DBNAME']
dbuser = app.config['DBUSERNAME']
dbpass = app.config['DBPASSWORD']


db = SQLAlchemy(app)

# Set the SQLAlchemy connection string to our database using provided information.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+dbuser+':'+dbpass+'@'+dbhost+'/'+dbname


login_manager = LoginManager(app)
login_manager.login_view = 'login'

