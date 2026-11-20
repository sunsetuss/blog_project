from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F

from .models import Article, Category


def article_list(request):
    articles = Article.objects.filter(
        status='published'
    ).select_related(
        'category', 'author'
    ).prefetch_related('tags')

    search = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if search:
        articles = articles.filter(title__icontains=search)

    if category_id:
        articles = articles.filter(category_id=category_id)

    categories = Category.objects.all()

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/article_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
    })


def article_detail(request, pk):
    Article.objects.filter(
        pk=pk,
        status='published'
    ).update(view_count=F('view_count') + 1)

    article = get_object_or_404(
        Article.objects.select_related(
            'category', 'author'
        ).prefetch_related('tags'),
        pk=pk,
        status='published'
    )

    return render(request, 'blog/article_detail.html', {
        'article': article,
    })
