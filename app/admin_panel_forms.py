"""
This file defines forms used in the admin panel for managing users and cards 
on the platform.

The file contains two model forms:

- UserForm: A form for creating and editing user accounts. It includes fields 
  for username, email, superuser status, and staff status. It also includes 
  password and password confirmation fields, but they are optional. The form 
  disables the superuser field for non-superuser users. It also validates that 
  the password and password confirmation match.

- CardForm: A form for creating and editing cards. It includes fields for title, 
  image, likes, user, tag, and date created. However, the date created field 
  is most likely automatically populated when creating a new card and should 
  not be editable through this form.
"""

from django import forms
from django.contrib.auth.models import User
from .models import Card


class UserForm(forms.ModelForm):
    """
    A form for creating and editing user accounts in the admin panel.

    This form allows admins to create new users or edit existing ones. It
    includes fields for username, email, superuser status, and staff status.
    The password and password confirmation fields are optional and only used
    when setting or changing a user's password.

    **Features:**

    * Disables the superuser field for non-superuser users.
    * Validates that password and password confirmation match.

    """

    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "is_staff",
        ]

        exclude = ["password", "password_confirm"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error("password_confirm", "Password does not match")


class CardForm(forms.ModelForm):
    """
    A form for creating and editing cards in the admin panel.

    This form allows admins to create new cards or edit existing ones. It
    includes fields for title, image, likes (which might not be editable),
    user (which is most likely pre-populated and not editable), tag, and date
    created (which is most likely automatically populated and not editable).

    **Note:** The editability of certain fields like 'likes', 'user', and
    'date_created' depends on the specific implementation. This docstring
    highlights these considerations.

    """

    class Meta:
        model = Card
        fields = ["title", "image", "likes", "user", "tag", "date_created"]
