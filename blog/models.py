from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


class Genre(models.Model):
    """Game genre model."""
    name = models.CharField(max_length=100, unique=True) 
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Game(models.Model):
    """Game model with improved validation and structure."""
    title = models.CharField(max_length=200, unique=True)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="blog/images/", help_text="Game cover image")
    img = models.URLField(blank=True, null=True, help_text="RAWG API cover image URL")
    video = models.FileField(
        upload_to="blog/videos/", 
        blank=True, 
        null=True,
        help_text="Game trailer or gameplay video"
    )
    is_home = models.BooleanField(
        default=True, 
        help_text="Display on homepage"
    )
    slug = models.SlugField(unique=True, blank=True)  
    metaScore = models.IntegerField(blank=True, null=True)

    gameplay_video_id = models.CharField(max_length=50, blank=True, null=True)
    trailer_video_id = models.CharField(max_length=50, blank=True, null=True)
    review_video_id = models.CharField(max_length=50, blank=True, null=True)
    tips_video_id = models.CharField(max_length=50, blank=True, null=True)

    genres = models.ManyToManyField(Genre, related_name="games", blank=True)
    platform = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-id'] 
        indexes = [
            models.Index(fields=['is_home']), # Index for faster filtering
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
    def average_rating(self):
        """Calculate average rating for this game. Open for the avg calculation changes."""
        return self.posts.aggregate(avg=Avg('rating'))['avg']

    def review_count(self):
        """Get total number of reviews for this game."""
        return self.posts.count()
    
    def get_display_image(self):
        """Get the best available image for display - prioritizes RAWG API image over uploaded image."""
        if self.img:  # RAWG API image URL
            return self.img
        elif self.image:  # Uploaded image file
            return self.image.url
        return None


class Post(models.Model):
    """Review/Post model with improved validation."""
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="Review content")
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Rating from 0.0 to 5.0"
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True,
        related_name="posts"
    )
    game = models.ForeignKey(
        Game, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id'] 
        indexes = [
            models.Index(fields=['game', '-id']),
            models.Index(fields=['creator', '-id']),
        ]

    def __str__(self):
        return f"{self.title or 'Review'} - {self.game.title}"


class UserProfile(models.Model):
    """Extended user profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="blog/images/", 
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def review_count(self):
        """Get total number of reviews by this user."""
        return self.user.posts.count()


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")

    class Meta:
        unique_together = ('user','post') # Both user and post should be unique together
        ordering = ['-id']

# Function to send a signal for creating a user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create user profile when user is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved."""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
