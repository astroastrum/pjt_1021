from django import forms
from .models import Review, Comment
from django import forms

class ReviewForm(forms. ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        
class CommentForm(forms. ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"