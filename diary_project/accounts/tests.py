from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Profile


User = get_user_model()


class AccountsTests(TestCase):
    def test_register_requires_email_and_saves_profile_phone(self):
        response = self.client.post(reverse("register"), {
            "username": "new_user",
            "email": "new@example.com",
            "phone": "77777777777",
            "password1": "StrongPass12345",
            "password2": "StrongPass12345",
        })

        self.assertRedirects(response, reverse("entry_list"))
        user = User.objects.get(username="new_user")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.profile.phone, "77777777777")

    def test_register_rejects_empty_email(self):
        response = self.client.post(reverse("register"), {
            "username": "new_user",
            "email": "",
            "password1": "StrongPass12345",
            "password2": "StrongPass12345",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="new_user").exists())

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_profile_update_changes_user_and_profile_fields(self):
        user = User.objects.create_user(username="owner", password="password12345", email="old@example.com")
        Profile.objects.filter(user=user).update(phone="111")
        self.client.force_login(user)

        response = self.client.post(reverse("profile_edit"), {
            "first_name": "Ivan",
            "last_name": "Petrov",
            "email": "ivan@example.com",
            "phone": "77777777777",
        })

        self.assertRedirects(response, reverse("profile"))
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Ivan")
        self.assertEqual(user.last_name, "Petrov")
        self.assertEqual(user.email, "ivan@example.com")
        self.assertEqual(user.profile.phone, "77777777777")
