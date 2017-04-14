try:
    from __main__ import app
except:
    from my_app import app
from models import db, Setting, Rip
import os
from flask import Flask, render_template, request, redirect, flash, send_from_directory
from forms import SetupForm, NewRipForm, SettingsForm
from functools import wraps
import json

#################
#### ROUTES #####
#################

def validate_setup_complete(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Setting.get("setup_completed") != True:
            return redirect("/setup")
        return f(*args, **kwargs)
    return decorated_function
    

@app.route("/new_rip", methods=['GET', 'POST'])
@validate_setup_complete
def new_rip():
    form = NewRipForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            Rip.from_url_list(form.data['name'], form.data['urls'])
            flash("Rip Created")
            return redirect("/")
    return render_template('new_rip.html', form=form)


@app.route("/")
@validate_setup_complete
def rips():
    rips = Rip.query.order_by(Rip.id.desc())
    return render_template('rips.html',rips=rips)


@app.route("/setup", methods=['GET', 'POST'])
def setup():
    form = SetupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.app_key.data
            file.save(app.spotify_key_path)
            Setting.set("username",form.username.data)
            Setting.set("password",form.password.data)
            Setting.set("setup_completed",True)
            flash("settings updated")
            return redirect("/")
    return render_template('setup.html', form=form)

@app.route("/download/<path:filename>")
def download(filename):
    zips = os.path.join(app.root_path, 'songs', 'zips')
    return send_from_directory(directory=zips, filename=filename)

@app.route("/settings", methods=['GET', 'POST'])
@validate_setup_complete
def settings():
    form = SettingsForm(format_string = Setting.get("format_string"))
    if request.method == 'POST':
        if form.validate_on_submit():
            Setting.set("format_string", form.format_string.data)
            flash("Settings Updated")
            return redirect("/")
    return render_template('settings.html', form=form)

@app.route("/api/rip/<path:rip_id>")
def api_rip(rip_id):
    rip = Rip.query.get(rip_id)
    if rip:
        return json.dumps(rip.to_dict())
    else:
        return "error"

@app.route("/api/rip")
def api_rips():
    rips = Rip.query.order_by(Rip.id.desc())
    output= [rip.to_dict() for rip in rips]
    return json.dumps(output)
