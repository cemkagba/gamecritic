from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Post, Genre


class GamePost(forms.ModelForm):
    """Form for creating game reviews/posts."""
    
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Review title (optional)'
        }),
        help_text="Optional title for your review"
    )
    
    description = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Write your detailed review here...'
        }),
        help_text="Share your thoughts about this game"
    )
    
    rating = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '5',
            'step': '0.1'
        }),
        help_text="Rate from 0.0 to 5.0"
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'rating']
        
    def clean_rating(self):
        """Validate rating is within acceptable range."""
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0.0 or rating > 5.0:
                raise forms.ValidationError("Rating must be between 0.0 and 5.0")
        return rating
    
    def clean_description(self):
        """Validate description length."""
        description = self.cleaned_data.get('description')  #filtered data with the where req met 
        return description


class GameSearchForm(forms.Form):
    """Form for searching games."""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search games...'
        })
    )
    
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label="All Genres",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('created_at', 'Newest First'),
            ('-created_at', 'Oldest First'),
            ('title', 'Title A-Z'),
            ('-title', 'Title Z-A'),
        ],
        required=False,
        initial='created_at',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
