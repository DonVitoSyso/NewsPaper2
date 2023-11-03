from django import forms
from .models import Post
# D4.4
from django.core.exceptions import ValidationError



class PostForm(forms.ModelForm):
   # D4.4
   text = forms.CharField(min_length=20)

   class Meta:
      model = Post
      # fields = '__all__' # D4.3
      # D4.4
      fields = ['title', 'text', 'author', 'category']
      widgets = {
         'author': forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
         'category': forms.SelectMultiple(attrs={'class': 'form-control pure-input-1-2'}),
         'title': forms.TextInput(attrs={'class': 'form-control pure-input-1-2', 'placeholder': 'Post Title'}),
         'text': forms.Textarea(attrs={'class': 'form-control pure-input-1-2'}),
      }

   # D4.4
   def clean(self):
      cleaned_data = super().clean()
      text = cleaned_data.get("text")
      title = cleaned_data.get("title")

      # D4.4_2
      '''
      if text is not None and len(text) < 20:
         raise ValidationError({
            "text": "Описание не может быть менее 20 символов."
         })
      '''
      if title == text:
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
