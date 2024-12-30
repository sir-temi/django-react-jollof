from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile
from users.permissions import IsAdmin, IsUser


class PermissionTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin", password="password"
        )
        Profile.objects.create(user=self.admin_user, role="admin")

        self.regular_user = User.objects.create_user(
            username="user", password="password"
        )
        Profile.objects.create(user=self.regular_user, role="user")

    def test_is_admin_permission(self):
        request = self.client.get("/admin/")
        request.user = self.admin_user
        self.assertTrue(IsAdmin().has_permission(request, None))

        request.user = self.regular_user
        self.assertFalse(IsAdmin().has_permission(request, None))

    def test_is_user_permission(self):
        request = self.client.get("/user/")
        request.user = self.regular_user
        self.assertTrue(IsUser().has_permission(request, None))

        request.user = self.admin_user
        self.assertFalse(IsUser().has_permission(request, None))
