from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title = models.TextField()
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta: #this class is for order by a field this model completely
        ordering = ('-created','title')


    def __str__(self) -> str: # این متد برای این است که در ادمین پنل فیلد تایتل را در لیست پست ها ببینیم
        return self.title

    def get_absolute_url(self):
        return reverse('home:post_detail',args=(self.id,self.slug))
    
    def likes_count(self):
        return self.pvote.count()
    
    def user_can_like(self,user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        else:
            return False

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomments')
    reply = models.ForeignKey('Comment',on_delete=models.CASCADE,related_name='rcomment',blank=True,null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'
    
class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uvotes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pvote')
    
    def __str__(self):
        return f'{self.user} like {self.post.slug}'
    
