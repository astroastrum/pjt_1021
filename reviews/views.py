from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import os

# Create your views here.


def index(request):
    return render(request, "reviews/index.html", {"form": Review.objects.all()})


@login_required
def create(request):
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user_id = request.user.id
            temp.save()
            return redirect("reviews:detail", temp.id)
    return render(request, "reviews/create.html", {"form": form})


def detail(request, pk):
    info = Review.objects.get(pk=pk)
    form = CommentForm()
    temp = info.comment_set.all()
    context = {
        "info": info,
        "form": form,
        "temp": temp,
    }
    return render(request, "reviews/detail.html", context)


@login_required
def update(request, pk):
    temp = Review.objects.get(pk=pk)
    if request.user.id == temp.user_id:
        form = ReviewForm(instance=temp)
        if request.method == "POST":
            form = ReviewForm(request.POST, request.FILES, instance=temp)
            if form.is_valid():
                if (temp.image and request.FILES.get("image")) or request.POST.get("image-clear"):
                    os.remove(temp.image.path)
                if (temp.thumbnail and request.FILES.get("thumbnail")) or request.POST.get(
                    "thumbnail-clear"
                ):
                    os.remove(temp.thumbnail.path)
                form.save()
                return redirect("reviews:detail", pk)
        context = {"form": form}
        return render(request, "reviews/update.html", context)
    else:
        return HttpResponseForbidden


@login_required
def delete(request, pk):
    temp = Review.objects.get(pk=pk)
    if request.user.id == temp.user_id:
        if temp.image:
            os.remove(temp.image.path)
        if temp.thumbnail:
            os.remove(temp.thumbnail.path)
        Review.objects.get(pk=pk).delete()
        return redirect("reviews:index")
    else:
        return HttpResponseForbidden


@login_required
def comment_create(request, review_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.review_id = review_pk
        temp.user_id = request.user.id
        temp.save()
        return redirect("reviews:detail", review_pk)


@login_required
def comment_delete(request, review_pk, comment_pk):
    temp = Comment.objects.get(pk=comment_pk)
    if request.user.id == temp.user_id:
        temp.delete()
        return redirect("reviews:detail", review_pk)
    else:
        return HttpResponseForbidden


def search(request):
    form = Review.objects.filter(title__contains=request.GET["title"])
    return render(request, "reviews/search.html", {"form": form})
