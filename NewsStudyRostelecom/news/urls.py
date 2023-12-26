from django.urls import path

from . import views
urlpatterns = [
    path('', views.news, name='news_index'),
    path('list/', views.index, name='news_list'),
    # path('/news/list/search/', views.search_news, name='search_news'),
    path('/news/list/search_auto/', views.search_auto, name='search_auto'),
    path('list/<int:pk>/', views.ArticleDetailView.as_view(), name='news_detail'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='news_delete'),
    # path('list/', views.news_list, name='news_list'),
    path('news_1/', views.news_1, name='news_1'),
    path('news_2/', views.news_2, name='news_2'),
    path('news_3/', views.news_3, name='news_3'),
    path('create', views.create_article, name='create_article'),
    #path('pagination',views.pagination,name='pagination'),
]
