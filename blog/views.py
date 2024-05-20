from django.shortcuts import render, redirect
from .models import Post, MyUser, CommentPost, FollowMyUser, LikePost
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def func(post, comments, likes):
    post.comments = comments[:5]
    post.likes = likes[:3]
    return post


@login_required(login_url='/login')
def home_view(request):
    users = MyUser.objects.exclude(user=request.user)
    user = MyUser.objects.filter(user=request.user).first()

    followings = FollowMyUser.objects.filter(follower=user).values_list('following_id', flat=True)
    display_users = users.exclude(id__in=followings)
    users_followed = MyUser.objects.filter(id__in=followings)
    posts = Post.objects.filter(author__in=users_followed)
    if len(users_followed) == 0:
        posts = Post.objects.filter(is_published=True, author=user)
    d = {
        'posts': map(lambda post: func(post, CommentPost.objects.filter(post_id=post.id),
                                       LikePost.objects.filter(post_id=post.id)), posts),
        'user': user,
        'profiles': MyUser.objects.all().exclude(user=request.user),
        'user_profile': MyUser.objects.filter(user=request.user),
        'display_users': display_users
    }

    if request.method == 'POST':
        data = request.POST
        message = data['message']
        post_id = data['post_id']
        my_user = MyUser.objects.filter(user=request.user).first()
        obj = CommentPost.objects.create(message=message, post_id=post_id, author=my_user)
        obj.save()
        return redirect('/#{}'.format(post_id))

    return render(request, 'index.html', context=d)


@login_required(login_url='/login')
def profile_view(request, pk):
    user = MyUser.objects.filter(user=request.user).first()
    my_user = MyUser.objects.filter(user_id=pk).first()
    posts = Post.objects.filter(author_id=my_user.id)
    d = {
        'profile': my_user,
        'posts': posts,
        'user': user
    }
    if request.method == "POST":
        my_user = MyUser.objects.filter(user=request.user).first()
        files = request.FILES
        profile_image = files.get('image', None)
        if profile_image is not None:
            my_user.profile_image = profile_image
            my_user.save(update_fields=['profile_image'])
            return redirect(f'/profile/{my_user.id}/')

    return render(request, 'profile.html', context=d)


def setting_view(request):
    return render(request, 'setting.html')


def login_view(request):
    d = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        d['error'] = 'this user does not exist'
    return render(request, 'signin.html', context=d)


def register_view(request):
    d = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        p1 = data['password1']
        p2 = data['password2']
        if not User.objects.filter(username=username).exists() and p1 == p2:
            user = User.objects.create(username=username, password=make_password(p1))
            user.save()
            my_user = MyUser.objects.create(user=user)
            my_user.save()
            return redirect('/login')
        d['error'] = 'login was broken'
    return render(request, 'signup.html', context=d)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def upload_view(request):
    if request.method == 'POST':
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(post_image=request.FILES['image'], author=my_user)
        my_user.posts_count += 1
        post.save()
        my_user.save(update_fields=['posts_count'])
        return redirect('/')
    return redirect('/')


@login_required(login_url='/login')
def delete_view(request):
    post_id = request.GET.get('post_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    if request.user == my_user:
        post = Post.objects.filter(id=post_id, author_id=my_user.id).first()
        my_user.posts_count -= 1
        my_user.save(update_fields=['posts_count'])
        post.delete()
    return redirect('/')


@login_required(login_url='/login')
def follow_view(request):
    profile_id = request.GET.get('profile_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    profile = MyUser.objects.filter(id=profile_id).first()
    follow_exists = FollowMyUser.objects.filter(follower=my_user, following_id=profile_id)
    if follow_exists.exists():
        follow_exists.delete()
        profile.follower_count -= 1
        my_user.following_count -= 1
        profile.save(update_fields=['follower_count'])
        my_user.save(update_fields=['following_count'])
        return redirect('/')

    obj = FollowMyUser.objects.create(follower=my_user, following_id=profile_id)
    obj.save()
    profile.follower_count += 1
    my_user.following_count += 1
    profile.save(update_fields=['follower_count'])
    my_user.save(update_fields=['following_count'])
    return redirect('/')


@login_required(login_url='/login')
def like_view(request):
    post_id = request.GET.get('post_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    like = Post.objects.filter(id=post_id).first()
    like_exists = LikePost.objects.filter(author=my_user, post_id=post_id)
    if like_exists.exists():
        like_exists.delete()
        like.like_count -= 1
        like.save(update_fields=['like_count'])
        return redirect('/#{}'.format(post_id))

    obj = LikePost.objects.create(author=my_user, post_id=post_id)
    obj.save()
    like.like_count += 1
    like.save(update_fields=['like_count'])
    return redirect('/#{}'.format(post_id))


@login_required(login_url='/login')
def search_view(request):
    if request.method == "POST":
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')

    query = request.GET.get('q')
    posts = Post.objects.filter(is_published=True)
    if query is not None:
        posts = posts.filter(author__user__username__icontains=query)

    d = {
        'posts': posts
    }
    return render(request, 'index.html', context=d)
