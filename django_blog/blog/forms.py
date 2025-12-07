from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagWidget  # Import TagWidget from taggit
from .models import Comment, Post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]  # Only include content, as post and author will be set programmatically
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Enter your comment"}
            ),
        }

    # Example validation for comment length
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 3:
            raise forms.ValidationError("Comment is too short!")
        return content


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]  # Include tags in the form
        widgets = {
            "tags": TagWidget(),  # Use TagWidget for tag input
        }