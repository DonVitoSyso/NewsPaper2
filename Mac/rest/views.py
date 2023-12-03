# from django.http import HttpResponse
# from django.views import View
# from .tasks import hello, printer
# from datetime import datetime, timedelta

from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from .tasks import complete_order
from .models import Order
from datetime import datetime


# главная страница - таблица заказов
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context


# форма нового заказа
class NewOrderView(CreateView):
    model = Order
    fields = ['products']  # единственное поле
    template_name = 'new.html'

    # после валидации формы, сохраняем объект,
    # считаем его общую стоимость
    # и вызываем задачу "завершить заказ" через минуту после вызова
    def form_valid(self, form):
        order = form.save()
        order.cost = sum([prod.price for prod in order.products.all()])
        order.save()
        complete_order.apply_async([order.pk], countdown=60)
        return redirect('/')


# представление для "кнопки", чтобы можно было забрать заказ
def take_order(request, oid):
    order = Order.objects.get(pk=oid)
    order.time_out = datetime.now()
    order.save()
    return redirect('/')






# class IndexView(View):
#     def get(self, request):
#         printer.delay(10)
#         hello.delay()
#         # printer.apply_async([10], countdown=5)
#         printer.apply_async([10],
#                             eta=datetime.now() + timedelta(seconds=5))
#         return HttpResponse('Hello!')
