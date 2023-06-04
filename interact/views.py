from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib import messages

from .models import UserChatGroup
from resources.models import Post, Reply
from giz_app.models import Profile


def interact(request):

    if request.method == "POST":
        message = request.POST.get("message")
        title = request.POST.get("title")
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        post = Post(created_by=request.user, title=title, message=message)
        if video is not None and video != "":
            post.video = video
        if image is not None and image != "":
            post.image = image

        post.save()
        messages.success(request, "You have successfully posted.")

        return redirect('interact')

    posts = Post.objects.all()
    for post in posts:
        post.reply_count = Reply.objects.filter(post=post).count()

    context = {
        "posts": posts
    }
    return render(request, template_name='agrul/pages/interact/interact.html', context=context)


def single_post(request, post_id, slug):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        reply = Reply.objects.create(reply=request.POST.get("reply"), created_by=request.user, post=post)
        reply.save()
        messages.success(request, "Comment added successfully")
        return redirect('post', post_id, slug)
    context = {
        "post": post,
        "replies": Reply.objects.filter(post=post)
    }
    return render(request, template_name='agrul/pages/interact/single_post.html', context=context)


@api_view(['POST'])
def add_friend(request):
    data = request.data
    user = request.user
    new_friend = User.objects.filter(id=data.get('user_id')).first()
    if new_friend:
        add_new_friend(user, new_friend)
        chat_room = UserChatGroup.objects.create(user_1=user, user_2=new_friend)
        chat_room.save()
        return Response({
            'message': 'Friend added successfully',
        }, status=status.HTTP_200_OK)
    return Response({
        'message': 'User not found',
    }, status=status.HTTP_404_NOT_FOUND)


def add_new_friend(user_1, user_2):
    user_1_has_profile = hasattr(user_1, 'profile')
    user_2_has_profile = hasattr(user_2, 'profile')
    if not user_1_has_profile:
        profile = Profile.objects.create(user=user_1)
        profile.save()
        user_1.refresh_from_db()
    
    if not user_2_has_profile:
        profile = Profile.objects.create(user=user_2)
        profile.save()
        user_2.refresh_from_db()
    
    if user_1 and user_2:
        if user_1 not in user_2.profile.friends.all():
            user_2.profile.friends.add(user_1)
            user_2.profile.save()
        if user_2 not in user_1.profile.friends.all():
            user_1.profile.friends.add(user_2)
            user_1.profile.save()
