from django import forms
from .models import Article, Comment

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body',)

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)