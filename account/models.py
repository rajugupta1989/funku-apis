from django.db import models
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
import uuid
import logging
from django.conf import settings
from master.models import bar_type, drink_type, gender, music_type
from rest_framework_jwt.settings import api_settings
from account.lib.auth.manager import UserManager
from account.utils import verification_mail
from common.core.validators import validate_mobile
from django.utils.text import gettext_lazy as _
from django.core.validators import validate_email
from django.utils import timezone
from django.core.mail import send_mail
from common.abstract_model import CommonAbstractModel


logger = logging.getLogger("accounts.token")


# Create your models here.
def get_jwt_secret(user_model):
    print("jwt_secret........", user_model)
    return user_model.jwt_secret


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(
        _("mobile"),
        max_length=16,
        unique=True,
        help_text=_(
            "required. mobile number must be entered in the format: '999999999'."
        ),
        validators=[validate_mobile],
        error_messages={"unique": _("user with mobile already exists")},
    )

    email = models.EmailField(
        _("Email Address"),
        max_length=100,
        unique=True,
        help_text=_(
            "required. email number must be entered in the format: 'abc@abc.com'."
        ),
        validators=[validate_email],
        error_messages={"unique": _("user with email already exists.")},
        blank=True,
        default=False,
        null=True,
    )
    mobile_otp = models.CharField(max_length=11, blank=True, null=True)
    email_otp = models.CharField(max_length=11, blank=True, null=True)
    email_otp_valid = models.DateTimeField(null=True, blank=True)
    # check mobile verified or not after registrations
    is_mobileVerify = models.IntegerField(default=0)
    # check email verified or not after registrations
    is_emailVerify = models.IntegerField(default=0)
    page_count = models.IntegerField(default=0)
    password = models.CharField(
        _("Password"),
        max_length=128,
        help_text=_("required. enter password."),
        blank=True,
        default=False,
        null=True,
    )

    jwt_secret = models.UUIDField(default=uuid.uuid4)
    role = models.ManyToManyField(Role,blank=True, null=True)
    profile_image_verifiy = models.BooleanField(default=False)
    first_name = models.CharField(
        _("first name"),
        max_length=30,
        help_text=_("required. please enter name "),
        blank=True,
        default=None,
        null=True,
    )

    last_name = models.CharField(
        _("last name"), max_length=150, blank=True, default=None, null=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    models.DateField()
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["email", "password"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # abstract = True

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        try:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            token = jwt_encode_handler(jwt_payload_handler(self))
        except Exception as ex:
            raise Exception(f"Token Generation Failed {ex}")
        # Update last login time after successful login
        update_last_login(None, self)
        return token

    def clean(self):
        # super.clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class userProfile(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    file_name = models.FileField(upload_to="documents", null=True, default=None)


class userProfileDetail(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    gender = models.ForeignKey(gender, on_delete=models.CASCADE,blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    music = models.ManyToManyField(music_type,blank=True)
    drink = models.ManyToManyField(drink_type,blank=True)
    bar = models.ManyToManyField(bar_type,blank=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)


class FileRepo(CommonAbstractModel):

    FILE_TYPE_CHOICES = (
        ("audio", "Audio"),
        ("video", "Video"),
        ("others", "Others"),
        ("jpg", "Jpg"),
        ("jpeg", "Jpeg"),
        ("img", "Img"),
        ("png", "Png"),
        ("links", "links"),
    )

    title = models.CharField(max_length=200,blank=False, null=True)
    description = models.TextField(max_length=200,blank=False, null=True)
    file = models.FileField(
        upload_to="documents", null=True, blank=True)
    file_type = models.CharField(
        max_length=200, choices=FILE_TYPE_CHOICES, default="others"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title