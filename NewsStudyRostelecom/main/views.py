from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import News, Product


def index(request):
    return render(request,'main/index.html')
def news(request):
    return render(request,'main/news.html')

def news_1(request):
    return render(request,'main/news_1.html')
def news_2(request):
    return render(request,'main/news_2.html')
def news_3(request):
    return render(request,'main/news_3.html')

def examples(request):
    # value = -10
    # n1 = News('Новость 1','Текст 1','07.11.23')
    # n2 = News('Новость 2','Текст 2','01.11.23')
    # l = [n1, n2]
    # d = {1: 'один', 'Два': 2}
    #
    # context = {'title': 'Страница главная',
    #            'Header1': 'Заголовок страницы',
    #            'numbers': l,
    #            'dictionary': d,
    #            'value':value,
    #            }
    # context['пример']= 'Example'

    if request.method == 'POST':
        print('Получили post-Запрос!')
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title,float(price),int(quantity))
        print('Создан товар:',new_product.title, 'Общая сумма:',new_product.amount())
    else:
        print('Получили get-Запрос!')
    water = Product('Добрый-минералка', 43, 2)
    chocolate = Product('Шоколадка', 80, 1)

    colors = ['red','blue','golden','black']
    context = {
        'colors':colors,
        'water': water,
        'chocolate':chocolate,
    }
    return render(request,'main/examples.html', context)

def get_demo(request,a,operation,b):
    match operation:
        case 'plus':
            result = int(a)+ int(b)
        case 'minus':
            result = int(a) - int(b)
        case 'multiply':
             result = int(a) * int(b)
        case 'divide':
            result = int(a) / int(b)
        case _:
            return HttpResponse(f'Неверная команда')
    return HttpResponse(f'Вы ввели: {a} и {b} <br>Результат {operation}: {result}')


def about(request):
    return HttpResponse('<h1> о нас </h1>')


def contacts(request):
    return HttpResponse('<h1> контакты </h1>')


def sidebar(request):
    return render(request,'main/sidebar.html')

def user_account(request):
    return render(request,'main/user_account.html')
def about(request):
    return render(request,'main/about.html')


def custom_404(request, exception):
    # return render(request,'main/sidebar.html')
    return HttpResponse(f'Введен неверный запрос, или страница еще в разработке:{exception}')

import git
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_server(request):
    if request.method == "POST":
        local_dir = '/home/proverym/DjangoNewsRostelecom'
        repo = git.Repo(local_dir)
        repo.remotes.origin.pull()
        return HttpResponse("PythonAnywhere server updated successfully")
    else:
        return HttpResponse("Вы попали не туда")