

class TestGet:

    def test_post(self,client):
        request = client.post('/get/audiobook/1/')
        assert request.status_code == 405

    def test_put(self,client):
        request = client.put('/get/audiobook/1/')
        assert request.status_code == 405

    def test_delete(self,client):
        request = client.delete('/get/audiobook/1/')
        assert request.status_code == 405

    def test_get_song(self,client):
        request = client.get('/get/song/1/')
        assert request.status_code == 200


class TestGetAll:

    def test_post(self,client):
        request = client.post('/get/audiobook/')
        assert request.status_code == 405

    def test_put(self,client):
        request = client.put('/get/audiobook/')
        assert request.status_code == 405

    def test_delete(self,client):
        request = client.delete('/get/audiobook/')
        assert request.status_code == 405

    def test_get_podcasts(self,client):
        request = client.get('/get/podcast/')
        assert request.status_code == 200


