from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Article, Comment
from .forms import ArticleEditForm, ArticleCreateForm, CommentForm

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

# class ArticleDetailGet(DetailView):
#     model = Article
#     template_name = 'article_detail.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         return context

# class ArticleDetailPost(SingleObjectMixin, FormView):
#     model = Article
#     form_class = CommentForm
#     template_name = 'article_detail.html'
    
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.article = self.object
#         comment.author = self.request.user
#         comment.save()
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse('article_detail', kwargs={'pk': self.object.pk})

# class ArticleDetailView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         view = ArticleDetailGet.as_view()
#         return view(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         view = ArticleDetailPost.as_view()
#         return view(request, *args, **kwargs)

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={'pk': self.kwargs['pk']})

@login_required
def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.article = article
            form.save()
            return redirect(article)
    else:
        form = CommentForm()
    return render(request, 'article_detail.html', {'article':article,'form':form})

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    template_name = 'article_edit.html'

@login_required
def article_update_view(request, pk):
    object = get_object_or_404(Article, pk=pk)
    
    if object.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ArticleEditForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(object)
    else:
        form = ArticleEditForm(instance=object)
    return render(request, 'article_edit.html', {'form':form})

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    success_url = reverse_lazy('article_list')

@login_required
def article_delete_view(request, pk):
    object = get_object_or_404(Article, pk=pk)

    if object.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        object.delete()
        return redirect("article_list")

    return render(request, "article_delete.html", {'object':object})