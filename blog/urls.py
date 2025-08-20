# http://127.0.0.1:8000
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include


urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("all-games/", views.AllGamesView.as_view(), name="all_games"),
    path("details/<slug:slug>/", views.GameDetailView.as_view(), name="extra_details"),
    path('create-review/<slug:slug>/', views.CreateReviewView.as_view(), name='create_review'),
    path('update-game-review/<int:review_id>/', views.UpdateGameReviewView.as_view(), name='update_game_review'),
    path('delete-review/<int:review_id>/', views.DeleteReviewView.as_view(), name='_delete_review'),
    path('toggle-like/<int:post_id>/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path("__reload__/", include("django_browser_reload.urls")),
]
