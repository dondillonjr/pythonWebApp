# File (auth.py) is a blueprint for our 
# Web Application, URLs/routes are defined here.
# 
# (Authintication) Blueprint - contains URLs/routes 
# user can go to via website browser. Ex login page,
# sign-up page and logout page.
#
# Blueprint contains functions: 
# login(), sign-up(), and logout() which are called
# when user enters the following URLs in browser:
# /login, /sign-up, /logout
#
# Package Flask imports "Blueprint" function.
# To Render template so you can see it on 
# screen you must import render_template
# To get access to request data from POST you must
# import request.
# To have messages shown to users on webpage you 
# must import flash
from logging import debug
import MySQLdb
from   MySQLdb import cursors
from   MySQLdb.cursors import Cursor
from   flask import Blueprint, render_template, request, flash
from   .__init__ import db
import json
# (auth variable) is name of Blueprint 
# 'auth' is file containing Blueprint
auth = Blueprint('auth', __name__)

# Function login() is called when url "/llogin"
# is entered in browser. Browser (renders/shows)
# page on browser.
#
# Define a route in FLASK
# @auth.route() is called a declorator
# Render template so we can see it on screen 
# call return render_template() and retrun
# login.html template.
#
# methods=get, post allows route /login to except
# both get and post request.
#
# EXample of GET request
# When you go to /home/login from the web browser
# you are getting a response from the webServer
# GET - Loading a web page or retrieving information, 
# retrieving html that represents page. No data sent 
# to server for GET request
#
# Example of POST request
# When you hit the (Login) button from the Login 
# web page you are sending (request) with login fields
# (email, name, password) to the webServer for
# route /home/login. Server will interpret request and
# afterwards respond/do something
# POST = make change to database, or change to state of
# (website or system). Sends all information in form to
# web Server
#
#################### Login #################################
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Note: request.form will only contain data if 
    # request is launched via the Login button (POST) from 
    # login page.  Note - login & password will show in 
    # terminal output via -- print(data)
    # ImmutableMultiDict([('email', 'don@com'), ('password', 'a123')])
    # 
    # If /home/login is entered via browser a GET request
    # is generated. No data is sent to Webserver for GET # # request. 
    # (request.form) will have no data. 

    data = request.form
    #print(request.get_json['userName'])
    #print(data)
    
    if request.method == 'POST':
        #user    = request.form.get('userName')
        #passwd  = request.form.get('password')
        #######   OR ################
        grab_json = json.dumps(data)
        json_data = json.loads(grab_json)
        user      = json_data['userName']
        passwd    = json_data['password']
        print(f"user='{user}' password='{passwd}'")

        try:
            cur = db.connection.cursor()
            sql = f"select username, password from legal_users where username = '{user}'"
            print(sql)
            cur.execute(sql)
            results = cur.fetchone()
            cur.close()

            #print(results)
            print(f"db_user='{results['username']}' db_passwd='{results['password']}'")
            ########### MESSAGE FLASH ############
            ## POP Message on WEB PAGE - part of Flask
            ## TO use, must import FLASH
            if user != results['username']:
                #flash - shows message on web page - category=error, category=success
                #category used to display messages in different colors
                flash('Invalid User Name.', category='error')
            else:
                if passwd != results['password']:
                    flash('Invalid Password.', category='error')
                else:
                    # add user validated
                    flash('Login Successful', category='success')

        except MySQLdb.OperationalError as err:
            flash('MySQL server host issue', category='error')
        except TypeError as err:
            flash('Invalid User', category='error') 
        except MySQLdb.MySQLError as error:
            flash("Failed to delete user" .format(error), category='error')
            print("Failed to delete user" .format(error))            
            
    # pass (variable/values) hold_var to (template) login.html
    return render_template("login.html", hold_var="Hello Don", boolean=True)

################################# SIGN UP #########################################
# Function sign-up() is called when url "/sign-up"
# is entered in browser. Browser (renders/shows)
# page on browser.
#
# Define a route in FLASK
# @auth.route() is called a declorator
# Render template so we can see it on screen 
# call return render_template() and retrun
# sign_up.html template.
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        userName      = request.form.get('userName')
        password1     = request.form.get('password1')
        password2     = request.form.get('password2')
        email         = request.form.get('email')
        contactnumber = request.form.get('contactnumber')
        print(request.form)
        
        ########### FLASH MESSAGE ############
        ## POP Message on WEB PAGE - part of Flask
        ## TO use, must import FLASH
        
        if len(userName) < 2:
            #flash - shows message on web page - category=error, category=success
            #category used to display messages in different colors
            flash('userName must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 5:
            flash('Password must be greater than 4 character.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 character.', category='error')
        elif len(contactnumber) < 9:
            flash('Password must be greater than 9 character.', category='error')
        else:
            try:
                cur = db.connection.cursor()
                sql = ("INSERT INTO legal_users (username, password, email, contactnumber) VALUES (%s, %s, %s, %s)",  (userName, password1, email, contactnumber  ))
                print(sql)
                cur.execute(*sql)
                
                db.connection.commit() 
                cur.close() 
                
                flash('Account created', category='success')                 
            except MySQLdb.OperationalError as err:
                flash('MySQL server host issue', category='error')

            except MySQLdb.MySQLError as error:
                flash("Failed to insert into MySQL table {}" .format(error), category='error')
                print("Failed to insert into MySQL table {}" .format(error))

    return render_template("sign_up.html")

########################  Delete Account #############################
@auth.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    # Note: request.form will only contain data if 
    # request is launched via the Delete button (POST) from 
    # Delete Account page.  Note - login & password will show in 
    # terminal output via -- print(data)
    # ImmutableMultiDict([('email', 'don@com'), ('password', 'a123')])
    # 
    # If /home/delete-account is entered via browser a GET request
    # is generated. No data is sent to Webserver for GET # # request. 
    # (request.form) will have no data. 

    #data = request.form
    #print(data)
  
    if request.method == 'POST':
        user    = request.form.get('userName')
        #print(f"user='{user}'")
        if len(user) < 2 or user == '':
            #flash - shows message on web page - category=error, category=success
            #category used to display messages in different colors
            flash('Invalid user.', category='error')
        else:
            try:
                cur = db.connection.cursor()
                sql = f"delete from legal_users where username = '{user}'"
                print(sql)
                cur.execute(sql)
                db.connection.commit()
                cur.close()
                ########### MESSAGE FLASH ############
                ## POP Message on WEB PAGE - part of Flask
                ## TO use, must import FLASH
                flash('Account Deleted', category='success')
            except MySQLdb.OperationalError as err:
                flash('MySQL server host issue', category='error')
            except MySQLdb.MySQLError as error:
                flash("Failed to delete user" .format(error), category='error')
                print("Failed to delete user" .format(error))      

    # pass (variable/values) hold_var to (template) login.html
    return render_template("delete_account.html", hold_var="Hello Don", boolean=True)

######################### Logout #############################

# Function logout() is called when url "/logout"
# is entered in browser. Browser (renders/shows)
# page on browser.
#
# Define a route in FLASK
# @auth.route() is called a declorator
# Render template so we can see it on screen 
# call return render_template().
@auth.route('/logout')
def logout():
    return "<p>LogMeOut</p>"

### DON'T forget to register Blueprints in 
### __init__.py