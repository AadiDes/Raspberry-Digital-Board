from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def display_screen():
    return render_template('display.html')

@main.route('/admin')
def admin_panel():
    return render_template('admin.html')
