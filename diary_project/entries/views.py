from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from .models import Entry
from .forms import EntryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = "-id"
    paginate_by = 4

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_create.html"
    success_url = reverse_lazy("entry_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = "entries/entry_delete.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_update.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "entries/entry_detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)