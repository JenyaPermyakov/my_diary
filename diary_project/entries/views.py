from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from .models import Entry
from .forms import EntryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404


# 📌 Главная (НЕ показывает удалённые)
class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = "-id"
    paginate_by = 4

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, is_deleted=False)


# 📌 Создание
class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_create.html"
    success_url = reverse_lazy("entry_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# 📌 МЯГКОЕ УДАЛЕНИЕ
class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = "entries/entry_delete.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, is_deleted=False)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return redirect(self.success_url)


# 📌 Редактирование
class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "entries/entry_update.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, is_deleted=False)


# 📌 Детали
class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "entries/entry_detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, is_deleted=False)


# 📌 КОРЗИНА
class DeletedEntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entries/deleted_entries.html"
    context_object_name = "entries"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, is_deleted=True)


# 📌 ВОССТАНОВЛЕНИЕ
def restore_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.is_deleted = False
    entry.save()
    return redirect('deleted_entries')


# 📌 УДАЛИТЬ НАВСЕГДА
def hard_delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    Entry.objects.filter(pk=entry.pk).delete()
    return redirect('deleted_entries')