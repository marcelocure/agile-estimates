from django import forms
from django.contrib import admin
from aep.models import customer


class customerInline(admin.StackedInline):
    model = customer

admin.site.register(customer)
