from django.shortcuts import render, get_object_or_404

from .models import Post, Group

POSTS = Post.objects.select_related('group')[:10]


def index(request):
    context = {
        'posts': POSTS,

    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'posts': posts,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)
