from django import forms
from django.contrib import admin
from aep.models import Customer, User, Profile


class customerInline(admin.StackedInline):
    model = Customer

class userInline(admin.StackedInline):
    model = User

class profileInline(admin.StackedInline):
    model = Profile

admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Profile)
