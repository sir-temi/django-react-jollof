from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Profile


class ViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin", password="password"
        )
        self.admin_profile = Profile.objects.create(user=self.admin_user, role="admin")

        self.user = User.objects.create_user(username="user", password="password")
        self.user_profile = Profile.objects.create(user=self.user, role="user")

    def test_register_view(self):
        response = self.client.post(
            "/register/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_login_view(self):
        response = self.client.post(
            "/login/",
            {"username": "user", "password": "password"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        response = self.client.post(
            "/login/",
            {"username": "user", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "user")

    def test_admin_only_view(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Welcome, admin!")

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_only_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Welcome, regular user!")

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/user/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
