from flask import Flask
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_secret'
app.spotify_key_path = '/app/spotify_appkey.key'
default_format_string = '{artist} - {track_name}.{ext}'

from models import db, Setting
import views
db.create_all()
if not Setting.get("format_string"):
    Setting.set("format_string", default_format_string)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

