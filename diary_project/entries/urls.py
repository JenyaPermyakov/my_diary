from django.urls import path
from .views import EntryListView, EntryDetailView, EntryCreateView, EntryUpdateView, EntryDeleteView, \
    DeletedEntryListView, restore_entry, hard_delete_entry

urlpatterns = [
    path("", EntryListView.as_view(), name="entry_list"),
    path("create/", EntryCreateView.as_view(), name="entry_create"),
    path("<int:pk>/", EntryDetailView.as_view(), name="entry_detail"),
    path("<int:pk>/edit/", EntryUpdateView.as_view(), name="entry_edit"),
    path("<int:pk>/delete/", EntryDeleteView.as_view(), name="entry_delete"),

    path("deleted/", DeletedEntryListView.as_view(), name="deleted_entries"),

    path("<int:pk>/restore/", restore_entry, name="entry_restore"),
    path("<int:pk>/hard_delete/", hard_delete_entry, name="entry_hard_delete"),
]