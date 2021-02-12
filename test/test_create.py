import pytest


class TestCreate:

    def test_get(self, client):
        response = client.get('/create/')
        assert response.status_code == 405

    def test_put(self, client):
        response = client.put('/create/')
        assert response.status_code == 405

    def test_delete(self, client):
        response = client.delete('/create/')
        assert response.status_code == 405

    @pytest.mark.parametrize('id,name,duration,uploadedDate,status', [
        [15, "new", 50, "2022-03-09 00:00:00", 200],
        [15, "new", -60, "2022-03-09 00:00:00", 400],
        [16, "new", -60, "2020-03-09 00:00:00", 400],
        [17, "new", 60, "2020-03-09 00:00:00", 400]
    ])
    def test_create_song(self, client, id, name, duration, uploadedDate, status):
        response = client.post('/create/',
                               json={"audioFileType": "song",
                                     "audioFileMetadata": {"id": id, "name": name, "duration": duration,
                                                           "uploadedDate": uploadedDate
                                                           }})
        assert response.status_code == status

    @pytest.mark.parametrize('id,name,duration,uploadedDate,host,participants,status', [
        [21, "new", 50, "2022-03-09 00:00:00", "me", [], 200],
        [22, "new", 60, "2022-03-09 00:00:00", "me", ["only"], 200],
        [23, "new", 60, "2020-03-09 00:00:00", "me", ["1", "2"], 400],
        [24, "new", 60, "2022-03-09 00:00:00", "me", ["1", "2", "1", "2", "1", "2", "1", "2", "1", "2", "2"], 400]
    ])
    def test_create_podcast(self, client, id, name, duration, uploadedDate, host, participants, status):
        response = client.post('/create/',
                               json={"audioFileType": "podcast",
                                     "audioFileMetadata": {"id": id, "name": name, "duration": duration,
                                                           "uploadedDate": uploadedDate, "host": host,
                                                           "participants": participants
                                                           }})
        assert response.status_code == status

    @pytest.mark.parametrize('id,name,duration,uploadedDate,author,narrator,status', [
        [14, "new", 50, "2022-03-09 00:00:00", "author", "narrate", 200],
        [15, "new", -60, "2022-03-09 00:00:00", "author", "narrate", 400],
    ])
    def test_create_audiobook(self, client, id, name, duration, uploadedDate, author, narrator, status):
        response = client.post('/create/',
                               json={"audioFileType": "audiobook",
                                     "audioFileMetadata": {"id": id, "name": name, "duration": duration,
                                                           "uploadedDate": uploadedDate,"author": author,
                                                           "narrator": narrator
                                                           }})
        assert response.status_code == status


