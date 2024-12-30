from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, role="user")

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.role, "user")

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "testuser - user")
