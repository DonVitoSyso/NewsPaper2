from django.urls import path
# Импортируем созданное нами представление
from .views import (
   ProductsList, ProductDetail, ProductCreate, # D4.5 Refresh
   ProductUpdate, ProductDelete, # D4.5
   subscriptions, # D6.3
)
# D 8.2
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', ProductsList.as_view(), name='product_list'),  # refresh D4.5
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # path('<int:pk>', ProductDetail.as_view(), name='product_detail'), # refresh D4.5
   # D 8.2
   # добавим кэширование на детали товара. Раз в 10 минут товар будет записываться в кэш для экономии ресурсов.
   # path('<int:pk>/', cache_page(60*10)(ProductDetail.as_view()), name='product_detail'),
   path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
   # D4.5
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   # D6.3
   path('subscriptions/', subscriptions, name='subscriptions'),
]
