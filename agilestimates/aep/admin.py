from django import forms
from django.contrib import admin
from aep.models import customer, user, profile


class customerInline(admin.StackedInline):
    model = customer

class userInline(admin.StackedInline):
    model = user

class profileInline(admin.StackedInline):
    model = profile

admin.site.register(customer)
admin.site.register(user)
admin.site.register(profile)
