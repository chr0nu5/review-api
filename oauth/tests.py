from django.test import TestCase
from oauth.models import Client


# Create your tests here.
class ClientTestCase(TestCase):
    def setUp(self):
        client = Client(username="john", password="john")
        # client.generate_token()
        client.save()

    def test_client_null_token(self):
        """The user does not have a token"""
        client = Client.objects.get(username="john")
        self.assertIsNone(client.get_token())

    def test_client_has_token(self):
        """The user have a token with len 36"""
        client = Client.objects.get(username="john")
        client.generate_token()
        self.assertEqual(len(client.get_token()), 36)

    def test_client_invalidate_token(self):
        """The user token will be invalidated"""
        client = Client.objects.get(username="john")
        client.generate_token()
        client.invalidate_token()
        self.assertIsNone(client.get_token())
