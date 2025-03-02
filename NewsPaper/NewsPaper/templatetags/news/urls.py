from django.urls import path, include
from . import views
from .views import NewsCreate, PostUpdate, PostDelete, ArticleCreate

urlpatterns = {
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('accounts/', include('allauth.urls')),
    path('become-author/', views.become_author, name='become_author'),
    path('category/<int:category_id>/subscribe/', views.toggle_subscription,
         name='toggle_subscription')
}
