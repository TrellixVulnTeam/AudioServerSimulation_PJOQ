import pytest


class TestPut:

    def test_get(self, client):
        response = client.get('/update/song/1/')
        assert response.status_code == 405

    def test_post(self, client):
        response = client.put('/update/song/1/')
        assert response.status_code == 405

    def test_delete(self, client):
        response = client.delete('/update/song/1/')
        assert response.status_code == 405

    @pytest.mark.parametrize('id,name,duration,uploadedDate,status', [
        [2, "updated", 50, "2022-03-09 00:00:00", 200],
        [30, "new", 60, "2022-03-09 00:00:00", 500]
    ])
    def test_update_song(self, client, id, name, duration, uploadedDate, status):
        response = client.put('/update/song/' + id + '/',
                              json={"id": id, "name": name, "duration": duration,
                                    "uploadedDate": uploadedDate
                                    })
        assert response.status_code == status

    @pytest.mark.parametrize('id,name,duration,uploadedDate,host,participants,status', [
        [2, "new", 50, "2022-03-09 00:00:00", "me", [], 200],
        [2, "new", 60, "2022-03-09 00:00:00", "me", ["only"], 200],
        [2, "new", 60, "2022-03-09 00:00:00", "me", ["1", "2"], 500],
    ])
    def test_update_podcast(self, client, id, name, duration, uploadedDate, host, participants, status):
        response = client.post('/update/podcast/' + id + '/',
                               json={
                                   "id": id, "name": name, "duration": duration,
                                   "uploadedDate": uploadedDate, "host": host,
                                   "participants": participants
                               })
        assert response.status_code == status

    @pytest.mark.parametrize('id,name,duration,uploadedDate,author,narrator,status', [
        [1, "new", 50, "2022-03-09 00:00:00", "author", "narrate", 200],
        [1, "new", -60, "2022-03-09 00:00:00", "author", "narrate", 400],
        [30, "new", 60, "2022-03-09 00:00:00", "author", "narrate", 500],
    ])
    def test_update_audiobook(self, client, id, name, duration, uploadedDate, author, narrator, status):
        response = client.post('/update/' + id + '/',
                               json={"id": id, "name": name, "duration": duration,
                                     "uploadedDate": uploadedDate, "author": author,
                                     "narrator": narrator
                                     })
        assert response.status_code == status
