from django.urls import path
from . import views

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path('delete-review/<int:review_id>/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('update-review/<int:review_id>/', views.UpdateReviewView.as_view(), name='update_review'),
    path('update-username/', views.UpdateUsernameView.as_view(), name='update_username'),
    path('update-photo/', views.UpdatePhotoView.as_view(), name='update_photo'),
]
