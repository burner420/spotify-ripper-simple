try:
    from __main__ import app
except:
    from my_app import app

from flask_sqlalchemy import SQLAlchemy
import datetime
import pickle
import json
import string
import os

db = SQLAlchemy(app)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(20), unique=True, index=True)
    value = db.Column(db.String(255))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Setting %r - %r>' % (self.key, self.value)

    @classmethod
    def set(cls, key, value):
        """ Sets setting key/value pair
        key: string
        value: Python object (object is pickled as saved in db)
        """
        result = cls.query.filter_by(key=key).first()
        if result:
            db.session.delete(result)
            db.session.commit()
        item = cls(key=key,value=pickle.dumps(value))
        db.session.add(item)
        db.session.commit()

    @classmethod
    def get(cls, key):
        """
        Returns value of key
        Params:
            key: string
        Returns: 
            Python object or None if undefined
        """
        result = cls.query.filter_by(key=key).first()
        if result:
            return pickle.loads(result.value)
        return None



rip_song_association_table = db.Table('rip_song_join', db.Model.metadata,
    db.Column('rip_id', db.Integer, db.ForeignKey('rip.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

class Rip(db.Model):
    __tablename__ = 'rip'
    id = db.Column(db.Integer, primary_key=True)
    songs = db.relationship("Song", secondary=rip_song_association_table, back_populates="rips")
    name = db.Column(db.String(100))
    urls = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Integer)

    # time estimates
    total_duration = db.Column(db.Integer)
    total_position = db.Column(db.Integer)
    total_eta = db.Column(db.Integer)

    # song time estimates
    song_duration = db.Column(db.Integer)
    song_position = db.Column(db.Integer)
    song_eta = db.Column(db.Integer)

    current_track = db.Column(db.Integer, db.ForeignKey('song.id'))

    file_name = db.Column(db.String(1000))

    #Current song
    #Song Count
    statuses = { 1:"Queued",
                 2:"Ripping",
                 3:"Complete Successfully",
                 4:"Complete With Error",
                 5: "Error Logging In",
                 6: "Bad App Key"}

    @classmethod
    def from_url_list(cls,name,urls):
        """Takes a list of urls separated by newline characters"""
        rip = cls(name=name, urls=urls, status=1)
        rip.file_name = rip.generate_file_name()
        db.session.add(rip)
        db.session.commit()

    def update_status(self, status):
        self.status = status
        self.save()

    def save(self):
        sess = db.session.object_session(self)
        sess.add(self)
        sess.commit()

    @property
    def total_pct(self):
        if not self.total_duration and not self.song_position:
            return 0
        if not self.total_duration:
            return self.song_pct
        pct = int( (self.total_position + self.song_position) * 100 / self.total_duration )
        if pct>100:
            return 100
        return pct

    @property
    def song_pct(self):
        if not self.song_position or not self.song_duration:
            return 0
        pct = int(self.song_position * 100 / self.song_duration )
        return pct

    def format_time(self, seconds):
        if not seconds:
            return "?"
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h:
            return "%d:%02d:%02d" % (h, m, s)
        return "%01d:%02d" % (m, s)

    @property
    def total_eta_formatted(self):
        if not self.total_eta:
            return self.song_eta_formatted
        return self.format_time(self.total_eta)

    @property
    def song_eta_formatted(self):
        return self.format_time(self.song_eta)

    def to_dict(self):
        s = [s.to_dict() for s in self.songs]
        d = {   "id": self.id,
                "name": self.name,
                "file_name": self.file_name,
                "status": self.status,
                "total_duration": self.total_duration,
                "total_position": self.total_position,
                "total_eta": self.total_eta,
                "song_duration": self.song_duration,
                "song_position": self.song_position,
                "total_pct": self.total_pct,
                "song_eta_formatted":self.song_eta_formatted,
                "total_eta_formatted": self.total_eta_formatted,
                "songs": s

            }
        return d

    def generate_file_name(self):
        valid_characters = string.ascii_letters + string.digits
        cleaned_name = ''.join([s for s in self.name if s in valid_characters])
        appended_int = 2
        file_name = cleaned_name+'.zip'

        rip = Rip.query.filter(Rip.file_name == file_name).first()
        if not rip:
            return cleaned_name+'.zip'

        while True:
            file_name =  cleaned_name + '(' + str(appended_int) + ')'+'.zip'
            rip = Rip.query.filter(Rip.file_name == file_name).first()
            if not rip:
                return file_name
            appended_int += 1





class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    rips = db.relationship("Rip", secondary=rip_song_association_table, back_populates="songs")
    file_name = db.Column(db.String(1000))
    spotify_uri = db.Column(db.String(255))
    name = db.Column(db.String(1000))
    artist = db.Column(db.String(1000))
    length = db.Column(db.Integer)
    number = db.Column(db.Integer)
    addl = db.Column(db.Text)

    def to_dict(self):
        s = {   "id": self.id,
                "file_name": self.file_name,
                "spotify_uri": self.spotify_uri,
                "name": self.name,
                "artist": self.artist,
                "length": self.length,
                "number": self.number,
                "addl": self.addl
              }

        return s

    @classmethod
    def create_from_track_tags(cls,tags,rip_id):
        s = cls()
        s.spotify_track_id =    tags['uri']
        s.name =                tags['track_name']
        s.artist =              tags['artist']
        s.number =              tags['idx']
        rip = Rip.query.get(rip_id)
        s.rips.append(rip)

        sess = db.session.object_session(s)
        sess.add(s)
        sess.commit()
