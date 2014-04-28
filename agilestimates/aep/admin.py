from django import forms
from django.contrib import admin
from aep.models import customer, profile

class customerInline(admin.StackedInline):
    model = customer

class profileInline(admin.StackedInline):
    model = profile

admin.site.register(customer)
admin.site.register(profile)