from app.client import MyClient

class User:

    def __init__(self, client):
        self.is_premium = False
        self.is_admin = False
        self.client = client

    @property
    def client(self):
        return self.client

    @property
    def username(self):
        return self.client.username