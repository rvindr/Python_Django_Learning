from django import forms
from .models import Item

class AddItems(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('is_sold','created_by')
        widgets = {
            'category':forms.Select(attrs={
                'class':'form-control'
            }),
            'name':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control'
            }),
            'price':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'image':forms.FileInput(attrs={
                'class':'form-control'
            })
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('category','is_sold','created_by')
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control'
            }),
            'price':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'image':forms.FileInput(attrs={
                'class':'form-control'
            })
        }

