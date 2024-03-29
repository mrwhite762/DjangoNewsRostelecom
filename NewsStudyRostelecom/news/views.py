from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from .models import *
from django.db import connection, reset_queries
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
from .forms import *
import json


# def search_news(request):
#     print('Функция')
#     query = request.GET.get('q')

#URL:    path('search_auto/', views.search_auto, name='search_auto'),
# def search_auto(request):
#     print('вызов функции')
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         q = request.GET.get('term', '')
#         articles = Article.objects.filter(title__icontains=q)
#         results = []
#         for a in articles:
#             results.append(a.title)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data,mimetype)

from .utils import ViewCountMixin
#!!!!!можно про миксиин записи просмотра статьи. проговорить в какой моменгт он вызывается
class ArticleDetailView(ViewCountMixin, DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text','tags']

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index')
    template_name = 'news/delete_article.html'


from users.utils import check_group #импортировли декоратор
from django.conf import settings # Человек не аутентифицирован - отправляем на другую страницу
@check_group('Authors')
@login_required(login_url=settings.LOGIN_URL)
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #Проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #Сохраняем в БД
                form.save_m2m()  # сохраняем теги
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)
                return redirect('/news/list')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})



def news(request):
    return render(request,'news/news.html')

def news_1(request):
    return render(request,'news/news_1.html')
def news_2(request):
    return render(request,'news/news_2.html')
def news_3(request):
    return render(request,'news/news_3.html')

# def index(request):
#     categories = Article.categories #создали перечень категорий
#     author_list = User.objects.all() #создали перечень авторов
#     if request.method == "POST":
#         selected_author = int(request.POST.get('author_filter'))
#         selected_category = int(request.POST.get('category_filter'))
#         if selected_author == 0: #выбраны все авторы
#             articles = Article.objects.all()
#         else:
#             articles = Article.objects.filter(author=selected_author)
#         if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
#             articles = articles.filter(category__icontains=categories[selected_category-1][0])
#     else: #если страница открывется впервые
#         selected_author = 0
#         selected_category = 0
#         articles = Article.objects.all()
#
#     context = {'articles': articles, 'author_list':author_list, 'selected_author':selected_author,
#                'categories':categories,'selected_category': selected_category}
#
#     return render(request,'news/news_list.html',context)

from time import time
from django.core.paginator import Paginator
# def pagination(request):
#     articles = Article.objects.all()
from django.utils.translation import gettext as _
def index(request):
    categories = Article.categories #создали перечень категорий
    author_list = User.objects.all() #создали перечень авторов
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        request.session['author_filter'] = selected_author
        request.session['category_filter'] = selected_category
        if selected_author == 0: #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые или нас переадресовала сюда функция поиск
        value = request.session.get('search_input')  # вытаскиваем из сессии значение поиска
        if value != None: #если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(title__icontains=value)
            # del request.session['search_input'] #чистим сессию, чтобы этот фильтр не "заело"
        else:
            selected_author = request.session.get('author_filter')
            selected_category = request.session.get('category_filter')
            articles = Article.objects.all()
            if selected_author != None and int(selected_author) != 0:  # если не пустое - находим нужные ноновсти
                articles = articles.filter(author=selected_author)
            else:
                selected_author = 0
            if selected_category != None and int(selected_category) != 0:
                articles = articles.filter(category__icontains=categories[selected_category-1][0])
            else:
                selected_category = 0
    #сортировка от свежих к старым новостям
    articles=articles.order_by('-date')
    total = len(articles)
    p = Paginator(articles,5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    title = _('Заголовок страницы новости-индекс')
    demo_variable = _('текст демо-переменной')
    print('Значение переменной:', demo_variable)
    context = {'articles': page_obj, 'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category, 'total':total,
               'title':title
               }

    return render(request,'news/news_list.html',context)

def news_search(request):
    news = {}
    if request.method == 'POST':
        print(request.POST)
        news = Article.objects.filter(title=request.POST.get('search_input')).order_by('date')
    context = {'news': news}
    return render(request, 'news/news_search.html', context)

def search_auto(request):
    news = {}
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        news = Article.objects.filter(title__icontains=q)
        results = []
        for n in news:
            results.append(n.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# def index(request):
#     categories = Article.categories #создали перечень категорий
#     author_list = User.objects.all() #создали перечень авторов
#     if request.method == "POST":
#         selected_author = int(request.POST.get('author_filter'))
#         selected_category = int(request.POST.get('category_filter'))
#         request.session['selected_author'] = selected_author
#         request.session['selected_category'] = selected_category
#         if selected_author == 0: #выбраны все авторы
#             articles = Article.objects.all()
#         else:
#             articles = Article.objects.filter(author=selected_author)
#         if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
#             articles = articles.filter(category__icontains=categories[selected_category-1][0])
#     else: #если страница открывется впервые или нас переадресовала сюда функция поиск
#         selected_author = request.session.get('selected_author')
#         if selected_author != None: #если не пустое - находим нужные ноновсти
#             articles = Article.objects.filter(author=selected_author)
#         else:
#             selected_author = 0
#         selected_category = 0
#         value = request.session.get('search_input') #вытаскиваем из сессии значение поиска
#         if value != None: #если не пустое - находим нужные ноновсти
#             articles = Article.objects.filter(title__icontains=value)
#             del request.session['search_input'] #чистим сессию, чтобы этот фильтр не "заело"
#         else:
#             #если не оказалось таокго ключика или запрос был кривой - отображаем все элементы
#             articles = Article.objects.all()

