from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
    list_display = ['title','created','updated','slug']
    search_fields=['title','body']
    list_filter=['updated']
    prepopulated_fields = {'slug':['title']}
    raw_id_fields = ['user']




admin.site.register(Post,PostAdmin)