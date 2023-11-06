from django.shortcuts import render

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, # refresh D4.5
    UpdateView, DeleteView # D4.5
)
from .models import (
                    Post,
                    Category # D4
                    )
# D 3.3
from datetime import datetime
# D4.2
from .filters import PostFilter
# D4.5
from django.urls import reverse_lazy
from .forms import PostForm
# D 5.3
from django.contrib.auth.mixins import PermissionRequiredMixin
# D 6
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import CatSub, Category


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'title' # D3.3
    ordering = 'date' # D3.3
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице D 4.2

    # D 3.3
    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        # D4.2
        # Добавляем в контекст объект фильтрации.
        # context['filterset'] = self.filterset
        return context

    # Переопределяем функцию получения списка товаров
    # D4.2
    '''def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs'''


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'


# D4
class PostSearch(ListView):
    template_name = 'search.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    # D4
    paginate_by = 6
    ordering = ['-date']

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=super().get_queryset())  # вписываем наш фильтр в контекст
        # context['categories'] = Category.objects.all()
        context['form'] = PostForm
        return context

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


# D4. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
# D5 LoginRequiredMixin в параметрах
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',) # D5.3
    # Проверка на права доступа
    template_name = 'new_create.html' # имя шаблона
    form_class = PostForm # класс формы
    # model = Post # класс для работы с валидацией ниже

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        validated = super().form_valid(form)
        return validated


# D5 LoginRequiredMixin в параметрах
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post',) # D5.3
    # Проверка на права доступа
    template_name = 'new_create.html'
    form_class = PostForm
    model = Post

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    # def get_object(self, **kwargs):
    #     id = self.kwargs.get('pk')
    #     post = Post.objects.get(pk=id)
    #     post.isUpdated = True
    #     return post


# D5 LoginRequiredMixin в параметрах
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',) # D5.3
    # Проверка на права доступа
    success_url = '/news/'
    template_name = 'new_delete.html'

    # ИЗ ЭТАЛОНА
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# D5 LoginRequiredMixin в параметрах
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',) # D5.3
    # Проверка на права доступа
    template_name = 'new_create.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        validated = super().form_valid(form)

        return validated


# D6
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            CatSub.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            CatSub.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            CatSub.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
