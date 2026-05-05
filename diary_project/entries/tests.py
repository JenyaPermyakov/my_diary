from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Entry


User = get_user_model()


class EntryCrudTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="password12345")
        self.editor = User.objects.create_user(username="editor", password="password12345")
        self.entry = Entry.objects.create(
            user=self.author,
            title="Alpha",
            content="Entry content",
            status="new",
        )
        self.other_user = User.objects.create_user(username="other", password="password12345")

    def test_list_and_detail_are_public(self):
        list_response = self.client.get(reverse("entry_list"))
        detail_response = self.client.get(reverse("entry_detail", args=[self.entry.pk]))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)

    def test_create_requires_login_and_assigns_current_user(self):
        anonymous_response = self.client.get(reverse("entry_create"))
        self.assertEqual(anonymous_response.status_code, 302)

        self.client.force_login(self.author)
        response = self.client.post(reverse("entry_create"), {
            "title": "Beta",
            "content": "Second entry",
            "status": "progress",
        })

        self.assertRedirects(response, reverse("entry_list"))
        self.assertTrue(Entry.objects.filter(title="Beta", user=self.author).exists())

    def test_update_requires_change_permission(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("entry_edit", args=[self.entry.pk]))
        self.assertEqual(response.status_code, 403)

        permission = Permission.objects.get(codename="change_entry")
        self.editor.user_permissions.add(permission)
        self.client.force_login(self.editor)
        response = self.client.post(reverse("entry_edit", args=[self.entry.pk]), {
            "title": "Updated",
            "content": "Updated content",
            "status": "done",
        })

        self.assertRedirects(response, reverse("entry_list"))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Updated")

    def test_author_can_update_own_entry_without_global_permission(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse("entry_edit", args=[self.entry.pk]), {
            "title": "Author update",
            "content": "Updated by author",
            "status": "progress",
        })

        self.assertRedirects(response, reverse("entry_list"))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Author update")

    def test_delete_requires_delete_permission_and_soft_deletes(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("entry_delete", args=[self.entry.pk]))
        self.assertEqual(response.status_code, 403)

        permission = Permission.objects.get(codename="delete_entry")
        self.editor.user_permissions.add(permission)
        self.client.force_login(self.editor)
        response = self.client.post(reverse("entry_delete", args=[self.entry.pk]))

        self.assertRedirects(response, reverse("entry_list"))
        self.entry.refresh_from_db()
        self.assertTrue(self.entry.is_deleted)

    def test_author_can_delete_own_entry_without_global_permission(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse("entry_delete", args=[self.entry.pk]))

        self.assertRedirects(response, reverse("entry_list"))
        self.entry.refresh_from_db()
        self.assertTrue(self.entry.is_deleted)

    def test_deleted_entries_are_hidden_from_public_list(self):
        self.entry.is_deleted = True
        self.entry.save()

        response = self.client.get(reverse("entry_list"))

        self.assertNotContains(response, "Alpha")
