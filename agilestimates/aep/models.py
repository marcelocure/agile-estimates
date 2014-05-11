from django.db import models

class customer(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=30)
    operation_area = models.CharField(max_length=60)

    class Meta:
    	verbose_name="Customer"
    	verbose_name_plural = "Customers"

    def __unicode__(self):
    	return self.name


class profile(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
    	verbose_name="Profile"
    	verbose_name_plural = "Profiles"

    def __unicode__(self):
    	return self.name


class user(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    id_profile = models.ForeignKey(profile, verbose_name="user profile")
    
    class Meta:
    	verbose_name="User"
    	verbose_name_plural = "Users"

    def __unicode__(self):
    	return self.username


class project(models.Model):
    name = models.CharField(max_length=30)
    customer_id = models.ForeignKey(customer, verbose_name="customer")
    
    class Meta:
        verbose_name="Project"
        verbose_name_plural = "Projects"

    def __unicode__(self):
        return self.username
