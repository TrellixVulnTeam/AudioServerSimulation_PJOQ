from app import db


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    songName = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploadedDate = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, songName, duration, uploadedDate):
        self.id = id
        self.songName = songName
        self.duration = duration
        self.uploadedDate = uploadedDate

    def __repr__(self):
        return '<Song %r>' % self.songName

    @property
    def serialize(self):
        return {
            'id': self.id,
            'song Name': self.songName,
            'duration': self.duration,
            'uploaded date': self.uploadedDate,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Podcast(db.Model):
    __tablename__ = 'podcast'

    id = db.Column(db.Integer, primary_key=True)
    podcastName = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploadedDate = db.Column(db.DateTime, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.ARRAY(db.String(100)))

    def __init__(self, id, podcastName, duration, uploadedDate, host, participants=None):
        self.id = id
        self.podcastName = podcastName
        self.duration = duration
        self.uploadedDate = uploadedDate
        self.host = host
        if not (participants is None):
            self.participants = participants

    def __repr__(self):
        return '<Podcast %r>' % self.podcastName

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'podcast Name': self.podcastName,
            'duration': self.duration,
            'uploaded date': self.uploadedDate,
            'host': self.host,
            'participants': self.participants,
        }


class Audiobook(db.Model):
    __tablename__ = 'audiobook'

    id = db.Column(db.Integer, primary_key=True)
    audiobookTitle = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploadedDate = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)

    def __init__(self, id, audiobookTitle, duration, uploadedDate, author, narrator):
        self.id = id
        self.audiobookTitle = audiobookTitle
        self.duration = duration
        self.uploadedDate = uploadedDate
        self.author = author
        self.narrator = narrator

    def __repr__(self):
        return '<Audiobook %r>' % self.audiobookTitle

    @property
    def serialize(self):
        return {
            'id': self.id,
            'audiobook title': self.audiobookTitle,
            'duration': self.duration,
            'uploaded date': self.uploadedDate,
            'author': self.author,
            'narrator': self.narrator
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()