from django import forms
from django.forms import Textarea
from .models import Product, Comment, Order
from django.contrib.auth.models import User


class ComForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['com_text',]
        labels = {
            "com_text": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['com_text'].widget = Textarea(attrs={'rows': 3})


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery', 'comment',]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        help_texts = {
            'username': None,
        }
