from django.urls import path
# Импортируем созданное нами представление
from .views import (
                     PostsList, PostDetail, PostSearch,
                     PostCreate, PostDelete, PostUpdate, # D4
                     ArticleCreate,
                     CategoryList,  # subscriptions,                      # D6
                     )
# D8_3
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # D8_3 начало
   path('', cache_page(60*1)(PostsList.as_view()), name='news_list'),  # кэширование гл страницы 1 мин
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='new'), # кэширование страницы с новостями 5 мин
   #path('<int:pk>', PostDetail.as_view(), name='new'),
   # D8_3 конец
   # D4
   path('search/', PostSearch.as_view(), name='search'),
   path('search/<int:pk>', PostSearch.as_view(), name='new_search'),
   path('new/create/', PostCreate.as_view(), name='new_create'),
   path('new/<int:pk>/edit', PostUpdate.as_view(), name='new_update'),
   path('new/<int:pk>/delete', PostDelete.as_view(), name='new_delete'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit', PostUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
   #path('subscriptions/', subscriptions, name='subscriptions'),                  # D6
   path('subscriptions/', CategoryList.as_view(), name='subscriptions')
]
