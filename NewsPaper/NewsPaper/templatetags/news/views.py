from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from flask import redirect

from NewsPaper.accounts.models import Category
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

class NewsCreate(CreateView):
    form_class = PostForm
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        return super().form_valid(form)

class ArticleCreate(CreateView):
    form_class = PostForm
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


def toggle_subscription(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.user in category.subscribers.all():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)
    return redirect('category_news', category_id=category_id)

def news_detail():
    return None


def news_list():
    return None


def become_author():
    return None