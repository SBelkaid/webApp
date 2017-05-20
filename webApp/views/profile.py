from flask import Blueprint, render_template

profile = Blueprint('profile', __name__)

@profile.route('profile/hello')
def timeline():
    # Do some stuff
    return render_template('profile/hello.html')
