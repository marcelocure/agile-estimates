from django.db import models

class customer(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    class Meta:
    	verbose_name="Customer"
    	verbose_name_plural = "Customers"

    def __unicode__(self):
    	return self.name
