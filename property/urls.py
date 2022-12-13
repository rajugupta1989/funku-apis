from django.urls import path
from property import views


urlpatterns = [
    path(r'profile_image/', views.PropertyProfileImageAPIView.as_view(), name='profile_image'),
    path(r'update_profile_image/', views.PropertyProfileImageUpdateAPIView.as_view(), name='update_profile_image'),
    path(r'add_property/', views.AddPropertyAPIView.as_view(), name='add_property'),
    path(r'add_property_web/', views.AddPropertyWebAPIView.as_view(), name='add_property_web'),
    path(r'update_property_web/<int:pk>/', views.UpdateDeletePropertyWebAPIView.as_view(), name='update_property_web'),
    path(r'update_property/', views.UpdateDeletePropertyAPIView.as_view(), name='update_property'),
    path(r'add_property_social/', views.AddPropertySocialAPIView.as_view(), name='add_property_social'),
    path(r'update_property_social/<int:pk>/', views.UpdatePropertySocialAPIView.as_view(), name='update_property_social'),
    path(r"add_available_facilities/", views.AddAvailableFacilitiesAPIView.as_view(), name="add_available_facilities"),
    path(r"update_available_facilities/<int:pk>/", views.UpdateAvailableFacilitiesAPIView.as_view(), name="update_available_facilities"),


    path(r'add_flash_deal/', views.AddFlashDealAPIView.as_view(), name='add_flash_deal'),
    path(r'update_flash_deal/<int:pk>/', views.UpdateFlashDealAPIView.as_view(), name='update_flash_deal'),

    path(r'add_deal/', views.AddDealAPIView.as_view(), name='add_deal'),
    path(r'update_deal/<int:pk>/', views.UpdateDealAPIView.as_view(), name='update_deal'),


    path(r'add_party/', views.AddPartyAPIView.as_view(), name='add_party'),
    path(r'update_party/<int:pk>/', views.UpdatePartyAPIView.as_view(), name='update_party'),

]
