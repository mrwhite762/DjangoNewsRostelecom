from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('news/', views.news, name='news'),
    path('news_1/', views.news_1, name='news_1'),
    path('news_2/', views.news_2, name='news_2'),
    path('news_3/', views.news_3, name='news_3'),
    path('examples/',views.examples,name='examples'),
    path('calc/<int:a>/<slug:operation>/<int:b>',views.get_demo),
    # 127.0.0.1:8000/calc/10/power/2
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contact'),
    path('sidebar/', views.sidebar),
    path('user_account/', views.user_account, name='user_account'),

]
