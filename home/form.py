from django import forms

from blog.models import Post


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']