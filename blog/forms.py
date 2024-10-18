from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text', 'pub_date',
            'location', 'category', 'is_published', 'image'
        ]
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
