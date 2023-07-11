from django.urls import path
from property import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'profile_image/', views.PropertyProfileImageAPIView.as_view(), name='profile_image'),
    path(r'update_profile_image/', views.PropertyProfileImageUpdateAPIView.as_view(), name='update_profile_image'),
    path(r'add_property/', views.AddPropertyAPIView.as_view(), name='add_property'),
    path(r'add_property_web/', views.AddPropertyWebAPIView.as_view(), name='add_property_web'),
    path(r'property_verify/', views.PropertyVerifyAPIView.as_view(), name='property_verify'),
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
    path(r'get_deal_by_lat_long/', views.GetDealByLatLongAPIView.as_view(), name='get_deal_by_lat_long'),
    path(r'get_flashdeal_by_lat_long/', views.GetFlashDealByLatLongAPIView.as_view(), name='get_flashdeal_by_lat_long'),
    path(r'get_party_by_lat_long/', views.GetPartyByLatLongAPIView.as_view(), name='get_party_by_lat_long'),
    
    path(r'get_property_by_lat_long/', views.GetPropertyByLatLongAPIView.as_view(), name='get_property_by_lat_long'),
    path(r'user_enquiry/', views.UserEnquiryAPIView.as_view(), name='user_enquiry'),
    path(r'user_enquiry_cancel/<int:pk>/', views.GetUpdateUserEnquiryAPIView.as_view(), name='user_enquiry_cancel'),
    path(r'user_take_action_on_user_enquiry/', views.UserTakeActionOnUserEnquiryAPIView.as_view(), name='user_take_action_on_user_enquiry'),
    path(r'club_owner_take_action_on_user_enquiry/', views.ClubOwnerTakeActionOnUserEnquiryAPIView.as_view(), name='club_owner_take_action_on_user_enquiry'),



    path(r'user_booking/', views.UserBookingAPIView.as_view(), name='user_booking'),
    path(r'owner_booking/', views.OwnerBookingAPIView.as_view(), name='owner_booking'),

    path(r'send_otp_mail_verified_property/', views.SendOtpOnMailVerifiedPropertyAPIView.as_view(), name='send_otp_mail_verified_property'),
    path('search/', views.SearchAPIView.as_view(), name='search'),
     path('filter/', views.FilterAPIView.as_view(), name='filter'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)