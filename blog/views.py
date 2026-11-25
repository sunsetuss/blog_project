
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Article, Category, Tag
from .forms import ArticleForm


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

    tag_cloud = list(
        Tag.objects.annotate(
            articles_count=Count(
                'articles',
                filter=Q(articles__status='published'),
                distinct=True
            )
        ).filter(
            articles_count__gt=0
        ).order_by('-articles_count', 'name')[:40]
    )

    font_sizes = [12, 13, 14, 15, 16, 17]

    total_tags = len(tag_cloud)

    for index, tag in enumerate(tag_cloud):
        level = (
            index * (len(font_sizes) - 1)
            // max(1, total_tags - 1)
        )

        tag.font_size = font_sizes[-1 - level]

    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/article_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
        'tag_cloud': tag_cloud,
    })


def article_detail(request, pk):

    Article.objects.filter(
        pk=pk,
        status='published'
    ).update(
        view_count=F('view_count') + 1
    )

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


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('article_list')

    else:
        form = UserCreationForm()

    return render(request, 'blog/register.html', {
        'form': form,
    })


@login_required
def my_articles(request):

    articles = Article.objects.filter(
        author=request.user
    ).select_related(
        'category', 'author'
    ).prefetch_related('tags')

    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/my_articles.html', {
        'page_obj': page_obj,
    })


@login_required
def article_create(request):

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()

            return redirect('my_articles')

    else:
        form = ArticleForm()

    return render(request, 'blog/article_form.html', {
        'form': form,
        'page_title': 'Создание статьи',
    })


@login_required
def article_update(request, pk):

    article = get_object_or_404(
        Article,
        pk=pk,
        author=request.user
    )

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            return redirect('my_articles')

    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/article_form.html', {
        'form': form,
        'page_title': 'Редактирование статьи',
    })


@login_required
def article_delete(request, pk):

    article = get_object_or_404(
        Article,
        pk=pk,
        author=request.user
    )

    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')

    return render(request, 'blog/article_confirm_delete.html', {
        'article': article,
    })


LOGIN_URL = '/admin/login/'
