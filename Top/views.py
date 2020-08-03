# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login, logout
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from .forms import RegUserForm
from .models import Article, Comment, Rubric


def index(request):
  try:
    Articles = Article.objects.all()
    Rubrics = Rubric.objects.order_by('-id')
    return render(request, 'Top/list.html', {"Articles": Articles, 'Rubrics': Rubrics})
  except:
    return render(request, 'Top/404.html')

def poisck(request):
  title_poisck = request.POST['poisck']
  try:
    Articles = Article.objects.filter(title = title_poisck)
    Rubrics = Rubric.objects.order_by('-id')
    
    return render(request, 'Top/list.html', {"Articles": Articles, 'Rubrics': Rubrics})
  except:
    return render(request, 'Top/404.html')
    
def by_rubric(request, rubric_id):
  try:
    Articles = Article.objects.filter(rubric=rubric_id)
    Rubrics = Rubric.objects.order_by('-id')
    current_rubric = Rubric.objects.get(id=rubric_id)
    context = {'Articles': Articles, 'Rubrics': Rubrics, 'current_rubric': current_rubric}
    
    return render(request, 'Top/by_rubric.html', context)
  except:
    return render(request, 'Top/404.html')

def detail(request, article_id):
  try:
    a = Article.objects.get( id = article_id );
    Rubrics = Rubric.objects.all()
  except:
    return render(request, 'Top/404.html')
  
  Comments = a.comment_set.order_by('-pub_date')
  
  return render(request, 'Top/detail.html', {'Article': a, 'Comments': Comments, 'Rubrics': Rubrics})

def likes_detail(request, article_id):
  try:
    a = Article.objects.get( id = article_id );
  except:
    return render(request, 'Top/404.html')
  
  if request.method == 'POST':
    if request.user.is_authenticated:
      user_tags = User.objects.filter(user_like = article_id)
      current_user = request.user
      if current_user not in user_tags:
        try:
          a.likes += 1
          a.like_status.add(current_user)
          a.save()
            
          return HttpResponseRedirect(reverse('blog:detail', args=(a.id,)))
        except:
          return render(request, 'Top/404.html')
      else:
        try:
          a.likes -= 1
          a.like_status.remove(current_user)
          a.save()
            
          return HttpResponseRedirect(reverse('blog:detail', args=(a.id,)))
        except:
          return render(request, 'Top/404.html')
    else:
      return HttpResponseRedirect(reverse('blog:detail', args=(a.id,)))

def list_comment(request, article_id):
  try:
    a = Article.objects.get( id = article_id );
  except:
    return render(request, 'Top/404.html')
  
  a.comment_set.create(comment_text = request.POST['text_comment'], author = request.user.username )
  
  return HttpResponseRedirect( reverse('blog:detail', args=(a.id,)) )

# Авторизация и Регестрация
class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = '/accounts/login/'

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
      
    #def form_invalid(self, form):
        #return super(RegisterFormView, self).form_invalid(form)
        

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
