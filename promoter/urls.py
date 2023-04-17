from django.urls import path
from promoter import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r"add_promoter/", views.AddPromoterAPIView.as_view(), name="add_promoter"),
    path(
        r"update_promoter/<int:pk>/",
        views.UpdatePromoterAPIView.as_view(),
        name="update_promoter",
    ),
    path(
        r"add_promoter_social_profile/",
        views.AddPromoterSocialProfileAPIView.as_view(),
        name="add_promoter_social_profile",
    ),
    path(
        r"update_promoter_social_profile/<int:pk>/",
        views.UpdatePromoterSocialProfileAPIView.as_view(),
        name="update_promoter_social_profile",
    ),
]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)