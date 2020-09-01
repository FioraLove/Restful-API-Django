# -*- coding:utf-8 -*-
from rest_framework.authentication import TokenAuthentication
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        if timezone.now() > (token.created + timedelta(
                days=settings.TOKEN_LIFETIME)):  # 重点就在这句了，这里做了一个Token过期的验证，如果当前的时间大于Token创建时间+7天，那么久返回Token已经过期
            raise exceptions.AuthenticationFailed(_('Token has expired'))
        return token.user, token
