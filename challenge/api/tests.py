import requests
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import NeuralNetwork

class TestModel(APITestCase):
    """
    Test the endpoints for the NeuralWorker model
    """
    @classmethod
    def setUpTestData(cls):
        cls.nn = NeuralNetwork.objects.get(name="imagenet-inception-v3")

    def test_list(self):
        url = '/api/model/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(NeuralNetwork.objects.all().count(), len(data))

    def test_get(self):
        url = f'/api/model/{self.nn.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = response.json()
        self.assertEqual(obj['id'], self.nn.id)
        self.assertEqual(obj['name'], self.nn.name)
        self.assertEqual(obj['kind'], self.nn.kind)

    def test_read_only(self):
        url = f'/api/model/{self.nn.pk}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = {'kind': 'TAG'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_infer(self):
        url = f'/api/model/{self.nn.pk}/infer/'
        data = {}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual({'url': ['This field is required.']}, response.json())
        data = {'url': 'bad_url'}
        response = self.client.post(url, data=data)
        self.assertDictEqual({'url': ['Enter a valid URL.']}, response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'url': 'https://static.deepomatic.com/resources/demos/api-clients/dog1.jpg'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.json()['outputs'][0]['labels']['predicted'][0]['score'], 0.8, 1)


class TestWorkflow(APITestCase):
    """
    Test the endpoints for the WorkFlow model
    """

    @classmethod
    def setUpTestData(cls):
        "FILL ME"

    def test_workflow_list(self):
        "FILL ME"
        assert(False)

    def test_workflow_create(self):
        "FILL ME"
        assert(False)

    def test_workflow_delete(self):
        "FILL ME"
        assert(False)

    def test_workflow_run(self):
        TEST_IMAGES = [
            'https://storage.googleapis.com/dp-public/tech_challenge/b688efc5-8d63-4b84-b768-2dade04e3af9.jpg',
            'https://storage.googleapis.com/dp-public/tech_challenge/415185a7-8864-40a3-991d-59760327fb6b.jpg',
            'https://storage.googleapis.com/dp-public/tech_challenge/27f442cc-120b-4d8b-b49d-f94d3f27b876.jpg'
        ]

        for image in TEST_IMAGES:
            response = requests.post('https://europe-west1-deepomatic-160015.cloudfunctions.net/deepo-test-challenge', json={
                'input': image,
                'output': self.client.get("FILLME").content
            })
            self.assertEqual(200, response.status_code)
