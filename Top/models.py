import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone

class Article(models.Model):
  image = models.ImageField('Картинка', upload_to='images/', null=True, blank=True)
  rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
  create_author = models.CharField('Автор идеи', max_length=100)
  title = models.CharField('Название статьи', max_length=200)
  text = models.TextField('Текст статьие', blank=True, null=True)
  created_date = models.DateTimeField(db_index=True, auto_now_add=True)
  published_date = models.DateTimeField(blank=True, null=True, db_index=True, auto_now_add=True)

  class Meta:
    verbose_name = 'Статья'
    verbose_name_plural = 'Статьи'
    ordering = ['-published_date']
    
  def new_article(self):
    return self.published_date >= (timezone.now() - datetime.timedelta(days = 7))

  def publish(self):
    self.published_date = timezone.now()
    self.save()

  def __str__(self):
    return self.title

class Comment(models.Model):
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  author = models.CharField('Автор комментария', max_length=60)
  comment_text = models.TextField('Текст комметария', max_length=500)
  pub_date = models.DateTimeField('Дата публикации', db_index=True, auto_now_add=True)

  class Meta:
    verbose_name = 'Комментарий'
    verbose_name_plural = 'Комментарии'

  def __str__(self):
    return self.author
  
class Rubric(models.Model):
  name = models.TextField('Название', max_length=30, db_index=True)
  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'Рубрики'
    verbose_name = 'Рубрика'
    ordering = ['name']