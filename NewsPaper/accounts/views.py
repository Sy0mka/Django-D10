from django.core.paginator import Paginator
from django.shortcuts import render

from .filters import PostFilter


def news_search(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    paginator = Paginator(f.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_search.html', {
        'filter': f,
        'page_obj': page_obj
    })