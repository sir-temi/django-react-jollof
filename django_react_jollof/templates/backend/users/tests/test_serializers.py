from django.test import TestCase
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer, UserSerializer


class SerializerTest(TestCase):
    def test_register_serializer(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "newuser")

    def test_user_serializer(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["username"], "testuser")
        self.assertEqual(serializer.data["email"], "test@example.com")
