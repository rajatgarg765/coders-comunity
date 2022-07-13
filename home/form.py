from django import forms
from froala_editor.widgets import FroalaEditor
from blog.models import Post


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']