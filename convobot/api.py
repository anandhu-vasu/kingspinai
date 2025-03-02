import base64
from convochannels.messenger_bot.views import get_facebook_page
from rest_framework.exceptions import ValidationError
import telegram
from convobot.exceptions import ChatbotNotFound
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenViewBase
from convobot.models import Auth
from crypt.crypt import Encrypt

class TokenObtainPairSerializer(TokenObtainSerializer):
    data = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        TokenObtainPairSerializer.data = kwargs.get("data",{})

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['expiry'] = refresh.access_token["exp"]

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        if not "chatbot" in self.data.keys():
            raise ValidationError({"chatbot": ["This field is required"]},"required")
        
        try:
            chatbot = self.user.chatbots.get(name=self.data.get("chatbot"))
        except:
            raise ChatbotNotFound()

        if not "uid" in self.data.keys():
            raise ValidationError({"uid": ["This field is required"]},"required")
        auth = self.data.get("auth",False)
        if auth:
            Auth.objects.update_or_create(chatbot=chatbot,uid=self.data.get("uid"),defaults={"uname":self.data.get("uname",None)})
            data['auth']=Encrypt(self.data.get("uid")).prependrandom.base64urlstrip.substitution()

        if chatbot.telegram_status and chatbot.telegram_key:
            try:
                data['telegram'] = telegram.Bot(token=chatbot.telegram_key).username
            except:
                pass
        if chatbot.messenger_status and chatbot.messenger_key:
            try:
                data['messenger'] = get_facebook_page(chatbot.messenger_key)['id']
            except:
                pass
        return data

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['chatbot'] = cls.data.get("chatbot",None)
        token['uid'] = cls.data.get("uid",None)
        if "uname" in cls.data.keys():
            token['uname'] = cls.data.get("uname",None)
        return token


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token),'expiry': refresh.access_token["exp"]}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data

class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer

class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshSerializer
