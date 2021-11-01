from flask import Blueprint, render_template
views = Blueprint('views', __name__)

# home() runs whenever we use url / on browser

@views.route('/')
def home():
    return render_template("home.html")