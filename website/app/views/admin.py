from app import app, poweroff
from flask import render_template, request

@app.route('/admin')
def admin():
    if 'poweroff' in request.args:
      poweroff()

    return render_template('admin.html')
