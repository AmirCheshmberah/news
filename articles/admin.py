from django.contrib import admin
from . import models


class CommentInline(admin.StackedInline):
    model = models.Comment
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]
    list_display = ['title', 'body', 'author']


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment)