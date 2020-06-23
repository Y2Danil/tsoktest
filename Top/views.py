from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Article, Comment, Rubric
from django.views.generic.base import View
from django.contrib.auth import logout
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login

def index(request):
  Articles = Article.objects.all()
  Rubrics = Rubric.objects.order_by('-id')
  return render(request, 'Top/list.html', {"Articles": Articles, 'Rubrics': Rubrics})

def poisck(request):
  title_poisck = request.POST['poisck']
  try:
    Articles = Article.objects.filter(title = title_poisck)
    Rubrics = Rubric.objects.order_by('-id')
  except:
    raise Http404('Ошибка 404')
  
  return render(request, 'Top/list.html', {"Articles": Articles, 'Rubrics': Rubrics})
    
def by_rubric(request, rubric_id):
  Articles = Article.objects.filter(rubric=rubric_id)
  Rubrics = Rubric.objects.order_by('-id')
  current_rubric = Rubric.objects.get(id=rubric_id)
  context = {'Articles': Articles, 'Rubrics': Rubrics, 'current_rubric': current_rubric}
  return render(request, 'Top/by_rubric.html', context)

def detail(request, article_id):
  try:
    a = Article.objects.get( id = article_id );
    Rubrics = Rubric.objects.all()
  except:
    raise Http404('Ошибка 404')
  
  Comments = a.comment_set.order_by('-pub_date')
  
  return render(request, 'Top/detail.html', {'Article': a, 'Comments': Comments, 'Rubrics': Rubrics})

def list_comment(request, article_id):
  try:
    a = Article.objects.get( id = article_id );
  except:
    raise Http404('Ошибка 404')
  
  a.comment_set.create(comment_text = request.POST['text_comment'], author = request.user.username )
  
  return HttpResponseRedirect( reverse('blog:detail', args=(a.id,)) )


# Авторизация и Регестрация
class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = '/accounts/login/'

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "Top/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")