from django import forms
from catalog.models import ProductFilial, Product, Filial

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
