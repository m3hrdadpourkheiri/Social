from django.contrib import admin
from .models import Post,Comment,Vote

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
    list_display = ['title','created','updated','slug']
    search_fields=['title','body']
    list_filter=['updated']
    prepopulated_fields = {'slug':['title']}
    raw_id_fields = ['user']

class CommentAdmin(admin.ModelAdmin):
    list_display=['user','post','is_reply','created']
    raw_id_fields=['post','user','reply']

class VoteAdmin(admin.ModelAdmin):
    list_display=['user','post']
    raw_id_fields=['post','user']

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Vote,VoteAdmin)