from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=30)
    operation_area = models.CharField(max_length=60)


class Profile(models.Model):
    name = models.CharField(max_length=30)


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, verbose_name="profile")

    class Meta:
        db_table = 'aep_user'


class Project(models.Model):
    name = models.CharField(max_length=30)
    customer = models.ForeignKey(Customer, verbose_name="customer")
    trello_board = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='ProjectUser')


class ProjectUser(models.Model):
    project = models.ForeignKey(Project, verbose_name="project")
    user = models.ForeignKey(User, verbose_name="user")

    class Meta:
        db_table = 'aep_user_project'


class Session(models.Model):
    username = models.CharField(max_length="30")
    login_date = models.DateField()


class Sprint(models.Model):
    description = models.CharField(max_length=600)
    project = models.ForeignKey(Project, verbose_name="project")
    start_date = models.DateField()
    end_date = models.DateField()
    points_estimated = models.FloatField(null=True)
    points_delivered = models.FloatField(null=True)
    number_of_tests = models.IntegerField(null=True)
    date_scanned = models.DateField(null=True)

class Card(models.Model):
    sprint = models.ForeignKey(Sprint, verbose_name='sprint')
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()
    points_created = models.FloatField(null=True)
    tests_created = models.IntegerField(null=True)
