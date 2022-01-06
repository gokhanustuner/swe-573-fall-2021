from django import forms
from .models import Service
from django.utils.translation import gettext_lazy as _

REPETITION_TERM_CHOICES = (1, 'One-Time'), (2, 'Weekly'), (3, 'Monthly'), (4, 'Yearly')
PRIVACY_STATUS_CHOICES = (1, 'Public'), (2, 'Private')
PARTICIPANT_PICKING_CHOICES = (1, 'Free'), (2, 'Pick participants')
CATEGORY_CHOICES = (1, _('Food')), (2, _('Music')), (3, _('Education')), (4, _('Arts')), (5, _('Entertainment')), \
                   (6, _('Technical')), (7, _('Craftsmanship')), (8, _('Repair and maintenance'))


class ServiceCreateForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'location',
        'style': 'padding: 0.375rem 1.75rem 0.375rem 0.75rem;',
    }))
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    credit = forms.IntegerField(widget=forms.TextInput(attrs={
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
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    repetition_term = forms.ChoiceField(choices=REPETITION_TERM_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    privacy_status = forms.ChoiceField(choices=PRIVACY_STATUS_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    participant_picking = forms.ChoiceField(choices=PARTICIPANT_PICKING_CHOICES, widget=forms.Select(attrs={
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
            'credit',
            'description',
            'participant_limit',
            'category',
            'repetition_term',
            'privacy_status',
            'participant_picking',
            'content',
        )


class ServiceUpdateForm(forms.ModelForm):
    CANCELLATION_CHOICES = (0, 'No'), (1, 'Yes')

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'location',
        'style': 'padding: 0.375rem 1.75rem 0.375rem 0.75rem;',
    }))
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    credit = forms.IntegerField(widget=forms.TextInput(attrs={
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
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    repetition_term = forms.ChoiceField(choices=REPETITION_TERM_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    privacy_status = forms.ChoiceField(choices=PRIVACY_STATUS_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    participant_picking = forms.ChoiceField(choices=PARTICIPANT_PICKING_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    cancelled = forms.ChoiceField(choices=CANCELLATION_CHOICES, widget=forms.Select(attrs={
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
            'credit',
            'description',
            'participant_limit',
            'category',
            'repetition_term',
            'privacy_status',
            'participant_picking',
            'cancelled',
            'content',
        )
