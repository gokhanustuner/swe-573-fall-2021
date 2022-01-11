from django import forms
from members.models import Member, MemberProfile


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600',
        'placeholder': 'Your Email Address',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3',
        'placeholder': 'Password'
    }))


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600',
        'placeholder': 'Your Name',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600',
        'placeholder': 'Your Email Address',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Member
        fields = (
            'full_name',
            'email',
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MemberProfileUpdateForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'location',
        'style': 'padding: 0.375rem 1.75rem 0.375rem 0.75rem;',
    }))
    personal_characteristics = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mb-0 p-3 h100 bg-greylight lh-16',
        'rows': 5,
        'placeholder': 'Write here about the content of your personal characteristics...',
        'spellcheck': 'false',
    }))
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mb-0 p-3 h100 bg-greylight lh-16',
        'rows': 5,
        'placeholder': 'Write here about the content of your personal characteristics...',
        'spellcheck': 'false',
    }))
    talents = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mb-0 p-3 h100 bg-greylight lh-16',
        'rows': 5,
        'placeholder': 'Write here about the content of your personal characteristics...',
        'spellcheck': 'false',
    }))
    photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'input-file',
        'id': 'file',
    }))

    class Meta:
        model = MemberProfile
        fields = (
            'location',
            'personal_characteristics',
            'bio',
            'talents',
            'photo',
        )
