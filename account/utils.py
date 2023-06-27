import uuid
import requests
from calendar import timegm
from datetime import datetime
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.settings import api_settings
import re


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False



def verification_mail(user, token, time_validity):
    # token_message = _("SMAS OTP Verification {token}")
    # token_message = token_message.format(token=token)
    try:
        html_message = render_to_string(
            'mailer/verification.html',
            {'name': user.get_full_name().title(), 'otp': token, 'time_validity': time_validity})
        user.email_user("SMAS OTP Verification", None, "admin@smas.com", html_message=html_message)
    except Exception as ex:
        raise Exception('mail failed to sent due to {}'.format(ex))  # ex.args
    return True


def sent_sms(mobile):
    try:
        data = settings.SMS_GETWAY[settings.SMS_GETWAY["DEFAULT"]]
        url = data['url']+data['apikey']+'/SMS/'+mobile+'/AUTOGEN'
        response = requests.get(url)
        print('url',url)
        
        return response
    except Exception as ex:
        raise Exception("sms failed to sent due to {}".format(ex))
    return True

def otp_verify(mobile,otp,session_id):
    try:
        data = settings.SMS_GETWAY[settings.SMS_GETWAY["DEFAULT"]]
        url = data['url']+data['apikey']+'/SMS/VERIFY/'+session_id+'/'+otp
        response = requests.get(url)
        print('url',url)
        return response
    except Exception as ex:
        raise Exception("sms failed to sent due to {}".format(ex))
    return True


def jwt_payload_handler(user):
    try:
        # Update JWT Secret Key on every new token generation
        user.jwt_secret = uuid.uuid4()
        user.save()

        username_field = get_username_field()
        username = get_username(user)
        payload = {
            'user_id': user.pk,
            'username': username,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
        }
        if hasattr(user, 'email'):
            payload['email'] = user.email
        if hasattr(user, 'mobile'):
            payload['mobile'] = user.mobile
        if isinstance(user.pk, uuid.UUID):
            payload['user_id'] = str(user.pk)

        payload[username_field] = username

        # Include original issued at time for a brand new token,
        # to allow token refresh
        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(
                datetime.utcnow().utctimetuple()
            )

        if api_settings.JWT_AUDIENCE is not None:
            payload['aud'] = api_settings.JWT_AUDIENCE

        if api_settings.JWT_ISSUER is not None:
            payload['iss'] = api_settings.JWT_ISSUER
    except Exception as ex:
        raise Exception(f"JWT Payload handler failed due to {ex}")

    return payload




def user_activate(user):
    user_obj = User.objects.get(id=user.id)
    user_obj.is_active
    user_obj.save()
    return True