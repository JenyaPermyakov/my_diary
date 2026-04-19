from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("entry_list")

class ProfileView(DetailView):
    template_name = "accounts/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        user = self.request.user

        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.save()

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email

        return initial