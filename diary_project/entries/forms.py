from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['title', 'content', 'status']

        labels = {
            'title': 'Название',
            'content': 'Описание',
            'status': 'Статус',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название задачи',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание задачи',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

