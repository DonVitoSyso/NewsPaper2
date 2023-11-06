from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# D5.5 - start
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
# D 6
from django.core.mail import EmailMultiAlternatives


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name="common")
        user.groups.add(authors)
        # D6
        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email, "vitosyso@yandex.ru"]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        # D6
        return user
# D5.5 - end


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )