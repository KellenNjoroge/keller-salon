from django.test import TestCase
from .models import *


# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.user = User(username='Keller', email='kell@kell.com', password='passwadd')
        self.user.save()
        self.ras = Profile(bio='A python Programmer', contact='054234444', user=self.user)

    def tearDown(self):
        Profile.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.ras, Profile))

    def test_save(self):
        self.ras.create_user_profile(self.user, True)
        self.ras.save_user_profile(self.user)
        users = Profile.objects.all()
        self.assertTrue(len(users) > 0)
