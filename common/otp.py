import time
from binascii import unhexlify
from django.conf import settings
from common.core import topt
from account.models import User
from rest_framework.response import Response
from rest_framework import status


def user_activate(user):
    try:
        user_obj = User.objects.filter(id=user.id).last()
        user_obj.is_active=True
        user_obj.save()
        return True
    except Exception as e:
        print(str(e))
        error = {'status': False, 'message': "Something Went Wrong","error":str(e)}
        return Response(error, status=status.HTTP_200_OK)



def Update_page_count(user,page):
    data = User.objects.filter(id=user.id).last()
    data.page_count=page
    data.save()
    return True


class OTP:
    def __init__(self, secret_key):
        self.step = settings.TOTP_TOKEN_VALIDITY
        self.digits = settings.TOTP_DIGITS
        self.secret_key = secret_key

    @property
    def bin_key(self):
        return unhexlify(self.secret_key.encode())

    def totp_obj(self):
        totp = topt.TOTP(key=self.bin_key, step=self.step, digits=self.digits)
        totp.time = time.time()
        return totp

    def generate_otp(self):
        totp = self.totp_obj()
        return str(totp.token()).zfill(self.digits)

    def otp_validity(self):
        return self.step // 60


