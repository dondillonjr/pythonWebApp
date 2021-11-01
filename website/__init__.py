# From package Flask import function flask
# Flask allows you to use Blueprints, flash messages,
# templates, SQLAlchemy for access database
#
#
#

#mydb = mysql.connector.connect(host=Host, user=User, password=Password, database=Database)

#QUERY1 = "Select * from legal_users"
#QUERY2 = "Select username, password, email from legal_users"
#QUERY3 = "select * from legal_users"

from flask import Flask
from flask_mysqldb import MySQL

#from flask_sqlalchemy import SQLAlchemy

Host    = "ec2-18-216-119-62.us-east-2.compute.amazonaws.com"
User    = "root"
Password="myPassword"
DB_NAME = 'validate_users'

## DEFINE NEW DATABASE (db) = database Object
# used when wanting to add something to database
#db = SQLAlchemy()
## DEFINE NEW DATABASE (db) = database Object
    # used when wanting to add something to database
db = MySQL() 

## Create Flask application, initilized it with secret key and 
## return flask app from function create_app()
def create_app(): 
    # initilize our app
    ## __name__ = represents the name of the file 
    # that was ran (main.py)
    app = Flask(__name__)
    ## Flask app use config variable SECRET_KEY, 
    # which encripts/secure session coieky date
    # related to website.
    ## secret key for our app = HelloDon
    app.config['SECRET_KEY'] = 'HelloDon'

    ## TELLs Flask where database is located my
    # my database is locate at (f'sqlite:///{DB_NAME}')
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MYSQL_HOST']     = Host
    app.config['MYSQL_USER']     = User
    app.config['MYSQL_PASSWORD'] = Password
    app.config['MYSQL_DB']       = DB_NAME
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    ## DEFINE NEW DATABASE (db) = database Object
    # used when wanting to add something to database

    ## Tell Flask we have Blueprints
    ## Import Blueprint files (.views), (.auth)
    ## Name of Blueprint (variable views), (variable auth)
    from .views import views
    from .auth  import auth
    #
    # register Blueprint with Flask application
    # url_prefix defines URL prefix used for browser
    # EX: (/home) means to for auth routes 
    # URL (/home/login) must be used to access login page
    # /home is the URL prefix
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,  url_prefix='/home')

    #import .models
    db.init_app(app)

    return app

    #def create_database(app):
        #if not path()

