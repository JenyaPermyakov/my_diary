from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from .models import Entry
from .forms import EntryForm
from django.urls import reverse_lazy

class EntryListView(ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = "-id"
    paginate_by = 4

class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_create.html"
    success_url = reverse_lazy("entry_list")

class EntryDeleteView(DeleteView):
    model = Entry
    template_name = "entries/entry_delete.html"
    success_url = reverse_lazy("entry_list")

class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_update.html"
    success_url = reverse_lazy("entry_list")

class EntryDetailView(DetailView):
    model = Entry
    template_name = "entries/entry_detail.html"
    context_object_name = "entry"
