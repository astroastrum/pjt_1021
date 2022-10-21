from django.shortcuts import render
from .models import Review, Comment

# Create your views here.

def index(request):
    review = Review.objects.order_by('-pk')
    context = {
        'review': review
    }
    return render(request, 'reviews/index.html', context)