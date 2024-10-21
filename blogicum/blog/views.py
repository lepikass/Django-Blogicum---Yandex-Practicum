from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Category, Comment, Post
from .utils import paginate_queryset, get_published_posts


def index(request):
    posts = get_published_posts()
    page_obj = paginate_queryset(request, posts)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = get_published_posts(category=category)
    page_obj = paginate_queryset(request, post_list)
    return render(
        request, 'blog/category.html',
        {
            'category': category,
            'page_obj': page_obj
        }
    )


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        post = get_object_or_404(
            get_published_posts(), pk=post_id
        )

    comments = post.comments.all()
    form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


User = get_user_model()


class ProfileView(View):
    def get(self, request, username):
        profile = get_object_or_404(User, username=username)
        profile.full_name = profile.get_full_name() or None
        posts = Post.objects.filter(author=profile).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        page_obj = paginate_queryset(request, posts)
        return render(
            request, 'blog/profile.html',
            {'profile': profile, 'page_obj': page_obj}
        )


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'blog/user.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            updated_user = form.save()
            return redirect('blog:profile', username=updated_user.username)
        return render(request, 'blog/user.html', {'form': form})


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/create.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.is_published = True
            post.save()
            return redirect('blog:profile', username=request.user.username)
        return render(request, 'blog/create.html', {'form': form})


class EditPostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return redirect('blog:post_detail', post_id)
        form = PostForm(instance=post)
        return render(request, 'blog/create.html', {'form': form})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return redirect('blog:post_detail', post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
        return render(request, 'blog/create.html', {'form': form})


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        # Проверяем, является ли пользователь автором поста.
        # Если текущий пользователь не является автором поста,
        # то ему не разрешено удалять этот пост.
        if post.author != request.user:
            # Перенаправляем пользователя на страницу поста,
            # так как у него нет прав на удаление.
            return redirect('blog:post_detail', post_id=post.id)
        return render(request, 'blog/create.html', {
            'post': post,
            'is_delete_confirmation': True,
        })

    def post(self, request, post_id):
        # Пытаемся получить пост по идентификатору и проверяем,
        # является ли текущий пользователь автором поста.
        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.delete()
        return redirect('blog:profile', username=request.user.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    return render(request, 'blog/comment.html', {
        'post': post,
        'comments': post.comments.all(),
    })


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)
    return render(
        request,
        "blog/comment.html",
        context={"comment": comment, "form": form},
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/comment.html", context={"comment": comment})


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
