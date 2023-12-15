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
def search_auto(request):
    print('вызов функции')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        articles = Article.objects.filter(title__icontains=q)
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

class ArticleDetailView(DetailView):
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



# Человек не аутентифицирован - отправляем на другую страницу
from django.conf import settings
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

def index(request):
    categories = Article.categories #создали перечень категорий
    author_list = User.objects.all() #создали перечень авторов
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        if selected_author == 0: #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые
        selected_author = 0
        selected_category = 0
        articles = Article.objects.all()

    context = {'articles': articles, 'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category}

    return render(request,'news/news_list.html',context)




# def news_list(request):
    # article = Article.objects.all().first()
    # print('Автор новости', article.title, ':', article.author.account.gender)
    # context = {'article': article}
    # Пол автора новости
    # articles = Article.objects.filter(author=request.user.id)
    # print(articles)
    # context = {'article': articles}
    # Поиск статей по автору
    # articles = Article.objects.get(author=2)
    # print(articles.tags.all())
    # Поиск тегов по автору
    # article = Article.objects.filter(title__contains='Новость')
    # print(article)
    # for t in article.tags.all():
    #     print(t.title)

    # user_list = User.objects.all()
    # for user in user_list:
    #     print(Article.objects.filter(author=user))
    # print(user_list)
    # Список юзеров у которых есть новости, после печатаем все новости у всех юзеров

    # print(article.tags.all())
    # tag = Tag.objects.filter(title='General_IT').first()
    # tagged_news = Article.objects.filter(tags=tag)
    # print(tagged_news)
    # Поиск новостей по тегам

    # article = Article.objects.all()
    # context = {'article': article}
    # return render(request,'news/news_list.html', context)


# def news_detail(request, id):
#     article = Article.objects.filter(id=id)[0]
#     return HttpResponse(f'<h1>{article.title}</h1>')