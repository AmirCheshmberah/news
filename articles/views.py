from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

def article_list_view(request):
    all = Article.objects.filter(author=request.user)
    return render(request, 'article_list.html', {'article_list':all})

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'body', )
    template_name = 'article_edit.html'

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy('article_list')