from django.urls import path
from artist import views


urlpatterns = [
    path(r'add_artist/', views.AddArtistAPIView.as_view(), name='add_artist'),
    path(r'update_artist/<int:pk>/', views.UpdateArtistAPIView.as_view(), name='update_artist'),
    path(r'add_artist_social_profile/', views.AddArtistSocialProfileAPIView.as_view(), name='add_artist_social_profile'),
    path(r'update_artist_social_profile/<int:pk>/', views.UpdateArtistSocialProfileAPIView.as_view(), name='update_artist_social_profile'),
   
]
