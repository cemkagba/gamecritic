from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q , F
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.html import linebreaks
from blog.models import Game, Post, Like, Genre
from .forms import GamePost
from .youtube_api import search_trailer, search_gameplay, search_review, search_tips


class IndexView(View):
    """Homepage view"""

    def get(self, request):
        games = Game.objects.filter(is_home=True).order_by('-created_at')
        review_game = Game.objects.annotate(review_count=Count('posts')).order_by('-review_count')[:5]
        page_number = request.GET.get('page', 1)
        
        # it has paginator but not used in this view for later updates 
        paginator = Paginator(games, 5)
        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

        # Pull last created 5 game
        recent_games = Game.objects.order_by('-created_at')[:5]

        context = {
            'games': page_obj,
            'reviewed_games': review_game,
            'recent_games': recent_games,
        }
        return render(request, 'blog/index.html', context)


class AllGamesView(View):
    """View for displaying all games with pagination and filtering."""
    
    SORTING_OPTIONS = {
        'rating_desc': {
            'field': 'avg_rating',
            'label': 'Rating High to Low',
            'requires_annotation': True,
            'annotation': {'avg_rating': Avg('posts__rating')}
        },
        'rating_asc': {
            'field': '-avg_rating',
            'label': 'Rating Low to High',
            'requires_annotation': True,
            'annotation': {'avg_rating': Avg('posts__rating')}
        },
        'newest': {
            'field': '-created_at',
            'label': 'Newest First',
            'requires_annotation': False
        },
        'oldest': {
            'field': 'created_at', 
            'label': 'Oldest First',
            'requires_annotation': False
        },
        'title_asc': {
            'field': 'title',
            'label': 'Title A-Z',
            'requires_annotation': False
        },
        'title_desc': {
            'field': '-title',
            'label': 'Title Z-A', 
            'requires_annotation': False
        }
    }
    
    DEFAULT_SORT = 'newest'

    def get(self, request):
        games = Game.objects.all()
        games = self._apply_filters(games, request)

        search_query = request.GET.get('search', '')
        if search_query:
            games = games.filter(
                Q(title__icontains=search_query) | 
                Q(platform__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(genres__name__icontains=search_query)
            ).distinct()
        
        games = self._apply_sorting(games, request)

        page_number = request.GET.get('page', 1)
        paginator = Paginator(games, 10)

        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

    # Split all platforms and collect unique values
        all_platforms = set() #unique set elements for every platform 
        for game in Game.objects.values_list('platform', flat=True):
            if game:
                for p in game.split(','):
                    all_platforms.add(p.strip())
        all_platforms = sorted(all_platforms)
        
        context = {
            'games': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': page_obj.has_other_pages(),
            'search_query': search_query,
            'all_platforms' : all_platforms,
            'selected_platform' : request.GET.get('platform',''),
            'selected_genre': request.GET.get('genre', ''),
            'selected_sort': request.GET.get('sort', self.DEFAULT_SORT),
            'all_genres': Genre.objects.all().order_by('name'),
            'sorting_options': self.get_available_sorting_options(),
        }
        return render(request, 'blog/all_games.html', context)

    def _apply_filters(self, queryset, request):
        genre_filter = request.GET.get('genre')
        if genre_filter:
            queryset = queryset.filter(genres__slug=genre_filter)
        
        platform_filter = request.GET.get('platform')
        if platform_filter:
            queryset = queryset.filter(platform__icontains=platform_filter)
        
        return queryset
    
    def _apply_sorting(self, queryset, request):
       
        sort_by = request.GET.get('sort', self.DEFAULT_SORT)

        if sort_by not in self.SORTING_OPTIONS:
            sort_by = self.DEFAULT_SORT

        sort_config = self.SORTING_OPTIONS[sort_by]

        if sort_config.get('requires_annotation', False):
            queryset = queryset.annotate(**sort_config['annotation']).filter(avg_rating__isnull = False)
            
            if sort_by == 'rating_desc':
                # Order the queryset by 'avg_rating' in descending order,
                # placing NULL values last
                #F func for work with every database system and usage for desc and asc nulls_first etc
                return queryset.order_by(F('avg_rating').desc(nulls_last=True))
            elif sort_by == 'rating_asc':
                # Order the queryset by 'avg_rating' in ascending order,
                # placing NULL values first
                return queryset.order_by(F('avg_rating').asc(nulls_first=True))

        return queryset.order_by(sort_config['field'])
    
    def get_available_sorting_options(self):
        return {
            key: config['label'] 
            for key, config in self.SORTING_OPTIONS.items()
        }


class GameDetailView(View):
    """Detailed view for a specific game."""
    
    SORT_OPTIONS = {
        'most_liked': {'order': '-like_count', 'label': 'Most Liked'},
        'least_liked': {'order': 'like_count', 'label': 'Least Liked'},
    }
    
    def get(self, request, slug):
        game = get_object_or_404(Game, slug=slug)
        self._search_game_videos(game)
        
        sort = request.GET.get('sort', 'most_liked')
        
        posts_list = Post.objects.filter(game=game).annotate(
            like_count=Count('likes')
        )
        
        if sort in self.SORT_OPTIONS:
            posts_list = posts_list.order_by(self.SORT_OPTIONS[sort]['order'])
        else:
            posts_list = posts_list.order_by('-like_count')

        if request.user.is_authenticated:
            for post in posts_list:
                post.user_has_liked = post.likes.filter(user=request.user).exists()
        else:
            for post in posts_list:
                post.user_has_liked = False
        

        context = {
            'game': game,
            'slug': slug,
            'posts': posts_list,
            'genres': Genre.objects.all(),
            'avg_rating': game.average_rating(),
            'form': GamePost(),
            'current_sort': sort,
            'sort_options': self.SORT_OPTIONS,
        }
        
        return render(request, 'blog/extra_details.html', context)
    
    def _search_game_videos(self, game):
        """
        Search and cache video IDs for the game.
        Only searches if video ID is None (never searched before).
        """
        try:
            videos_updated = False
            
            # Only call the API for video IDs that have never been searched (None)
            if game.trailer_video_id is None:
                trailer_videos = search_trailer(game.title, max_result=1)
                if trailer_videos:
                    game.trailer_video_id = trailer_videos[0]['video_id']
                else:
                    # Use an empty string to indicate that no video was found
                    game.trailer_video_id = ''
                videos_updated = True
            
            if game.review_video_id is None:
                review_videos = search_review(game.title, max_result=1)
                if review_videos:
                    game.review_video_id = review_videos[0]['video_id']
                else:
                    game.review_video_id = ''
                videos_updated = True
            
            if game.gameplay_video_id is None:
                gameplay_videos = search_gameplay(game.title, max_result=1)
                if gameplay_videos:
                    game.gameplay_video_id = gameplay_videos[0]['video_id']
                else:
                    game.gameplay_video_id = ''
                videos_updated = True

            if game.tips_video_id is None:
                tips_videos = search_tips(game.title, max_result=1)
                if tips_videos:
                    game.tips_video_id = tips_videos[0]['video_id']
                else:
                    game.tips_video_id = ''
                videos_updated = True
            
            if videos_updated:
                game.save()
                
        except Exception as e:
            # Log the error if needed, but don't break the page
            print(f"Error searching videos for {game.title}: {e}")
            pass


class CreateReviewView(LoginRequiredMixin, View):
    """Create new review for a game."""
    login_url = 'login'

    def post(self, request, slug):
        game = get_object_or_404(Game, slug=slug)
        form = GamePost(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.game = game
            post.save()
            messages.success(request, "Review submitted successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
        
        return redirect('extra_details', slug=slug)


class UpdateGameReviewView(LoginRequiredMixin, View):
    """Update game review."""
    login_url = 'login'

    def post(self, request, review_id):
        review = get_object_or_404(Post, id=review_id, creator=request.user)
        game_slug = review.game.slug
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax :
            form = GamePost(request.POST, instance=review)

            if form.is_valid():
                old_title = review.title
                old_description = review.description  
                old_rating = review.rating
                saved_review = form.save()
                
                return JsonResponse({
                    'success':True,
                    'message': 'Review updated successfully!' if (
                        old_title != saved_review.title or 
                        old_description != saved_review.description or 
                        old_rating != saved_review.rating
                    ) else 'No changes were made.',
                    'review': {
                        'id': saved_review.id,
                        'title': saved_review.title,
                        'description': linebreaks(saved_review.description),
                        'rating': str(saved_review.rating),
                        'updated_at': saved_review.updated_at.strftime('%b %d, %Y at %H:%M')
                    }
                })
            else:
                return JsonResponse({
                    'success':False,
                    'errors':form.errors
                })

        form = GamePost(request.POST, instance=review)
        
        if form.is_valid():
            old_title = review.title
            old_description = review.description  
            old_rating = review.rating
            
            saved_review = form.save()
            
            if (old_title == saved_review.title and 
                old_description == saved_review.description and 
                old_rating == saved_review.rating):
                messages.info(request, "No changes were made.")
            else:
                messages.success(request, "Review updated successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
        
        return redirect('extra_details', slug=game_slug)


class DeleteReviewView(LoginRequiredMixin, View):
    """Delete user review view."""
    login_url = 'login'

    def post(self, request, review_id):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                review = get_object_or_404(Post, id=review_id, creator=request.user)
                review.delete()
                return JsonResponse({'success': True, 'message': 'Review deleted successfully.'})
            except Post.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Review not found or you don't have permission."})
            except Exception:
                return JsonResponse({'success': False, 'message': 'An error occurred while deleting the review.'})
        else:
            try:
                review = get_object_or_404(Post, id=review_id, creator=request.user)
                game_slug = review.game.slug
                review.delete()
                messages.success(request, "Review deleted successfully.")
                return redirect('extra_details', slug=game_slug)
            except Post.DoesNotExist:   
                messages.error(request, "Review not found or you don't have permission")
                return redirect('profile')
            except Exception:
                messages.error(request, 'An error occurred while deleting the review.')
                return redirect('profile')


class ToggleLikeView(LoginRequiredMixin, View):
    """Toggle like/unlike for a post."""
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