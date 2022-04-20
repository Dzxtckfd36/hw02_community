from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from .models import Post, Group, User


POSTS = 10
PAGE = 5

def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,

    }
    return render(request, 'posts/index.html', context)

@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_list = group.posts.order_by('-pub_date')[:POSTS]
    paginator = Paginator(group_list, PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


class JustStaticPage(TemplateView):
    template_name = 'posts/just_page.html'

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    count = Post.objects.filter(author__username=username).count()
    paginator = Paginator(user_posts, POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'count': count,
        'page_obj': page_obj,
        'author': username,
    }
    return render(request, 'posts/profile.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
        }
    return render(request, 'posts/post_detail.html', context)
