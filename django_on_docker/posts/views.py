from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Book, Post, Wokashi, Ahare, Bookmark, Comment, Nice
from django.contrib.auth.models import User
from .forms import CommentForm, PostForm
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
import urllib.parse

# from .models import User

import requests
import time

RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = "1065776451953533134"
def get_book_cover_path(title, author):
    encoded_title = urllib.parse.quote(str(title))
    encoded_author = urllib.parse.quote(str(author))
    response = requests.get("{}?format=json&applicationId={}&title={}&author={}".format(RAKUTEN_BOOKS_API_URL, RAKUTEN_APP_ID, encoded_title, encoded_author))
    cover_path = ''
    if response.status_code != requests.codes.ok:
        cover_path = 'Requests failed'
    elif response.json()["count"] == 0:
        cover_path = 'No book found'
    else:
        cover_path = response.json()["Items"][0]["Item"]["largeImageUrl"]
    return cover_path

# Takahashi Shunichi
def index(request):
    post = Post.objects.filter(is_deleted=False)

    params = {"title": "ポスト一覧", "post": post}
    return render(request, "posts/index.html", params)


#Takahashi Shunichi
def wokashi_create(request):
    if request.method == "POST":
        user_id = request.user.id
        post_id = request.POST["post_id"]
        wokashi = Wokashi(user_id=user_id, post_id=post_id, count=1)
        wokashi.save()
        return redirect(to="/posts")


#Takahashi Shunichi
def ahare_create(request):
    if request.method == "POST":
        user_id = request.user.id
        post_id = request.POST["post_id"]
        wokashi = Ahare(user_id=user_id, post_id=post_id, count=1)
        wokashi.save()
        return redirect(to="/posts")


# Takahashi Shunichi
# Umakoshi Masato
def detail(request, num):
    post = Post.objects.get(id=num)
    # comments = post.comment_set.all()
    comments = Comment.objects.filter(post_id=num)
    num_nices = [
        len(Nice.objects.filter(comment_id=comment.id)) for comment in comments
    ]
    comments_num_nices = zip(comments, num_nices)
    params = {
        "title": "ポスト詳細",
        "post": post,
        "comments_num_nices": comments_num_nices,
        "form": CommentForm(),
    }
    return render(request, "posts/detail.html", params)


# Takahashi Shunichi
@transaction.atomic
def create(request):
    if request.method == "POST":
        content = (request.POST["content"], )
        title = (request.POST["title"], )
        author = (request.POST["author"], )

        # cover_path = ''
        cover_path = get_book_cover_path(title, author)
        time.sleep(1)

        if cover_path == 'No book found':
            book = Book(title=title, author=author) #すでに存在するなら追加しない
        else:
            book = Book(title=title, author=author, cover_path=cover_path) #すでに存在するなら追加しない
        book.save()
        user = User.objects.get(id=request.user.id)
        post = Post(user_id=user, content=content, book_id=book)
        post.save()

        return redirect(to="/posts")
    params = {"title": "ポスト投稿", "form": PostForm()}
    return render(request, "posts/create.html", params)


# Takahashi Shunichi
@transaction.atomic
def edit(request, num):
    post = Post.objects.get(id=num)
    book_id = post.id
    book = Book.objects.get(id=book_id)
    initial_dict = {
        "content": post.content,
        "title": book.title,
        "author": book.author
    }

    if request.method == "POST":
        content = (request.POST["content"], )
        title = (request.POST["title"], )
        author = (request.POST["author"], )

        book.title = title
        book.author = author
        book.save()
        post.content = content
        post.save()
        return redirect(to="/posts")

    params = {
        "title": "ポスト編集",
        "id": num,
        "form": PostForm(initial=initial_dict)
    }
    return render(request, "posts/edit.html", params)


# Takahashi Shunichi
@transaction.atomic
def delete(request, num):
    post = Post.objects.get(id=num)
    if request.method == "POST":
        post.is_deleted = True
        post.save()
        return redirect(to="/posts")

    params = {"title": "ポスト削除", "id": num, "post": post}
    return render(request, "posts/delete.html", params)


@transaction.atomic
def comment_create(request, num):
    """Posting comment function.

    TODO:
        handle
            * Not logged in user
            * Not post request

    Author:
        Masato Umakoshi
    """
    # If not post, raise 404
    if request.method != "POST":
        raise Http404("Hogehoge")

    # This may be too naive
    user_id = request.user.id
    content = request.POST["content"]
    comment = Comment(
        user_id=User.objects.get(pk=user_id),
        post_id=Post.objects.get(pk=num),
        content=content,
    )
    comment.save()
    # post_id may be post.id??
    # return HttpResponseRedirect(reverse("posts:show", args=(num, )))
    return redirect(to="/posts")


@transaction.atomic
def nice_create(request):
    """Posting nice function.

    TODO:
        handle
            * Not logged in user
            * Not post request

    Author:
        Masato Umakoshi
    """
    # If not post, raise 404
    if request.method != "POST":
        raise Http404("Hogehoge")

    # This may be too naive
    user_id = request.user.id
    comment_id = request.POST["comment_id"]
    nice = Nice(
        user_id=User.objects.get(pk=user_id),
        comment_id=Comment.objects.get(pk=comment_id),
    )
    nice.save()
    # post_id may be post.id??
    # return HttpResponseRedirect(reverse("posts:show", args=(num, )))
    return redirect(to="/posts")