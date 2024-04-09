from django import forms
from django.contrib.auth.models import User
from .models import Card

# from .models import Card


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=False)

    # Originally there's only this class inside UserForm
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "is_superuser",
            "is_staff",
        ]

        exclude = ["password", "password_confirm"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UserForm, self).__init__(*args, **kwargs)
        if user is not None and not user.is_superuser:
            self.fields["is_superuser"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error("password_confirm", "Password does not match")


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["title", "image", "likes", "user", "tag", "date_created"]
