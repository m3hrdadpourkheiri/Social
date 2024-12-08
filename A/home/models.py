from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str: # این متد برای این است که در ادمین پنل فیلد تایتل را در لیست پست ها ببینیم
        return self.title

    def get_absolute_url(self):
        return reverse('home:post_detail',args=(self.id,self.slug))