from django import forms
from .models import Service


class ServiceCreateForm(forms.ModelForm):
    REPETITION_TERM_CHOICES = (1, 'One-Time'), (2, 'Weekly'), (3, 'Monthly'), (4, 'Yearly')
    PRIVACY_STATUS_CHOICES = (1, 'Public'), (2, 'Private')
    PARTICIPANT_PICKING = (1, 'Free'), (2, 'Pick participants')

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'location',
    }))
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mb-0 p-3 h100 bg-greylight lh-16',
        'rows': 5,
        'placeholder': 'Write your description about this service...',
        'spellcheck': 'false',
    }))
    participant_limit = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    repetition_term = forms.ChoiceField(choices=REPETITION_TERM_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    privacy_status = forms.ChoiceField(choices=PRIVACY_STATUS_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    participant_picking = forms.ChoiceField(choices=PARTICIPANT_PICKING, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mb-0 p-3 h100 bg-greylight lh-16',
        'rows': 5,
        'placeholder': 'Write here about the content of your service...',
        'spellcheck': 'false',
    }))

    class Meta:
        model = Service
        fields = (
            'title',
            'location',
            'start_date',
            'end_date',
            'description',
            'participant_limit',
            'repetition_term',
            'privacy_status',
            'participant_picking',
            'content',
        )
