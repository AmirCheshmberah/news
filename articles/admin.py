from django.contrib import admin
from . import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'author']


admin.site.register(models.Article, ArticleAdmin)