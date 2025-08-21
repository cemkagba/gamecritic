from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from .forms import ProfileForm, ProfileUpdateForm, LoginForm, RegisterForm, ReviewForm,ReviewForm
from blog.models import UserProfile, Post,Like
from django.utils.html import linebreaks
from django.db.models import Count



class LoginView(View):
    """User login view."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})
    
    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect("home")
        
        return render(request, "account/login.html", {'form': form})

class RegisterView(View):
    """User registration view."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
       
            user = form.save()
        
            UserProfile.objects.get_or_create(user=user)

     
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(request, "Account created successfully! Welcome!")
                return redirect("home")
        
        return render(request, "account/register.html", {'form': form})


class LogoutView(View):
    """User logout view."""

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out successfully!")
        return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get_or_create_profile(self):
        """Get or create user profile."""
        try:
            return self.request.user.userprofile
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=self.request.user)

    def get(self, request):
        user_profile = self.get_or_create_profile()

        posts = (
            Post.objects
                .filter(creator=request.user)
                .annotate(like_count=Count('likes'))   # number of likes
                .order_by('-id')
        )

    # Which posts has this user liked? (single query)
        liked_ids = set(
            Like.objects.filter(user=request.user, post__in=posts)
                        .values_list('post_id', flat=True)
        )
        for p in posts:
            p.user_has_liked = p.id in liked_ids

        context = {
            'form': ProfileForm(instance=user_profile),
            'update_form': ProfileUpdateForm(instance=request.user),
            'user': request.user,
            'posts': posts,
        }
        return render(request, 'account/profile.html', context)


class UpdateReviewView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, review_id):
        """Update the review using ReviewForm."""
        
        review = get_object_or_404(Post, id=review_id, creator=request.user)
        form = ReviewForm(request.POST, instance=review)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if form.is_valid():
            old_title = review.title
            old_description = review.description
            old_rating = review.rating

            saved_review = form.save()

            if (old_title == saved_review.title and
                old_description == saved_review.description and
                old_rating == saved_review.rating):
                msg = "No changes were made."
            else:
                msg = "Review updated successfully!"

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': msg,
                    'review': {
                    'id': saved_review.id,
                    'title': saved_review.title,
                    'description': linebreaks(saved_review.description),
                    'rating': str(saved_review.rating),
                    'updated_at': saved_review.updated_at.strftime('%b %d, %Y at %H:%M')
                    }
                })
            else:
                messages.success(request, msg)
                return redirect('profile')
        else:
            errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
            if is_ajax:
                return JsonResponse({'success': False, 'errors': errors})
            else:
                for field, errs in form.errors.items():
                    for error in errs:
                        messages.error(request, f"{field.title()}: {error}")
                return redirect('profile')


class UpdateUsernameView(LoginRequiredMixin, View):
    """Update username view """
    login_url = 'login'

    def post(self, request):
        new_username = request.POST.get('username', '').strip()
        current_username = request.user.username

    # Validation
        if not new_username:
            messages.error(request, "Username cannot be empty.")
            return redirect('profile')

        if new_username == current_username:
            messages.info(request, "Username is already the same.")
            return redirect('profile')

        if User.objects.filter(username=new_username).exists():
            messages.error(request, 'This username is already taken!')
            return redirect('profile')

        try:
            request.user.username = new_username
            request.user.save() 
            messages.success(request, f"Username updated to '{new_username}' successfully!")
        except Exception as e:
            messages.error(request, "An error occurred while updating username.")
        
        return redirect('profile')

        

class UpdatePhotoView(LoginRequiredMixin, View):
    """Update profile photo view """
    login_url = 'login'
    
    def post(self, request):
        
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user)
        
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile photo updated successfully!")
        else:
            messages.error(request, "Error updating profile photo.")
        
        return redirect('profile')
    

class DeleteReviewView(LoginRequiredMixin, View):
    """Delete user review view."""
    login_url = 'login'

    def post(self, request, review_id, *args, **kwargs):
        try:
            review = get_object_or_404(Post, id=review_id, creator=request.user)
            review.delete()
            messages.success(request, "Review deleted successfully.")
        except Post.DoesNotExist:
            messages.error(request, 'Review not found or you dont have permission')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the review.')

        return redirect('profile')


class ToggleLikeView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'liked': liked,
                'like_count': post.likes.count(),
                'post_id': post.id,
            })

        next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect('extra_details', slug=post.game.slug)