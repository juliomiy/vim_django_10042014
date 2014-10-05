# vim_app/api.py
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from vim_app.models import Customer, Markets
from tastypie.models import create_api_key
from django.contrib.auth.models import User
from django.db import models

models.signals.post_save.connect(create_api_key, sender=User)


class CustomerResource(ModelResource):
    class Meta:
        queryset = Customer.objects.all()
        resource_name = 'customer'
        excludes = ['email', 'password', 'active','createtimestamp','updatetimestamp','facebook_token', 'twitter_token' ,'wallet_token','paypal_token']
        allowed_methods = ['get']

class MarketsResource(ModelResource):
    class Meta:
        queryset = Markets.objects.all()
        resource_name = 'markets'
        allowed_methods = ['get']
#        authentication = ApiKeyAuthentication()

