from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from .models import Entry
from .forms import EntryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class EntryListView(ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    paginate_by = 4

    def get_ordering(self):
        sort = self.request.GET.get('sort', '-id')
        allowed = ['id', '-id', 'title', '-title', 'status']
        return sort if sort in allowed else '-id'

    def get_queryset(self):
        return Entry.objects.filter(is_deleted=False)

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_create.html"
    success_url = reverse_lazy("entry_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EntryDetailView(DetailView):
    model = Entry
    template_name = "entries/entry_detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        return Entry.objects.filter(is_deleted=False)

class EntryUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_update.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(is_deleted=False)

class EntryDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Entry
    template_name = "entries/entry_delete.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(is_deleted=False)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return redirect(self.success_url)

class DeletedEntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entries/deleted_entries.html"
    context_object_name = "entries"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, is_deleted=True)

def restore_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.is_deleted = False
    entry.save()
    return redirect('deleted_entries')

def hard_delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.delete()
    return redirect('deleted_entries')