from django import forms
from django.contrib import admin
from aep.models import customer, profile

class customerInline(admin.StackedInline):
    model = customer

class profileInline(admin.StackedInline):
    model = profile


#class csnDetailAdmin(forms.ModelForm):
#    class Meta:
#        model = customer
#        widgets = {'name': AutosizedTextarea(),
#                   'country' : AutosizedTextarea()}


#class csnInline(vlmModelAdmin):
#    readonly_fields = []
#    model = customer
#    fields = ((('id','name','country',),) )
#    extra = 0
#    form = csnDetailAdmin
    #----------------------------------------------------------------------------------
#    def customer_link(self, obj):
#        return mark_safe('<a href="/admin/aep/customer/%s">ediiiiit</a>' % obj.id)
#    customer_link.short_description = 'Click to Edit'

admin.site.register(customer)
admin.site.register(profile)