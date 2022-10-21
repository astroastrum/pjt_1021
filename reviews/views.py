from django.shortcuts import render
from .models import Review, Comment

# Create your views here.

def index(request):
    return render(request, 'reviews/index.html')