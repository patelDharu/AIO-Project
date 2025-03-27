from django import forms
from User.models import sub_category_one, sub_category

# Form for adding Sub Category One
class SubCategoryOneForm(forms.ModelForm):
    class Meta:
        model = sub_category_one
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sub Category One Name'})
        }

# Form for adding Sub Category
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = sub_category
        fields = ['name', 'category', 'sub_category_one']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sub Category Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sub_category_one': forms.Select(attrs={'class': 'form-control'})
        }
