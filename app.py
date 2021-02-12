from flask import Flask, request, Response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask.views import MethodView
from datetime import datetime
from validators import is_positive,future_date
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from core.models import Song, Podcast, Audiobook


class AudioCRUDAPI(MethodView):

    def is_valid(self, data, filetype):
        if "id" not in data:
            abort(500,"Id missing")
        elif "name" not in data:
            abort(500,"Name missing")
        elif "duration" not in data:
            abort(500,"duration missing")
        elif "uploadedDate" not in data:
            abort(500,"Upload date missing")
        if filetype == "podcast":
            if "host" not in data:
                abort(500,"Host missing.")
        elif filetype == "audiobook":
            if "author" not in data:
                abort(500,"Author missing")
            elif "narrator" not in data:
                abort(500,"Narrator missing")
        duration = data['duration']
        uploadedDate = data['uploadedDate']
        if not is_positive(duration) and not future_date(uploadedDate):
            abort(400, "duration must be positive and upload date must be in the future")
        elif not future_date(uploadedDate):
            abort(400, "Uploaded date must be in the future")
        elif not is_positive(duration):
            abort(400, "duration must be positive")
        else:
            try:
                participants = data['participants']
                if len(participants) > 10:
                    abort(400, "Number of participants must be less than 10")
            except KeyError:
                pass

    def post(self):
        '''
            POST method that gets two fields:
                audioFileType: String
                audioFileMetadata: Dictionary
        :return:200 if successful
                400 in case of a bad request
        '''
        data = request.json
        audioType = data['audioFileType'].lower()
        information = data['audioFileMetadata']
        # if self.is_valid(information, audioType) == "Pass":
        self.is_valid(information,audioType)
        if audioType == 'song':
            newSong = Song(id=information['id'], songName=information['name'], duration=information['duration'],
                           uploadedDate=information['uploadedDate'])
            newSong.save_to_db()
            return Response("Song added", status=200)
        elif audioType == 'podcast':
            if "participants" in information:
                newPodcast = Podcast(id=information['id'], podcastName=information['name'], host=information['host'],
                                     duration=information['duration'], uploadedDate=information['uploadedDate'],
                                     participants=information['participants'])
            else:
                newPodcast = Podcast(id=information['id'], podcastName=information['name'], host=information['host'],
                                     duration=information['duration'], uploadedDate=information['uploadedDate'])
            newPodcast.save_to_db()
            return Response("Podcast added", status=200)
        else:
            newAudiobook = Audiobook(id=information['id'], audiobookTitle=information['name'],
                                     duration=information['duration'], uploadedDate=information['uploadedDate'],
                                     author=information['author'], narrator=information['narrator'])
            newAudiobook.save_to_db()
            return Response("Audiobook added", status=200)

    def get(self, filetype, id=None):
        if id is None:
            if filetype == 'song':
                return jsonify(songs=[i.serialize for i in Song.query.all()])
            elif filetype == 'podcast':
                return jsonify(podcasts=[i.serialize for i in Podcast.query.all()])
            elif filetype == 'audiobook':
                return jsonify(audiobooks=[i.serialize for i in Audiobook.query.all()])
        else:
            if filetype == 'song':
                song = Song.query.get(id)
                return jsonify(song=song.serialize)
            elif filetype == 'podcast':
                podcast = Podcast.query.get(id)
                return jsonify(podcast=podcast.serialize)
            elif filetype == 'audiobook':
                audiobook = Audiobook.query.get(id)
                return jsonify(audiobook=audiobook.serialize)
        return Response("Audio type doesn't exist", status=400)

    def delete(self, filetype, id):
        if filetype == 'song':
            song = Song.query.get(id)
            db.session.delete(song)
            db.session.commit()
            return Response("Song delete", status=200)
        elif filetype == 'podcast':
            podcast = Podcast.query.get(id)
            db.session.delete(podcast)
            db.session.commit()
            return Response("Podcast delete", status=200)
        elif filetype == 'audiobook':
            audiobook = Audiobook.query.get(id)
            db.session.delete(audiobook)
            db.session.commit()
            return Response("Audiobook delete", status=200)

    def put(self, filetype, id):
        data = request.json
        self.is_valid(data,filetype)
        if filetype == 'song':
            song = Song.query.get(id)
            song.id = data['id']
            song.songName = data['name']
            song.duration = data['duration']
            song.uploadedDate = data['uploadedDate']
            song.save_to_db()
            return Response("Song updated", status=200)
        elif filetype == 'podcast':
            podcast = Podcast.query.get(id)
            podcast.id = data['id']
            podcast.podcastName = data['name']
            podcast.duration = data['duration']
            podcast.uploadedDate = data['uploadedDate']
            podcast.host = data['host']
            try:
                podcast.participants = data['participants']
            except KeyError:
                pass
            db.session.add(podcast)
            db.session.commit()
            return Response("Podcast updated", status=200)
        elif filetype == 'audiobook':
            audiobook = Audiobook.query.get(id)
            audiobook.id = data['id']
            audiobook.audiobookTitle = data['audiobookTitle']
            audiobook.duration = data['duration']
            audiobook.uploadedDate = data['uploadedDate']
            audiobook.author = data['author']
            audiobook.narrator = data['narrator']
            db.session.add(audiobook)
            db.session.commit()
            return Response("Audiobook updated", status=200)


view = AudioCRUDAPI.as_view('CRUD')
app.add_url_rule('/create/', view_func=view, methods=['POST'])
app.add_url_rule('/get/<filetype>/', view_func=view, methods=['GET'])
app.add_url_rule('/get/<filetype>/<id>/', view_func=view, methods=['GET'])
app.add_url_rule('/delete/<filetype>/<id>/', view_func=view, methods=['DELETE'])
app.add_url_rule('/update/<filetype>/<id>/', view_func=view, methods=['PUT'])

if __name__ == '__main__':
    app.debug = True
    app.run()
