from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Article
from .forms import ArticleEditForm, ArticleCreateForm

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'body',)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    template_name = 'article_new.html'

@login_required
def article_create_view(request):
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            article = form.save()
            return redirect(article)
    else:
        form = ArticleCreateForm()
    return render(request, 'article_new.html', {'form':form})
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'

def article_list_view(request):
    all = Article.objects.filter(author=request.user)
    return render(request, 'article_list.html', {'article_list':all})

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

@login_required
def article_detail_view(request, pk):
    object = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'object':object})

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'body', )
    template_name = 'article_edit.html'

@login_required
def article_update_view(request, pk):
    object = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleEditForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(object)
    else:
        form = ArticleEditForm(instance=object)
    return render(request, 'article_edit.html', {'form':form})

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy('article_list')

@login_required
def article_delete_view(request, pk):
    object = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        object.delete()
        return redirect("article_list")

    return render(request, "article_delete.html", {'object':object})