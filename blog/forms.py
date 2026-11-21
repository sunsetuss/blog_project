from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article

        fields = [
            'title',
            'content',
            'category',
            'tags',
            'status',
        ]

        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 12,
            }),

            'tags': forms.SelectMultiple(attrs={
                'size': 6,
            }),
        }
