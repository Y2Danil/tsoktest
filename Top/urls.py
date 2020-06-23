from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
  path('', views.index, name='index'),
  path('article/', views.poisck, name='poisck'),
  path('rubric/<int:rubric_id>/', views.by_rubric, name='by_rubric'),
  path('article/<int:article_id>/', views.detail, name='detail'),
  path('article/<int:article_id>/list_comment/', views.list_comment, name='list_comment'),
  path('register/', views.RegisterFormView.as_view(), name='register')
]