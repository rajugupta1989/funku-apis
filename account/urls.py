from django.urls import path
from account import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'role/', views.RoleAPIView.as_view(), name='role'),
    path(r'send_otp_mail/', views.SendOtpOnMailAPIView.as_view(), name='send_otp_mail'),
    path(r'verify_mail_otp/', views.MailOtpVerifiedAPIView.as_view(), name='verify_mail_otp'),
    path(r'send_otp/', views.Send_OtpAPIView.as_view(), name='send_otp'),
    path(r'verify/', views.Verify.as_view(), name='verify'),
    path(r'profile/', views.ProfileAPIView.as_view(), name='profile'),
    path(r'profile_image/', views.ProfileImageAPIView.as_view(), name='profile_image'),
    path(r'update_profile_image/', views.ProfileImageUpdateAPIView.as_view(), name='update_profile_image'),
    path(r'profile_detail/', views.ProfileDetailAPIView.as_view(), name='profile_detail'),
    path(r'update_profile_detail/', views.ProfileDetailUpdateAPIView.as_view(), name='update_profile_detail'),
    path(r'user_music_type/', views.userMusicTypeAPIView.as_view(), name='user_music_type'),
    path(r'user_drink_type/', views.userDrinkTypeAPIView.as_view(), name='user_drink_type'),
    path(r'user_bar_type/', views.userBarTypeAPIView.as_view(), name='user_bar_type'),
    path(r'file_repo/', views.FilesRepoAPIView.as_view(), name='file-repo-list'),
    path(r'file_repo/<int:pk>/', views.FileRepoAPIView.as_view(), name='file-rep_-detail'),
    path(r'user_search/', views.UserSearchAPIView.as_view(), name='user_search'),
    # path(r'resent/', views.Resent.as_view(), name='reset'),
    # path(r'login/', views.Login.as_view(), name='login'),
    # path(r'exist/<str:device>', views.UserExists.as_view(), name='exist'),
    # path(r'change-password/', views.ChangePassword.as_view(), name='change-password'),
    # path(r'profile/', views.Profile.as_view(), name='profile'),
    # path(r'logout/', views.Logout.as_view(), name='logout'),
    path(r'token-refresh/', views.RefreshToken.as_view(), name='refresh-token')

]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
