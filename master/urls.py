from django.urls import path
from master import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        r"avatar_profile/", views.AvatarProfileAPIView.as_view(), name="avatar_profile"
    ),
    path(r"gender/", views.GenderAPIView.as_view(), name="gender"),
    path(r"music_type/", views.MusicAPIView.as_view(), name="music_type"),
    path(r"drink_type/", views.DrinkAPIView.as_view(), name="drink_type"),
    path(r"bar_type/", views.BarAPIView.as_view(), name="bar_type"),
    path(r"property_type/", views.PropertyTypeAPIView.as_view(), name="property_type"),
    path(r"country/", views.CountryAPIView.as_view(), name="country_view"),
    path(r"state_by_country/<int:pk>/", views.StateByCountryAPIView.as_view(), name="state_by_country"),
    path(r"city_by_state/<int:pk>/", views.CityByStateAPIView.as_view(), name="city_by_state"),
    path(r"payment_method/", views.PaymentMethodAPIView.as_view(), name="city-by-state"),
    path(r"facilities_available/", views.FacilitiesAvailableAPIView.as_view(), name="facilities_available"),
    path(r"artist_type/", views.ArtistTypeAPIView.as_view(), name="artist_type"),
    path(r"language/", views.LanguageAPIView.as_view(), name="language"),
    path(r"additional_feature/", views.AdditionalFeatureAPIView.as_view(), name="additional_feature"),
    path(r"deal_terms_and_conditions/", views.DealTermsAndConditionsAPIView.as_view(), name="deal_tearms_and_conditions"),
    path(r"flash_deal_for/", views.FlashDealForAPIView.as_view(), name="flash_deal_for"),
    path(r"brand_type/", views.BrandTypeAPIView.as_view(), name="brand_type"),
    path(r"deal_type/", views.DealTypeAPIView.as_view(), name="deal_type"),
    path(r"entry_type/", views.EntryTypeAPIView.as_view(), name="entry_type"),
    path(r"occasion/", views.OccasionAPIView.as_view(), name="occasion"),
    path(r"user_matching_profile_for/", views.UserMatchingProfileForAPIView.as_view(), name="user_matching_profile_for"),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)