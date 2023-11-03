from django import forms
from .models import Product
# D4.4
from django.core.exceptions import ValidationError



class ProductForm(forms.ModelForm):
   # D4.4
   description = forms.CharField(min_length=20)

   class Meta:
      model = Product
      # fields = '__all__' # D4.3
      # D4.4
      fields = [
         'name',
         'description',
         'category',
         'price',
         'quantity',
      ]

   # D4.4
   def clean(self):
      cleaned_data = super().clean()
      description = cleaned_data.get("description")
      name = cleaned_data.get("name")

      # D4.4_2
      '''
      if description is not None and len(description) < 20:
         raise ValidationError({
            "description": "Описание не может быть менее 20 символов."
         })
      '''
      if name == description:
         raise ValidationError(
            "Описание не должно быть идентично названию."
         )

      return cleaned_data

   # D 4.3
   '''
   class ProductForm(forms.Form):
      name = forms.CharField(label='Name')
      description = forms.CharField(label='Description')
      quantity = forms.IntegerField(label='Quantity')
      category = forms.ModelChoiceField(
        label='Category', queryset=Category.objects.all(),
      )
      price = forms.FloatField(label='Price')
   '''
