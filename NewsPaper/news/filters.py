from django_filters import (FilterSet, CharFilter, ModelChoiceFilter,
                            DateFilter,
                            ) # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Category
from django import forms

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    date = DateFilter(
        label='Дата',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control pure-input-1-2'}),
    )
    # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то что запросил пользователь
    title = CharFilter(
        lookup_expr='icontains',
        label='Название статьи',
        # D6 для оформеления поиска
        widget=forms.TextInput(attrs={'class': 'form-control pure-input-1-2', 'placeholder': 'Post Title'}),
    )
    # мы хотим чтобы нам выводило имя из списка
    '''author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы',
        # D6
        widget=forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
    )'''
    # мы хотим чтобы нам выводило категория списком
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
        # D6
        widget=forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
    )

    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться
    # (т. е. подбираться) информация о товарах
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация
       fields = ['date', 'title', 'author', 'category']
