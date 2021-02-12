

class TestDelete:

    def test_post(self, client):
        request = client.post('/delete/audiobook/1/')
        assert request.status_code == 405

    def test_put(self, client):
        request = client.put('/delete/audiobook/1/')
        assert request.status_code == 405

    def test_get(self,client):
        request = client.get('/delete/audiobook/1/')
        assert request.status_code == 405

    def test_delete_song(self, client):
        request = client.delete('/delete/song/1/')
        assert request.status_code == 200
