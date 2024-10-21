from django.core.paginator import Paginator
from .models import Post
from django.utils import timezone
from django.db.models import Count


def paginate_queryset(request, queryset, items_per_page=10):
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_published_posts(category=None):
    posts = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    if category:
        posts = posts.filter(category=category)
    return posts.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
