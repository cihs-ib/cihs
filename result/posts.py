from django.views.generic.edit import UpdateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Post
#@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'result/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'result/post_detail.html', {'post': post})

def post_list(request):
    posts = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 30)
    try:
        all_page = paginator.page(page)
    except PageNotAnInteger:
        all_page = paginator.page(1)
    except EmptyPage:
        all_page = paginator.page(paginator.num_pages)
    return render(request, 'result/all_post_list.html', {'all_page': all_page, 'post': posts.count()})
    
    
@login_required
def posts_publishing(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = timezone.now()
    post.save()
    return redirect('post_edit', pk=pk)

class post_edit(UpdateView):
    model = Post
    fields = ['subject', 'text', 'comment']
    success_url = reverse_lazy('post_list')

@login_required
def post_draft_list(request):#post approvals(#review post uncomment for no review)
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'result/post_draft_list.html', {'posts': posts})
@login_required
def my_post(request):#adding publish button(#review post uncomment for no review)
    post = Post.objects.filter(Account_Username=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 30)
    try:
        all_page = paginator.page(page)
    except PageNotAnInteger:
        all_page = paginator.page(1)
    except EmptyPage:
        all_page = paginator.page(paginator.num_pages)
    return render(request, 'result/post_list.html', {'all_page': all_page, 'post': post.count()})
